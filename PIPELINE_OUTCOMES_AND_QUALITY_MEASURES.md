# Truck simulation pipeline, outcome files, and quality measures

This guide explains what the pipeline produces, which files should be used for the thesis, and how the reported quality measures should be read.

## The main distinction

The result folders answer three different questions:

1. **Discovery diagnostics:** Did the discovery methods learn reasonable arrival, duration, routing, and resource patterns from the training data?
2. **Held-out validation:** Does one frozen ProSiT model reproduce the unseen 20% test log?
3. **Scenario analysis:** What changes inside this frozen model when an input is changed?

Scenario results are model results. They are not independent proof that the same causal effect would occur at the real terminal.

## Pipeline overview

```mermaid
flowchart LR
    A["Processed CTB event log<br/>s6 event log"] --> B["Chronological 80/20 split"]
    B --> C["Training log<br/>s6_train.csv"]
    B --> D["Held-out log<br/>s6_test.csv"]

    C --> E["Discovery diagnostics<br/>arrivals, durations, features,<br/>resource overlap"]
    C --> F["ProSiT discovery<br/>sequential CTB calibration"]
    F --> G["Frozen source bundle<br/>prosit_params.pkl"]
    G --> H["Derived final bundle<br/>RMG max concurrency = 3"]

    D --> I["Single-run detailed validation<br/>activity, case, arrival, routing plots"]
    G --> I

    D --> J["Final 10-seed held-out validation<br/>means, standard deviations, 95% CIs"]
    H --> J

    H --> K["Matched-seed scenarios<br/>baseline, T22 closed, demand +20%"]
    K --> L["Paired scenario effects<br/>and structural contracts"]

    E --> M["Sensitivity and robustness evidence"]
    J --> N["RQ1: reproduction of observed behaviour"]
    E --> O["RQ2 and RQ3: limitations and specification sensitivity"]
    L --> P["RQ4: what-if capability"]
```

## Which result folders are current?

### Final thesis evidence

- **Discovery source:** `../trucksimulation/baseline/discovery_params/params_20260816_214403_train80/prosit_discovery_workload_sequential_calibrated/`
- **Final held-out validation:** `../trucksimulation/validation/results/prosit_sequential_calibrated_rmg_cap3_vs_holdout_ci/`
- **Final scenarios:** `../trucksimulation/validation/results/prosit_sequential_calibrated_scenarios_rmg_cap3_ci/`
- **Temporal split:** `../trucksimulation/validation/results/split_manifest.json`

### Supporting detailed results

- **Single-run validation with detailed activity and distribution files:** `../trucksimulation/validation/results/prosit_sequential_calibrated_vs_holdout/`
- **Percentile sensitivity:** `../trucksimulation/validation/results/percentile_sensitivity/`
- **Receive/delivery utilisation:** `../trucksimulation/validation/results/receive_delivery_utilisation/`
- **Context-rule audit:** `../trucksimulation/validation/results/prosit_context_rule_audit/`

The folders named `prosit_train80_*`, older timestamped validation folders, and the uncapped `prosit_sequential_calibrated_scenarios_ci` folder are development, screening, or diagnostic runs. They should not replace the final cap-3 validation and scenario folders in the thesis.

## The files to open first

| Order | File | What it tells you |
|---:|---|---|
| 1 | `validation/results/split_manifest.json` | How the full log was split; case and event counts; cutoff date; leakage checks. |
| 2 | `.../prosit_discovery_workload_sequential_calibrated/prosit_run_summary.json` | Discovery inputs, settings, calibration, output paths, and model metadata. |
| 3 | `.../prosit_discovery_workload_sequential_calibrated/prosit_conformance.csv` | Training and test process-model conformance. |
| 4 | `.../prosit_sequential_calibrated_rmg_cap3_vs_holdout_ci/mc_summary.csv` | Main held-out validation measures averaged across ten seeds, including 95% confidence intervals. |
| 5 | `.../prosit_sequential_calibrated_rmg_cap3_vs_holdout_ci/yard_activity_emd_summary.csv` | Activity-level service-time EMDs for the yard activities. |
| 6 | `.../prosit_sequential_calibrated_scenarios_rmg_cap3_ci/scenario_parameter_changes.json` | The exact parameters changed in each scenario and the parameters intentionally kept constant. |
| 7 | `.../prosit_sequential_calibrated_scenarios_rmg_cap3_ci/scenario_paired_delta_summary.csv` | Main scenario effects calculated against the matched baseline seed. |
| 8 | `.../prosit_sequential_calibrated_scenarios_rmg_cap3_ci/scenario_contracts.csv` | Whether every scenario run remained structurally valid. All hard-failure columns must be zero. |

