# Camera/background investigation — 1–2 November 2026

## Result

Fixed presentation only. Real keyboard-driven Chromium/WebGL runs cover Mario and Kenney on `/play/1` and editor `T` test-play, plus controlled flat terrain, a physical ramp, long falls, held-jump springs, mushroom growth and window resize. **20 recorded trajectories, 11,538 rendered frames:** four original baselines, four patched sample trajectories and twelve patched fixture trajectories. No physics, replay, movement constants, contract or ABI changes.

## Proven causes

1. **Vertical camera policy and visual coupling.** `PlayScene` followed `playerSprite.x/y` with `startFollow(..., true, .15, .15, 0, TILE)`. A normal jump therefore moved the whole world: the baseline Mario `/play/1` jump changed vertical camera scroll by **120 world px**; Kenney changed it by **112.94 px**. The deadzone dimensions were multiplied by zoom even though Phaser consumes world units. Phaser follows target coordinates, **not its scale**; the coupling to the animation came from placing the target at the visual feet/padding offset (Kenney offsets vary by pose), rather than from Phaser reading sprite bounds.
2. **Swept collision bounds used as artwork geometry.** `syncSprite` positioned the feet at `hull.bounds.max.y` and calculated height from that AABB. Matter expands these bounds by velocity. In all four baselines, the actual 60 px physical hull had a measured bounds height of **60–80 px**; falling visual feet overshot the physical foot sensor by about **16 px**. This explains the changing character size/feet independently of camera movement. Physical head/foot sensors already exist and are stable.
3. **One render behind parallax.** Background phase ran at scene `POST_UPDATE`. Installed Phaser 3.90 applies follow, scroll rounding and bounds later in `Camera.preRender`; the renderer then emits the camera `prerender` event before drawing children. Every baseline background phase matches the **previous** camera scroll to approximately `6e-14`, while differing from the current rendered scroll by up to **2.695 world px**. This is a measured one-frame lag, not an asset reload.
4. **Two different rounding policies.** Phaser floors follow scroll when `roundPixels=true`, but disables `renderRoundPixels` at fractional zoom. `syncSprite` separately rounded position and padding. This quantized camera feedback and character movement at different stages. The fractional zoom itself is valid.
5. **Fractional TileSprite backing dimensions.** Backgrounds repeatedly received non-integral sizes and scale setters. Phaser compares those logical sizes with integral canvas backing dimensions on every draw. The patch uses integral overscan dimensions, updates size/scale only when changed and accounts for camera zoom origin and overscan in phase.

### Ruled out

The baseline Mario `/play/1` recording contains **56 HUD events**, with **zero** Phaser resize events, canvas width/height mutations or canvas replacements. Pack/editor recordings confirm the same. Current React pages do not subscribe to `play:hud`; `PhaserGame` creates its game in a mount effect with a stable ref dependency. There is no application `ResizeObserver`. Real pause/resume state changes, editor transitions, zoom and two window resizes preserved the game/canvas identity. Resize correctly changes backing dimensions. Background texture uploads measured during movement were **zero** before and after: do not describe this as textures being reloaded every frame.

## Patch

- `web/src/game/render/PlayerCameraTarget.ts`: a separate physical x / feet-baseline reference. Grounded slopes and landings update the baseline. Ordinary jumps stay within a viewport-relative vertical band; six physics steps of vertical velocity look-ahead start tracking earlier for fast springs/falls. Short viewports shrink the band.
- `PlayScene.ts`: follow that reference, use a 3-tile horizontal / 1-tile vertical world-space deadzone, place the player near 70% viewport height, and preserve the existing ~.15 horizontal response at 60 Hz with elapsed-time-adjusted lerp. Vertical response is .2, rather than adding heavy smoothing. Follow and sprites use continuous coordinates under the same camera transform. Sprite height and feet use physical sensors; authored padding and squash/stretch remain visual.
- `render/background.ts`: use the camera `prerender` event, after follow/clamp, including editor cameras without a follow target. Maintain viewport cover with integral overscan. Phase is equivalent to a world-anchored layer under Phaser's centre-origin zoom:

  `tilePositionX * tileScale = renderedScrollX * factor + (cameraWidth - spriteWidth) / 2`

  The overscan correction similarly fixes the vertical visible-top phase. Remove the listener on scene shutdown.

**Measurement detail:** camera logical width can be fractional (e.g. `1049.609375`) while canvas backing width is integral (`1049`). Resize probes capture both. Comparing phase against backing width instead of camera width produces a false 0.3046875 px error; the assertions use the actual logical viewport.

## Browser verification

`browser-checks.txt` is the output of `python3 docs/screenshots/camera-fix/assert-evidence.py`:

```text
PASS 16 real-browser trajectories; physical follow, ordinary-jump baseline, same-frame parallax, slopes, vertical travel, forms, resize and canvas identity
```

