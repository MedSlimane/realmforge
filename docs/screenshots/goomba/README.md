# Goomba gameplay integration — 1 November 2026

The downloaded Nintendo Goomba atlas is active in real gameplay. Nintendo;
ripped by DogToon64, The Spriters Resource asset 238649 (SMM2's NSMBU style).
Private educational demo only. No model preview is a gameplay texture.

## Files and behavior

- `assets/packs/mario/scripts/build.py` builds the pinned Goomba source first,
  then applies the four fragment entries as the final entry-level manifest merge.
  The build verifies staged objects in a disposable directory and compares pinned
  source bytes, decoded PNG RGBA and atlas bytes with published files. This
  prevents PNG encoder changes from dropping completed object animations. Existing
  inspection trees and legacy walker files survive cleanup.
- `web/public/packs/mario/manifest.json` changes only `elements.walker`,
  `elements.goomba`, `enemies.walker` and `enemies.goomba`; see `manifest-diff.json`.
- `web/src/game/render/artwork.ts` preserves the walker's feet-normalized canvas
  instead of independently trimming and stretching each pose. Its test exercises
  the real preparation pass; pack tests check every runtime frame's source aspect.
- `game-core/src/elements/display.ts` preserves facing and feet, plays the complete
  stomp once, destroys on its actual animation completion and supplies a
  duration-based safety timeout. There is no extra squash/fade for this already-flat
  art. The static Kenney path retains its 220 ms squash fallback. Tests cover
  authored scale, feet, completion, timeout and static fallback. Physics is unchanged.
- `docs/CHECKLIST.md`, `assets/CREDITS.md`, and pack `SOURCES.md` record completed
  Goomba motion, accurate Nintendo/DogToon64 credits and missing character clips.

## Actual browser evidence

`walk.png`, `stomp.png`, and `walk-stomp.gif` are actual browser captures from
Chromium 153 / Phaser 3.90.0 on `http://127.0.0.1:8080/play/1`. The outer React
header retains the sample's “Frozen Pendulums” name. The actual PlayScene level is
`fixture.level.v1.json`, loaded through the existing development scene handle;
`browser-evidence.json` includes that exact level and real physics frame samples.
No physics body, player position, collision rule or animation clock was modified.

After starting the normal UI run, `record-browser.js` restarts PlayScene with this
fixture and sends only ArrowRight and Space keyboard input. The unchanged Matter
runtime detects the falling player contacting the walker, removes its collision
body, and creates the stomp presentation. No `activate()`, `stompVisuals()`,
`finish()`, EventBus finish emission or synthetic animation completion is called.
Listeners only observe real postupdate/animation/destroy events.

Recorded results (`browser-summary.json`):

- All **16 distinct walk frames** and **14 distinct stomp frames** were observed.
- Every observed Goomba scale was **0.64 × 0.64**; origins were **(0.5, 1)**.
- Configured stomp duration: **583.333 ms**. First observed stomp frame to actual
  completion: **586.9 ms**, then the ghost was destroyed. Player ended alive/idle;
  the enemy was disabled and no Goomba sprite remained.
- GIF: **8 real canvas-area browser screenshots over 1.66 seconds**. Raw PNGs and
  capture timestamps remain in `capture-frames/` and `browser-evidence.json`.
  Pillow only assembled the screenshots; it did not generate animation frames.
  This sparse GIF is visual evidence, not the source/runtime animation authority.

`browser-console.txt` records the real limitations: localhost API/RPC connection
refusals and WalletConnect remote configuration/telemetry failures. The local
fixture and Goomba atlas rendered successfully. Server-signed results and on-chain
settlement were outside this visual check; no course clear is claimed.

To repeat, start `npm run dev -- --host 127.0.0.1` in `web`, open a Playwright CLI
session named `goomba` on `/play/1`, using the installed Chromium executable, then
run `playwright-cli --session goomba run-code --filename docs/screenshots/goomba/record-browser.js`.
The script uses this checkout's absolute path and returns the observation JSON.
The task's development server and owned browser session were stopped afterward.

## Commands and real outputs

Commands run from repo root unless another directory is stated. Each log contains
actual stdout/stderr. Builds and tests were rerun after their relevant code changes.

| Command | Exit / result | Full output |
|---|---|---|
| `python3 assets/packs/mario/scripts/build.py` | 0; 398 elements, 9 character keys, 6 enemies, 4 themes; source-first + final Goomba merge | [pack-build.txt](pack-build.txt) |
| `python3 assets/packs/mario/scripts/test-validation.py` | 0; **19 tests**, including two real rebuilds, preservation, PNG encoding and native-aspect regressions | [pack-tests.txt](pack-tests.txt) |
| `python3 assets/packs/mario/goomba-import/build.py --verify-only` | 0; 76 pinned input/output hashes; 62 exact RGBA crops, 16 walk + 14 stomp; aliases | [import-validation.txt](import-validation.txt) |
| `assets/node_modules/.bin/tsx assets/packs/mario/goomba-import/verify-registry.ts` | 0; one atlas, aliases, sizes/anchors, animation definitions; this supplied probe performs an in-memory merge | [import-validation.txt](import-validation.txt) |
| `assets/node_modules/.bin/tsx assets/packs/mario/scripts/validate-registry.ts` | 0; actual final manifest, 400 loader records, all 118 legacy IDs, four layered themes | [pack-registry.txt](pack-registry.txt) |
| `cd game-core && npm test` | 0; **87 tests / 7 files** | [game-core-tests.txt](game-core-tests.txt) |
| `cd game-core && npm run build` | 0; TypeScript build | [game-core-build.txt](game-core-build.txt) |
| `cd web && npm test` | 0; **40 tests / 8 files** | [web-tests.txt](web-tests.txt) |
| `cd web && npm run build` | 0; includes `tsc --noEmit`, Vite production build | [web-build.txt](web-build.txt) |
| `python3 assets/packs/mario/character-model-import/validate.py` | 0; three extraction tests; original/extracted hashes, 24 DAE models, 18 stills, no animations | [model-validation.txt](model-validation.txt) |
| `/tmp/realmforge-character-model-venv/bin/python assets/packs/mario/scripts/validate.py` | **1**; staging source/pixel checks pass, then existing PNG byte-identity publication check fails | [pack-validation.txt](pack-validation.txt) |

The optional full pack validator regenerates object PNGs into `integrated/` and
compares compressed file hashes with previously published PNGs. Exact decoded RGBA
matches, but encoder-dependent bytes differ. Its failure is retained here, not
reported as a passing full validation. The focused builder now validates current
staging in a temporary directory and verifies exact RGBA/atlas content without
rewriting reviewed files; the 19-test suite covers acceptance of encoding-only
changes and rejection of even one changed RGBA pixel. Unrelated encoder-only
changes produced by the verification commands were restored to their pre-task bytes.

## Preservation and remaining gaps

`preservation.txt` verifies all **214 pre-existing uncommitted import/model files**
remain byte-for-byte unchanged. Completed object art/FX, every unrelated manifest
entry, old walker files, aliases and model previews are retained. No files were
staged, committed or pushed. No contracts, movement constants, collision bodies,
replay logic or physics runtime were edited.

Goomba's action names are inferred; **12 fps walk / 24 fps stomp are authored**.
Unlabelled sheet groups B/C are inspection-only. The animated walk's maximum opaque
85×100 envelope is smaller than the old 104×122 still; no resolution upgrade is
claimed. Paragoomba and the broader exact-fidelity gaps remain open.

The Nintendo/DogToon64 Mario/Luigi downloads contain rigs and textures but **zero
original animation/clip/channel/sampler elements across 24 DAE files**. Their 18
orthographic bind-pose previews remain inspection evidence only, outside the runtime
manifest. Compatible original timed skeletal clips and a verified animation evaluator
are still required. Existing short player cycles, Wii fallbacks and missing poses
also mean the character-fidelity gate remains unresolved independently of the full
validator's earlier PNG encoding failure.