The pickle file `prosit_params.pkl` is the executable source of truth for a discovered model. `prosit_params.json` is a large human-readable audit representation, but the simulation should not be reconstructed from it.

## Stage-by-stage output map

| Stage | Main outcome files | Use in the thesis |
|---|---|---|
| Event-log construction | `data/processed/CTB/s6_eventlog_target_rank_features.csv` and event-log audit files | Defines the reproducible abstraction of terminal operations. |
| Temporal split | `s6_train.csv`, `s6_test.csv`, `split_manifest.json` | Demonstrates a chronological 80/20 split and separation of training and test cases. |
| Arrival discovery | `arrival_rate_analysis.csv`, `arrival_rate_by_period.csv`, `arrival_cv_summary.csv`, `arrival_hyperparameter_sensitivity.csv` | Compares pooled and time-aware arrival models and documents cross-validation. |
| Duration and context discovery | `data_aware_model_summary.csv`, `duration_cv_summary.csv`, `tree_feature_importance.csv` | Shows whether contextual decision trees improve duration predictions and which attributes are used. |
| Resource diagnostics | `discovered_resource_capacities.csv`, `capacity_sensitivity_summary.csv` | Exploratory overlap and capacity proxies. These are not the authoritative final per-resource ProSiT capacities. |
| ProSiT discovery | `prosit_params.pkl`, `prosit_run_summary.json`, `control_flow_contract.json`, `ctb_calibration.json`, `prosit_conformance.csv` | Defines and audits the frozen simulation model. |
| Single-run held-out validation | `metrics_activity.csv`, `metrics_arrival.csv`, `metrics_case.csv`, `routing_comparison.csv`, `summary.json`, `figures/` | Detailed diagnosis of where the simulated and real distributions agree or differ. |
| Final multi-seed validation | `mc_replications.csv`, `mc_summary.csv`, `yard_activity_emd_replications.csv`, `yard_activity_emd_summary.csv`, `figures/` | Main RQ1 evidence, including Monte Carlo variability over ten seeds. |
| Percentile sensitivity | `transition_baselines_by_percentile.csv`, `waiting_time_shift_summary.csv`, `figures/` | Tests how the enabled-time baseline changes when another empirical percentile is chosen. |
| Robustness screening | `robustness_summary.csv` and the `prosit_no_enabled_*_ci` folders | Compares plausible model specifications. Useful for RQ3, but it is not the final held-out model result. |
| Scenario analysis | `scenario_replications.csv`, `scenario_kpi_summary.csv`, `scenario_paired_deltas.csv`, `scenario_paired_delta_summary.csv`, `scenario_contracts.csv`, `scenario_parameter_changes.json` | Main RQ4 evidence. The paired-delta summary is the main effect table. |
| Capacity robustness of scenarios | `capacity_sensitivity_paired_delta_summary.csv`, `capacity_sensitivity_interaction_summary.csv` | Shows whether scenario conclusions change under another plausible capacity specification. |

## Quality measures: meaning and interpretation

### Distribution and KPI measures