- All four controlled ordinary jump/land cycles: **exactly 0 vertical camera-scroll change**, with physical feet moving more than 200 px.
- All patched trajectories: current-render background phase error below `1e-8`; observed errors are around `1e-13` or smaller.
- Movement without resize: **0 background size/scale calls**, **0 internal backing resizes**, **0 main canvas replacements**. Resize performs one necessary backing update per layer per viewport change.
- Ramp: actual Matter static triangle, collision category `solid=4`, rendered gold for inspection. Real right/left movement traverses the incline and its changing floor baseline. This is a validation fixture, not a new editor element.
- Vertical travel: Mario fall camera moves **1239.06 px**, held-jump spring **630.21 px**; Kenney editor fall **714.11 px**, spring **586.48 px**. Physical feet remain within the viewport throughout these recordings.
- Mushroom pickup driven by movement changes the physical hull from 60 to 120 px. Growth animation and subsequent jump do not pull the camera vertically on the flat fixture.
- Resizes: 1440×1000 → 1100×850 → 1440×1000 in every pack/mode. Backgrounds cover every measured viewport and phase remains anchored.
- Return from test-play with `T`, click **Zoom in**, middle-drag pan: zoom `.65625 → .75`; one background camera listener; same game and canvas (`editor-return-zoom.json`).

An initial camera-only implementation without velocity look-ahead let the feet pass about 13 px below a 638 px viewport during a long fall. Its raw capture is retained in `initial-no-lookahead-fall.json.gz`. A failing regression and velocity look-ahead resolved it; final Mario maximum falling feet position is about 553 px. An initially overlapping spring spawn was corrected to start above the spring; final spring verification holds Space to exercise its full launch. Browser-harness startup/locator/screenshot failures were corrected and rerun; they are not counted as successful trajectories.

## Real command output

Commands ran inside each standalone package. Complete stdout is saved alongside this file; all four exited **0**.

```text
web: npm test
 Test Files  11 passed (11)
      Tests  50 passed (50)

web: npm run build
> tsc --noEmit && vite build
✓ built in 10.32s

game-core: npm test
 Test Files  7 passed (7)
      Tests  87 passed (87)

game-core: npm run build
> tsc -p tsconfig.json
```

Ten new focused regressions cover the actual sprite presentation consumer, background render phase/cover/resize/lifecycle, jump baseline, grounded slopes, sustained ascent/descent, fast vertical look-ahead and short viewports. `tests-red.txt` contains the original behavioral failures; `vertical-lookahead-red.txt` contains the fast-travel failure. `git diff --check` also passed.

## Evidence index

- [Before jump — Mario play](baseline-mario-play-jump.png) · [After jump](after-mario-play-jump.png)
- [Before jump — Kenney play](baseline-kenney-play-jump.png) · [After jump](after-kenney-play-jump.png)
- [Before — Mario editor test-play](baseline-mario-editor-jump.png) · [After](after-mario-editor-jump.png)
- [Before — Kenney editor test-play](baseline-kenney-editor-jump.png) · [After](after-kenney-editor-jump.png)
- [Physical ramp](verified-mario-play-slope-slope-up.png) · [Kenney ramp](verified-kenney-editor-slope-slope-up.png)
- [Long fall](verified-mario-play-fall-vertical-fall.png) · [Held-jump spring](verified-mario-play-spring-vertical-launch.png)
- [Mario resize](verified-mario-play-flat-resize-small.png) · [Kenney editor resize](verified-kenney-editor-flat-resize-small.png)
- [Editor zoom](editor-return-zoom.png) · [Editor pan](editor-return-pan.png)
- `metrics.json`: all per-phase summaries. `baseline-*.json.gz`, `after-*.json.gz`, `verified-*.json.gz`: full frame telemetry (camera scroll/pre-scroll, physical body/foot/bounds/velocity/mode, sprite position/scale/frame, canvas DOM/backing sizes/identity and background tile phases). Later probes also capture logical camera viewport and displayed sprite height.
- `trajectory.browser.js`, `fixtures.browser.js`, `run-browser.py`: reproduction harnesses using Playwright keyboard down/up, actual Matter and actual rendering. `assert-evidence.py` checks the saved observations independently. The pre-existing `probe.js`, `before*` files and original fixture were preserved.

To rerun: start Vite locally on 8080 and an isolated Playwright CLI browser session named `camera` (headed Chromium). Then, for example:

```sh
python3 docs/screenshots/camera-fix/run-browser.py --pack mario --mode play --kind flat
python3 docs/screenshots/camera-fix/run-browser.py --pack kenney --mode editor --kind spring
python3 docs/screenshots/camera-fix/assert-evidence.py
```

The runner defaults to a `rerun` label to preserve saved evidence; use `--label after` for sample trajectories or `--label verified` for fixture runs to replace their corresponding assertion inputs. Browser localStorage belongs to the isolated test profile.

## Limits and cleanup

Browser evidence is Chromium/WebGL desktop; Firefox, Safari, mobile and full Canvas-renderer gameplay were not exercised. Fractional zoom uses consistent subpixel transforms, not an integer pixel-art grid. Very short viewports must scroll during tall jumps to keep the player visible. Camera bounds still apply at level edges.

The existing API at 8787 rejected this test origin with CORS errors and the Hardhat RPC at 8545 was absent. `/play/1` therefore used its explicitly labelled sample fallback; chain/publishing behavior was outside this camera task. Those service errors were not altered. The Vite process and browser session started for this task were stopped; the pre-existing service on 8787 was left running. No commit or push was made.
