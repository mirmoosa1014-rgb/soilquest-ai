# Evaluation protocol and results

The full bounded run contains 96 episodes: two held-out families × four seeds (41–44) × three sample ceilings (8,16,24) × four policies. Every comparison shares field, potential cell measurement noise, starting sample, 650 m travel ceiling, and requested sample ceiling. Report actual acquired samples separately. Random policy may consume travel rapidly; random and uncertainty policies are feasible rather than optimized robot routing baselines.

The regular-grid baseline traverses a fixed 5 × 5 lattice in alternating rows, skipping blocked and unreachable sites. Once lattice sites are exhausted it falls back to fixed row-major sites. Uncertainty sampling greedily maximizes latent SD. Balanced sampling scores `(SD + 0.35 max(mean−45,0))/(1+travel/70)` and cannot inspect true concentrations.

At the 24-sample ceiling, arithmetic means over eight held-out fields:

| Policy | RMSE mg/kg | Hotspot recall | Actual samples | Travel m |
|---|---:|---:|---:|---:|
| Random | 12.25 | 11.3% | 10.00 | 647.1 |
| Regular grid | 9.40 | 45.2% | 24.00 | 629.4 |
| Uncertainty | 11.57 | 10.3% | 7.00 | 647.1 |
| Balanced | 8.86 | 28.5% | 22.25 | 633.1 |

These are descriptive results from only eight fields per ceiling, not statistical significance or general superiority. Balanced has lower average RMSE here, while regular grid finds more hotspots. Broad credible intervals lead to 96.8–99.5% coverage, yet recall remains weak. The seed-41 narrow-hotspot demo misses its approximately 80 mg/kg hotspot even after 20 acquired samples. This failure is displayed deliberately.

Metrics use unobserved traversable cells only. RMSE and MAE compare posterior means with true synthetic concentration. Hotspots are ≥50 mg/kg, an illustrative threshold with no regulatory meaning. Precision or recall is null when its denominator is zero. `max_missed_mgkg` is the largest true concentration of a false-negative cell, otherwise zero. Coverage is the fraction of unobserved true values inside the nominal latent interval. Bands in the research figure are ±one population SD across fields, not confidence intervals.

Data: `results/benchmark.csv`, `summary.json`, `benchmark-meta.json`, `demo.json`. The quick run has eight episodes and overwrites the same representative output files; rerun the full benchmark before regenerating report figures. All results are synthetic.

Recovery validation: source was reconstructed from retained authored transcript after the original Mac environment disconnected. Model, metrics and visual evidence were regenerated using the same code, fields, seeds and budgets. Rounding-level differences from the Mac are expected because scientific library versions/platform changed. See `progress.md` for exact validation and outstanding limitations.