| Measure | Better value | Meaning | Important warning |
|---|---:|---|---|
| EMD / Wasserstein distance | 0 | Average distance needed to align two empirical distributions. For times, the unit is minutes. | There is no universal pass threshold. Interpret it relative to the KPI scale and alternative models. |
| KS statistic | 0 | Largest vertical gap between the real and simulated cumulative distributions. It ranges from 0 to 1. | The KS p-value is strongly influenced by sample size. The statistic is the more useful effect-size description here. |
| Absolute mean, median, or P90 error | 0 | Absolute difference between the simulated and real summary value. | A small mean error does not guarantee a matching distribution. Use it together with EMD, KS, and quantiles. |
| Relative error | 0 | Absolute or signed difference divided by the real value. | CSV values are fractions; multiply by 100 to report percentages. |
| Yard activity-rate L1 error | 0 | Sum of absolute differences in events per case across all yard activities. | It measures event mix, not activity timing. |
| Maximum activity-rate error | 0 | Largest event-per-case difference for one activity. | Check the detailed activity file to identify the activity responsible. |

`service_time_min` is calculated as `complete - start`. Case turnaround is calculated from the first start to the last completion in a case. Interarrival time is calculated from differences between the first timestamps of consecutive cases.

### Prediction measures used during discovery

| Measure | Better value | Meaning |
|---|---:|---|
| MAE | 0 | Mean absolute prediction error. It is easy to interpret in the target unit. |
| RMSE | 0 | Root mean squared error. Large errors receive more weight than in MAE. |
| R-squared | 1 | Share of variance explained relative to a mean prediction. A value near 0 gives little improvement over the mean; a negative value is worse than the mean predictor. |
| Feature importance | Context-dependent | Importance assigned to an input by one fitted decision tree. Importances sum to one within that tree. | It shows model usage or association, not a causal effect. |

### Process-model conformance

| Measure | Better value | Meaning |
|---|---:|---|
| Fitness | 1 | How much observed log behaviour can be replayed by the discovered process model. |
| Fit traces | 100% | Share of traces that fit the discovered model. |
| Precision | 1 | How strongly the model avoids behaviour that was not observed. |
| Generalisation | Usually higher | Ability to allow plausible behaviour beyond the exact training traces. | It is a trade-off. A strict trace model can have high fitness and precision but lower generalisation. |
| Simplicity | Usually higher | Structural simplicity of the process model. | It is not a stand-alone validity test. |

### Multi-seed uncertainty and scenario effects

| Column or measure | Interpretation |
|---|---|
| `mean` | Average result across the ten random simulation seeds. |
| `std` | Variation between seeds. Lower values mean more stable repeated simulations. |
| `ci95_lo`, `ci95_hi` | Student-t 95% confidence interval for Monte Carlo variability across the ten seeds in `mc_summary.csv`. Scenario summaries use `ci95_delta_lo` and `ci95_delta_hi`. |
| Paired delta | Scenario result minus the baseline result for the same seed. Positive and negative values must therefore be interpreted according to the KPI. |
| `ci_excludes_zero` | `true` means the paired effect was resolved at this Monte Carlo level; `false` means the interval still includes no effect. |

These confidence intervals only describe random-seed uncertainty for one frozen model and one test log. They do not cover uncertainty from event-log construction, model discovery, input selection, or the correctness of the real-world causal assumptions.

### Structural contract measures

The contract columns are hard gates, not soft quality scores. The following values must be zero:

- gate-only cases;
- incorrect case boundaries;
- overlapping activities within a sequential case;
- decreasing completion times;
- Gate Out before the final yard activity;
- wrong case counts;
- assignments to prohibited resources;
- durations above the defined 24-hour validity bound.

A model with a good EMD but failed structural contracts should not be treated as valid.

## Important limitations when reading the files

### Real waiting time is unavailable

The real event log does not contain an `enabled` timestamp. Therefore, the real side of `metrics_waiting.csv` is empty and real-versus-simulated waiting-time EMD is not available. Simulated `start - enabled` can be described as **model-derived pre-service time**, but it should not be presented as a validated real queueing time.

### Raw and robust timing measures

The robust calculation clips valid observations to a maximum of 1,440 minutes. In the final validation, the raw and robust values are identical because no accepted observations exceeded 24 hours. Both columns are kept for auditability.

### Weighted and unweighted yard EMD

- **Unweighted yard EMD:** every non-gate activity has the same influence.
- **Real-frequency-weighted yard EMD:** activities with more held-out real events receive more influence.

The weighted result better describes the error experienced by a typical observed yard event; the unweighted result prevents rare activities from disappearing in the average.

