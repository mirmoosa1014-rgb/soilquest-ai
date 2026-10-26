# Design record — a field-survey notebook

## Reference and license

This interface adapts **Warm Documentary**, style id `documentary`, library `motionstyle_documentary`, from the Motion Graphic Style Library at revision `ab7faf2be3e17350f5c6c7e78dfb53d1792ae9cc`. The reference is `catalog/documentary.md`; its generated `documentary.css` is copied without modification into `frontend/src/motion-theme.css` and imported by the app. The upstream MIT notice is included in `THIRD_PARTY_NOTICES.md`.

The stylesheet consumes the upstream palette, typography and clip duration/easing variables rather than adding an independent theme. Core colors are umber `#140E0A`, warm ivory `#F3EBDF`, amber `#E0A15A`, dim text `#B6A494`, and rust `#8C3A2F`. Headings and body text use Iowan Old Style / Palatino / Georgia; quiet observation labels use SF Mono / system monospace. The 2px maximum radius, no shadows, no glow and almost absent chrome follow the reference. Continuous scientific colors interpolate the declared umber/rust/amber/ivory tokens. Data scale limits remain 0–130 synthetic mg/kg and 0–45 mg/kg posterior SD.

## App-specific interpretation

The new interface is a journal with a masthead, geographic reconstruction, margin notes, observation lower third, actual sample ledger, 3D surface study and evaluator’s notes. It replaces the earlier dashboard sidebar, promotional headline, neon greens, rounded cards and metric tiles. Fields and real evidence lead the page; there is no background video, stock image, invented landscape or marketing illustration.

The upstream reference describes narrated video and advises against charts and isometric blocks. This scientific application deliberately retains its geographic maps, paired comparison table and existing 3D data representation: removing them would hide evidence and break the task. The 3D mesh is the actual posterior concentration projection, not decorative isometric artwork. Chart extents, units, observations, policy outputs and benchmark numeric artifacts are unchanged. The map now explicitly labels metre coordinates and northing increases upward; this changes screen orientation only, not scientific data. Node-centered cell color areas are clipped at the 0–100 m boundary, while routes and sample marks use their actual x/y coordinates.

The video's 1920 × 1080 frame and 96px safe margin are adapted to a responsive document: desktop notebook width is capped, wide screens use a 96px inset, and mobile reflows the survey and margin notes into one column. Tables have their own scroll containers. Maps keep their aspect ratio and explicit legends.

## Motion clips and accuracy

- `fade_in`: 0.6 s, `cubic-bezier(0.65, 0, 0.35, 1)`, opacity 0 → 1 on the opening notebook heading.
- `lower_third`: 0.7 s, `cubic-bezier(0.16, 1, 0.3, 1)`, y 16px → 0 on the observation caption; opacity also follows `fade_in`.
- No stagger, spring, bouncing, count tween, stroke draw-on, loop or background drift.

`ken_burns` and the video's continuous idle motion are **not applied**. A data map must not zoom, drift or subtly change perceived size while being compared. Maps, mesh surfaces and all numbers update directly to a real requested simulation snapshot. Only the user-controlled view-angle slider rotates the data projection. Playback advances genuine acquisition states, rather than interpolating numeric values. Under `prefers-reduced-motion: reduce`, all animation and smooth scrolling are removed, automatic replay is disabled, and acquisition plus the observation slider remain available.

## Scientific freeze

This redesign changes frontend presentation and documentation only. Backend, sampler, GP, models, observations, numeric results and scientific tests are frozen. No training or benchmark script was run. Original research figures and replay GIF remain evidence from the earlier scientific run; their numeric content has not been restyled or regenerated in this pass. Those figures retain their original scientific palette rather than being repainted without a verified graphics environment.

## Verification and current screenshot status

The TypeScript/Vite production build passes locally. This Mac session can start the loopback FastAPI server, but cannot launch headless Chrome; its browser process exits immediately. Accordingly **no updated local screenshot is claimed**, and historical screenshots are not presented as the new notebook design. The browser verification code is in `frontend/tests/workbench.spec.ts`.

For reproducible Linux verification and authentic updated captures:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
npm ci --prefix frontend
npm run build --prefix frontend
cd frontend
npx playwright install --with-deps chromium
npm run test:browser
```

Playwright starts the loopback API automatically. The three scenarios check acquisition, replay, policy selection, evaluator reveal, 3D rotation, JSON export contents, input limits, 390px page width and reduced-motion behavior. It writes `frontend/artifacts/notebook-desktop.png`, `notebook-hero.png`, `notebook-mobile.png` and `notebook-reduced-motion.png` only from real browser-rendered states. `animations: disabled` prevents screenshots of half-finished fades; it does not fabricate application values.

`.github/workflows/ui-notebook.yml` runs that procedure on Linux on pushes to `design/**` branches, through manual dispatch, or on a frontend pull request and uploads screenshots plus failure traces as `soilquest-notebook-browser-evidence`. No workflow was triggered, commit made or code pushed in this redesign session. Browser execution and visual inspection remain pending in an environment that can launch a browser. `PLAYWRIGHT_CHROMIUM_EXECUTABLE` and `SOILQUEST_PYTHON` optionally select installed browser/Python executables for local testing without hardcoding a machine-specific path into product code.
