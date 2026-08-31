# Final CTB result sources

This directory contains the compact result set used to update the thesis after
the final train--validation--test run. The four configurations were discovered
on the first 64% of cases and compared on the following 16%. `visit_only` was
selected by the rule recorded in `selection_manifest.json`, rediscovered on
the combined 80% development data, and evaluated once on the untouched final
20%.

`control_flow_contract.json` identifies the raw Inductive-Miner tree and the
expert-repaired sequential source model used by all configurations.
`final_test_cap3_mc_summary.csv` and `final_test_ngd_summary.csv` provide the
final RQ1 results. `final_test_uncapped_mc_summary.csv` is the matching physical
capacity sensitivity. The scenario files report the final T22 and demand
interventions. SHA-256 hashes are recorded in `provenance_manifest.json`.