## Snapshot of the final results

### Data split and process conformance

- Full log: 89,460 cases and 275,408 events.
- Training log: 71,568 cases and 220,048 events.
- Held-out log: 17,892 cases and 55,360 events.
- Temporal cutoff: 20 April 2026 at 18:17.
- Test fitness: 0.99985; fit traces: 99.944%; precision: 0.96057.
- Ten unseen test variants represented ten cases, or 0.0559% of held-out cases.

### Final cap-3 held-out validation over ten seeds

| Result | Final mean | 95% Monte Carlo CI |
|---|---:|---:|
| Case-turnaround EMD | 9.306 min | 9.229 to 9.384 |
| Simulated mean turnaround | 30.436 min | 30.359 to 30.514 |
| Real mean turnaround | 39.742 min | Fixed held-out reference |
| Simulated turnaround P90 | 51.8 min | 51.498 to 52.102 |
| Real turnaround P90 | 71.0 min | Fixed held-out reference |
| Yard service-time EMD, unweighted | 2.999 min | 2.888 to 3.110 |
| Yard service-time EMD, real-frequency weighted | 2.340 min | 2.279 to 2.402 |
| Interarrival EMD | 0.072 min | 0.067 to 0.077 |
| Yard activity-rate L1 error | 0.187 | 0.184 to 0.189 |

All final structural contract failure counts are zero. The arrivals and yard service times are reproduced more closely than the complete case-turnaround distribution. In particular, the model underestimates the mean and upper tail of turnaround time.

### Final paired scenario effects

| Scenario | Change in mean turnaround versus matched baseline | 95% paired CI | Resolved away from zero? |
|---|---:|---:|---|
| T22 closed | +0.012 min | -0.102 to +0.127 | No |
| Demand +20% | -0.033 min | -0.128 to +0.063 | No |

The scenarios executed correctly and the T22-closed runs produced zero T22 assignments. However, the final paired intervals include zero for the main turnaround effects. The correct conclusion is therefore that the model supports technically valid what-if execution, but no clear operational effect was resolved under its present resource and congestion representation.

## Mapping the evidence to the research questions

| Research question | Main evidence | What it supports |
|---|---|---|
| RQ1: reproduction of observed behaviour | `prosit_conformance.csv`, final `mc_summary.csv`, `yard_activity_emd_summary.csv`, detailed single-run metrics | Accuracy for control flow, arrivals, activity mix, service times, and case turnaround; also where the model underestimates the upper tail. |
| RQ2: modelling challenges and limitations | Event-log contracts, calibration file, detailed activity results, missing real enabled timestamps, model audits | Problems caused by event-log abstraction, missing queue observations, resource representation, and the difference between structural and operational validity. |
| RQ3: alternative specifications | Percentile sensitivity, no-rules versus rules/workload screening, resource-capacity and scenario-capacity sensitivity | How assumptions about enabled times, context rules, workloads, and capacities affect predictions and conclusions. |
| RQ4: previously unobserved what-if scenarios | Parameter-change audit, paired scenario deltas, scenario contracts, T22-focused summary | Whether the frozen model can execute controlled counterfactual inputs and whether their effects are stable and structurally valid. |

Together, these results address the broader research objective: evaluating the accuracy, limitations, robustness, and decision-support capability of automatically discovered data-aware simulation models for container-terminal truck operations.

## Two consistency checks before final submission

1. **Percentile correlation label:** `corr_with_ref` in `validation/04_baseline_percentile_sensitivity.py` is currently calculated with the default pandas Pearson correlation. If the thesis calls this Spearman's rho or a rank correlation, either change the wording to Pearson correlation or change the script to `method="spearman"` and regenerate the output.
2. **Arrival benchmark values:** the current `arrival_rate_analysis.csv` reports time-aware MAE 9.414, RMSE 16.873, and R-squared 0.762; the pooled model reports MAE 28.982, RMSE 34.596, and R-squared approximately -0.001. These do not exactly match the current Chapter 5 values of 9.04, 16.15, 0.777, and pooled RMSE 34.19. The table and its run source should be reconciled before submission.
