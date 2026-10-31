# RealmForge NSMBU demo pack

Nintendo property, used for a private educational class demo only; do not distribute publicly; Kenney CC0 pack remains the public-safe fallback.

This is a schema-1 pack at `/packs/mario/manifest.json`. It covers all 117 existing Kenney element IDs plus native terrain edges, pipes, used/hard blocks, Bullet Bill, P-switch and switch-block state helpers. All four themes use the New Super Mario Bros. U rendered style. No SMB1/SMB3/SMW pixel-art assets and no AI-generated artwork are included. Source attribution and download limitations are in [SOURCES.md](SOURCES.md). Every element-to-file mapping is in [COVERAGE.md](COVERAGE.md).

## Rebuild and verify

From this directory:

```sh
python3 -m pip install -r requirements.txt
npm run fetch
npm run build
npm run validate
npm run preview
npm run validate:registry
```

`fetch` restores the exact image/asset-metadata bytes listed in `sources.json` to the gitignored `assets/_downloads/mario/` directory, checks SHA-256, and uses immutable GitHub revisions or content-addressed Scratch image URLs. `build` slices only the checked-in `slicing.json`; it never searches the network. `validate` checks actual source crops, checksums, manifest paths, atlas rectangles, animation names, all legacy element IDs, and exact horizontal boundary texels for every background. `validate:registry` additionally uses the repository's existing `assets/node_modules/.bin/tsx` to exercise the real web registry; run `npm ci` in `assets/` if that tool is absent. The pack itself adds no npm dependencies. Pillow is the only build dependency (MIT-CMU/HPND).

`curate.py`, `upgrade-sources.py`, and `research-icons.py` record the initial curation/research workflow; they are not needed for a clean rebuild. `curate.py` can regenerate the crop config from the pinned source inventory. The two research helpers need research metadata in the gitignored raw directory; no executable code from those game projects is reused.

## Schema additions and scale

Existing schema-1 sections and original character animation names remain intact. These are the only added manifest **fields**:

| Field | Meaning |
|---|---|
| Pack `pixelArt: false` | Use linear filtering; do not round sprite pixels. |
| Pack `sourceTile: 64` | One tile in the full-resolution NSMBU terrain sheets is 64 source pixels. `tileSize` remains the existing 64px gameplay grid. |
| Entry `displaySize: {w,h}` | Artwork display dimensions in gameplay tiles; does not alter controller physics. |
| Entry `anchor: {x,y}` | Normalized origin. Characters/enemies use feet at bottom centre (`0.5,1`). |
| Theme `parallax: [{file,scrollFactor}]` | Back-to-front horizontally repeating layers. `y` is supported by the consumer but is not needed here. |
| Animation `frameRate` | Playback rate (already supported by schema-1's existing animation entries). |

Existing `note`, `source`, `pack` and `aliasOf` fields document substitutions/provenance. New map entries reuse existing entry shapes; no new schema version or rendering code is required. `ui`, `editor`, `sfx` and `music` retain the exact original CC0 entries with absolute `/assets/` references, so the existing public-safe pack must remain installed.

Terrain crops stay 64px. Larger native object rips (up to several hundred pixels per frame) also stay at their downloaded resolution. The first accessible mirror's player captures are **only 24–48px per pose**, and some secondary objects are 14–32px; they are not passed off as HD source captures. Runtime display metadata makes big Mario's visible idle art two 64px tiles tall. All character frames share a native canvas and bottom-centred feet, preventing pose-dependent scale and foot jitter. Images are trimmed/cropped/padded, never upscaled by the pack builder. At runtime the high-resolution terrain may be sharper than these lower-resolution character captures.

Playable big Mario is `characters.mario`. Optional small Mario is named `characters.mario_small`. The concurrently updated web registry currently prioritizes `mario_small` over `mario`; selecting the preferred big Mario requires the coordinator to change that ordering in its owned code. This pack supplies both forms and does not change the consumer. Native Luigi's available walk capture is `luigi_native_walk`. Original `green`, `pink`, `purple`, `beige` keys remain compatibility aliases; green maps to Luigi and the other three map to Mario. They do not imply extra Toad/Toadette rips.

## Backgrounds

There are 21 original full-height source layers: grass/overworld 7, desert 5, snow 6, castle 3. Native transparent margins preserve source vertical alignment. To make each output wide and provably seamless, the script appends a horizontally mirrored copy and repeats that native period until the image is at least 1536px wide. No background is AI-generated, painted, rescaled or replaced with a flat fill. This mirror-repeat treatment is a disclosed derivative of the ripped layers, not a claim that the output is an untouched Nintendo texture. It can produce symmetrical scenery; the contact sheet shows the result.

## Substitutions and remaining fidelity limits

| Requested asset | Delivered choice / limitation |
|---|---|
| Big Luigi, all poses | **Mario big colour variant**, not an authentic Luigi model capture. Real native Luigi walk is supplied separately. A complete authentic big Luigi pose set is still missing. |
| Mario fall | Late frames of the native jump capture, rather than a separately ripped falling cycle. |
| Small Mario | Supplied with all nine animation names. Toad/Toadette are not included. |
| Goomba | Native lower-resolution mirror walk and squashed captures. The larger alternate Goomba was fan vector art and was rejected. |
| Flyer | Native Koopa flight poses composited with native wings. These remain lower resolution than the upgraded walking Koopa. |
| Slime | Native Note Block art represents the high-friction terrain; gameplay semantics remain slime. |
| Crate | Native used/throw block; an authentic NSMBU crate rip was not found. |
| Pendulum | Chain Chomp ball plus separately supplied native chain link. |
| Chain bridge | Native rope-bridge plank; chain link is supplied separately. |
| Falling block | Native Donut Block. |
| Elevator / rotating platform | Native lift segment / seesaw deck reused for these mechanisms. |
| Double jump / dash | Native Super Acorn / Super Star. |
| Switch | Full-resolution ON/OFF switch and red solid/outline toggled blocks. The native P-switch animation is also included as a helper. |
| Larger object rips | Downloadable diffuse sprites are used directly; this asset-only pack does not recreate the console normal/bump-map lighting. Some objects can look flatter than the lit console render. |
| Theme variants | Authentic native top/edge/interior crops. Question blocks use the larger native animated block rip. Hard/used block helpers share the native used-block appearance in this version. |
| Game-specific ripper credits for the first mirror | Not supplied by that mirror; explicitly marked unconfirmed in SOURCES.md rather than invented. |

This is an asset-only delivery. It does not change `web/src`, gameplay physics, the original Kenney pack, or shared docs. The coordinator should update `docs/CHECKLIST.md` and `assets/CREDITS.md` when integrating, and verify the desired visual-to-collision relationship for the two-tile character. No files were staged or committed.
