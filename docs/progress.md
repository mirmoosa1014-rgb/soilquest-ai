# Progress and recovery record

## Complete locally

- Seeded spatial field generator; noisy per-cell sampler with no duplicates; observation-only Gaussian process; four sampling policies; obstacle-aware BFS routing and actual travel accounting.
- Length-scale training on 18 fields from smooth/multiple/background families. Narrow/directional families and seeds 41–44 remain held out.
- React/TypeScript workbench, acquisition replay, paired four-policy comparison, evaluator reveal, complete JSON export and rotatable 3D posterior mesh.
- Professional README, architecture/model/evaluation documents, accessible explanations, 90-second demo and truthful contribution statement.
- Actual experiment data, six-panel research figure, 3D posterior figure, real-engine animation and authentic browser screenshots.

## Verified in the recovered Linux environment

- 12 scientific/interface/API tests passed, including a second run in a fresh isolated environment installed from pinned requirements.
- Frontend clean `npm ci` and TypeScript/Vite production build passed.
- Browser integration test passed: acquire sample, replay count, hidden-truth reveal, 3D rotation, audit download, policy selection, mobile width and sample-ceiling/family-change boundary.
- FastAPI server launched successfully on loopback for browser tests. Earlier Mac permission errors do not apply to the recovered runtime.
- Quick eight-episode and full 96-episode benchmarks ran; full results retained. Measured full-run wall time: about 1.25 s in this environment, excluding training/visualization.
- Visual inspection performed on generated research-overview and authentic browser screenshot. Browser images: `docs/images/workbench.png` (full page) and `workbench-hero.png` (viewport).
- CI workflow provided with contents-read permissions. Remote CI has not run because no repository has been published.

## Recovery provenance

The Mac environment disconnected during the original build. Its filesystem, environments and original generated image bytes are no longer accessible here. The implementation source, tests, analysis scripts and existing authored documentation were reconstructed from retained authored tool-call text; no inaccessible Mac file is claimed copied. The original `PROJECT_BRIEF.md` bytes were not carried forward. The README, final configuration and verification record were completed after recovery.

Model metadata, CSV/JSON results and all figure/GIF files were regenerated using the same implementation, seeds, families, budgets and model selection candidates. Numeric results match the earlier Mac run up to floating-point precision. Pixel-identical image recovery is not claimed: rendering libraries, fonts and platform changed. The frontend lockfile was regenerated from the same pinned major packages, and Python pins now match the verified Linux environment (NumPy 2.3.5/SciPy 1.17.0/matplotlib 3.10.8). A full Python dependency lock was captured from the successful fresh install.

A small UI correction made after recovery ensures switching field family never resets the observation counter above a smaller selected sample ceiling. The browser test exercises this boundary. A Vite API proxy and automatic Playwright web-server configuration make local development and browser checks reproducible.

## Remaining limitations

This is a bounded synthetic research prototype, not a physically validated soil transport simulator or chemical detector. There is no real sample collection, hardware integration, real-field calibration or deployed multi-user service. The Gaussian posterior assumptions and fixed noise are simplified, narrow hotspots can be missed, and eight held-out fields per ceiling are too few for broad performance claims. Browser request abort cancels obsolete UI work; bounded server computations are short and do not implement background-job cancellation.

No Git repository was created, no commit made, and no push performed. Publication awaits user confirmation. The recovered copy is in the active workspace; the disconnected original Mac Coding Projects folder has not been changed.


## Warm Documentary interface redesign — 2026-10-26

The release copy now has a field-notebook layout, using upstream Warm Documentary CSS and finite fade/lower-third clips. The sidebar, promotional hero, rounded cards and green glow were replaced by a geographic reconstruction, margin notes, specimen ledger, surface study and separate evaluator notes. Reduced motion disables all decorative animation and automatic replay while preserving manual acquisition. Scientific source, model metadata, observations, numeric results and tests were not modified; no training or benchmark was rerun. See `design.md` and `THIRD_PARTY_NOTICES.md`.

TypeScript/Vite build succeeds locally. The Mac loopback server starts, but headless Chrome exits under this execution environment. Updated screenshots, browser assertions and visual inspection are not claimed complete locally. Three browser scenarios and a Linux GitHub Actions workflow are provided to run acquisition/replay/reveal/rotation/export/policy/input-limit checks, 390px reflow and reduced motion, capturing authentic screenshots as workflow artifacts. No commit, push, deployment or repository-visibility change was made during this redesign.
