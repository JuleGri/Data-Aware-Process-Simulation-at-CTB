#!/usr/bin/env python3
"""Audit ProSiT JSON round trips for the frozen final CTB scenario bundles."""

from __future__ import annotations

import argparse
import hashlib
import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from prosit.simulator import SimulatorParameters


REPO = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = (
    REPO / "validation/results/standardized_20260830_visit_only_scenarios_cap3_ci"
)
DEFAULT_OUTPUT = REPO / "validation/results/json_roundtrip_audit_final_ctb"
FILES = {
    "baseline": "params_baseline_rmg_max_concurrency_3.pkl",
    "t22_closed": "params_t22_closed.pkl",
    "demand_plus_20pct": "params_demand_plus_20pct.pkl",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def array_summary(values: Any) -> dict[str, Any]:
    array = np.asarray(values, dtype=float)
    raw = array.astype("<f8", copy=False).tobytes()
    return {
        "n": int(array.size),
        "sha256_float64": hashlib.sha256(raw).hexdigest(),
        "mean": None if array.size == 0 else float(array.mean()),
        "p50": None if array.size == 0 else float(np.quantile(array, 0.50)),
        "p90": None if array.size == 0 else float(np.quantile(array, 0.90)),
        "min": None if array.size == 0 else float(array.min()),
        "max": None if array.size == 0 else float(array.max()),
    }


def sampled_nodes(value: Any, prefix: str) -> list[dict[str, Any]]:
    rules = getattr(value, "rules", None)
    if not isinstance(rules, dict):
        return []
    rows: list[dict[str, Any]] = []

    def visit(node: Any, path: str) -> None:
        if isinstance(node, dict):
            if "sampled" in node:
                rows.append({"path": path, **array_summary(node["sampled"])})
            for key, child in node.items():
                if key != "sampled":
                    visit(child, f"{path}/{key}")
        elif isinstance(node, (list, tuple)):
            for index, child in enumerate(node):
                visit(child, f"{path}/{index}")

    visit(rules, prefix)
    return rows


def all_sampled_nodes(params: SimulatorParameters) -> list[dict[str, Any]]:
    rows = sampled_nodes(params.arrival_time_distribution, "arrival")
    for name, value in params.execution_time_distributions.items():
        rows.extend(sampled_nodes(value, f"execution/{name}"))
    for name, value in params.waiting_time_distributions.items():
        rows.extend(sampled_nodes(value, f"waiting/{name}"))
    for name, value in params.transition_weights.items():
        rows.extend(sampled_nodes(value, f"routing/{name}"))
    for name, value in params.resource_weights.items():
        rows.extend(sampled_nodes(value, f"resource/{name}"))
    return rows


def stable_json(value: Any) -> str:
    def normalize(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {str(key): normalize(val) for key, val in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [normalize(item) for item in obj]
        if isinstance(obj, np.generic):
            return obj.item()
        return obj

    return json.dumps(normalize(value), sort_keys=True, default=str, separators=(",", ":"))


def main() -> int:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    summary_rows: list[dict[str, Any]] = []
    sampled_rows: list[dict[str, Any]] = []

    for scenario, filename in FILES.items():
        pickle_path = args.source / filename
        with pickle_path.open("rb") as handle:
            original = pickle.load(handle)

        json_path = args.output / f"{scenario}.json"
        original.to_json(str(json_path))
        restored = SimulatorParameters(
            original.net, original.initial_marking, original.final_marking
        )
        restored.from_json(str(json_path))

        original_samples = all_sampled_nodes(original)
        restored_samples = all_sampled_nodes(restored)
        for representation, rows in (
            ("frozen_pickle", original_samples),
            ("json_roundtrip_before_runtime", restored_samples),
        ):
            for row in rows:
                sampled_rows.append(
                    {"scenario": scenario, "representation": representation, **row}
                )

        original_arrival = next(
            (row for row in original_samples if row["path"].startswith("arrival/")),
            None,
        )
        restored_arrival = next(
            (row for row in restored_samples if row["path"].startswith("arrival/")),
            None,
        )
        attr_equal = stable_json(original.distribution_data_attributes) == stable_json(
            restored.distribution_data_attributes
        )
        summary_rows.append(
            {
                "scenario": scenario,
                "pickle_sha256": sha256(pickle_path),
                "json_sha256": sha256(json_path),
                "rules_mode_equal": original.rules_mode == restored.rules_mode,
                "use_workload_features_equal": (
                    original.use_workload_features == restored.use_workload_features
                ),
                "resources_equal": original.resources == restored.resources,
                "max_concurrency_equal": (
                    original.max_concurrency == restored.max_concurrency
                ),
                "calendars_equal": original.calendars == restored.calendars,
                "empirical_case_attribute_distribution_equal": attr_equal,
                "pickle_sampled_nodes": len(original_samples),
                "roundtrip_sampled_nodes_before_runtime": len(restored_samples),
                "pickle_arrival_sample_n": (
                    0 if original_arrival is None else original_arrival["n"]
                ),
                "roundtrip_arrival_sample_n_before_runtime": (
                    0 if restored_arrival is None else restored_arrival["n"]
                ),
                "ctb_calibration_metadata_in_pickle": hasattr(original, "ctb_calibration"),
                "ctb_calibration_metadata_after_roundtrip": hasattr(restored, "ctb_calibration"),
            }
        )

    summary = pd.DataFrame(summary_rows)
    sampled = pd.DataFrame(sampled_rows)
    summary.to_csv(args.output / "roundtrip_summary.csv", index=False)
    sampled.to_csv(args.output / "sampled_node_inventory.csv", index=False)
    manifest = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "prosit_json_contract": (
            "Official to_json/from_json representation of discovered parameters."
        ),
        "audit_question": (
            "Whether the exact post-calibration in-memory sample state of the final "
            "CTB bundles survives a JSON round trip."
        ),
        "scope": (
            "CTB bundles and installed ProSiT version only; this is not a claim that "
            "JSON is generally inferior to pickle."
        ),
        "source": str(args.source.resolve()),
        "summary": summary_rows,
        "outputs": ["roundtrip_summary.csv", "sampled_node_inventory.csv"],
    }
    (args.output / "roundtrip_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(f"\nAudit written to {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
