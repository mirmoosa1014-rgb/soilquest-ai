# Architecture

`field.generate` creates a deterministic 18 × 18, 100 × 100 m spatial concentration field and blocked cells. This is a stochastic Gaussian-plume generator, **not** a transport PDE. Isotropic plumes mimic diffusion-shaped fields; the directional family uses anisotropic covariance as a transport-shaped stress case, not a physically integrated advection solver. There is no time evolution or mass conservation claim.

`Sampler` is the sole measurement boundary. Noise is Gaussian σ=3 mg/kg and indexed by seed and cell, then measurements are clipped at zero. Policies never receive a field object or truth array. Every policy begins at cell 0 with the same noisy observation. Concentrations are fictional mg/kg units, not measurements or regulatory thresholds.

`model.predict` fits a Gaussian process using only coordinates and acquired measurements. `policy.choose` sees the resulting mean/standard deviation, sample history, obstacle map and remaining travel. `routes` uses four-connected breadth-first shortest paths. Movement is charged at 100/17 m per edge, including all intermediate path cells; intermediate cells yield no free samples. Return-to-base is not required. Both sample and travel ceilings are enforced, so different policies can stop with fewer samples.

`simulation.run` owns the hidden evaluator and computes metrics on traversable, unobserved cells. It adds ground truth only to the returned evaluator payload after policy execution. This is a separation of algorithm interfaces, not an adversarial security boundary: the local UI can inspect evaluation truth by design.

FastAPI exposes bounded GET endpoints. React replays acquisition by deterministic recomputation and aborts obsolete requests; jobs are capped at 40 samples on 324 cells and take well below one second per episode in the measured batch. There is no long-running background job system. The paired comparison uses identical field seeds, noise and resource ceilings. SVG heatmaps and a depth-sorted orthographic 3D mesh render actual posterior values. Rotation changes the viewing angle, never the model output.
