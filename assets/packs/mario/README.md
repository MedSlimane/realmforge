# RealmForge NSMBU demo pack

Nintendo property, for the team's private educational class demo only. Never publish this pack or make a repository containing it public. Kenney remains the CC0 fallback. No AI-generated art, Nintendo executable code, ROMs or keys are included.

The high-resolution pass removes all **50 baseline scale violations**: every manifest sprite and animation frame is now at or below **1.25×** at `displaySize × 64` pixels. See [AUDIT.md](AUDIT.md) for every before/after entry and current animation frame, and [PREVIEW.png](../../../web/public/packs/mario/PREVIEW.png) for the contact sheet. A scale pass does **not** imply complete exact-game or exact-pose fidelity: the remaining exceptions below are substantive.

## Rebuild and verify

```sh
python3 -m pip install -r requirements.txt
npm run fetch
npm run build
npm run preview
npm run validate
npm run validate:registry
```

Run these from `assets/packs/mario/`. Pillow (MIT-CMU/HPND) is the only build dependency; there are no new npm dependencies. `fetch` restores and SHA-256-checks the exact source images in `sources.json` into gitignored `assets/_downloads/mario/`. GitHub images are pinned to immutable commits; Scratch images are content-addressed. Wiki URLs are mutable upstream, so the recorded checksum fails on changed bytes rather than silently adopting them. `build` is offline and reads only `slicing.json`; a clean fetch/build reproduces the output. It deletes obsolete generated pack files, retaining `PREVIEW.png` until `preview` regenerates it.

`validate` checks source hashes, crop bounds, source downsampling, legacy coverage, manifest files, every animation reference, every sprite/frame's display scale, 47 autotile masks per theme, two-pixel atlas extrusion, background seams and the 25 MB pack budget. It regenerates `AUDIT.md`. `validate:registry` exercises the actual web registry using the existing `assets/node_modules/.bin/tsx`; install the existing `assets/` package if needed.

`curate.py`, `upgrade-sources.py`, `research-icons.py`, `curate-hires.py`, `curate-character-fallbacks.py`, `complete-autotiles.py` and `lock-hires-sources.py` are historical/research curation helpers, **not clean-build prerequisites**. The final, checked-in `slicing.json` is authoritative. They require research metadata in the ignored cache; build/fetch/validate do not.

## Manifest and shared API

Schema stays **1**. Existing sections, IDs, paths and animation names remain compatible. Additions use the existing entry shape (`texture`, `path`, `width`, `height`, optional `atlas`, `image`, `frame`, `animations`, `displaySize`, `anchor`, `note`, `source`). `pixelArt: false` requests linear filtering, `sourceTile: 64` records the terrain source grid, and `tileSize` stays 64. `ui`, `editor`, `sfx` and `music` still reference the untouched public-safe `/assets/` pack.

- `characters.mario` / `characters.mario_small`: big and small forms.
- `characters.luigi` / `characters.luigi_small`: genuine Luigi, including his different head/body proportions; **no Mario recolouring**.
- Each form exposes `idle`, `walk`, `run`, `skid`, `jump`, `fall`, `crouch`, `wallSlide`, `dead`; walk/run have at least three frames. All forms use one fixed native canvas and bottom-centred feet. Idle art is 120px big and 60px small; a taller jump extends above that without moving the feet. Pose authenticity caveats follow below.
- `green` aliases Luigi; `pink`, `purple`, `beige` alias Mario. `luigi_native_walk` remains a compatibility alias of the genuine Luigi atlas. These are not extra characters.
- `items.mushroom` and `elements.mushroom` are identical Super Mushroom entries. Static official NSMBU artwork; no invented two-frame animation. The `mushroom` gameplay behavior belongs to game-core.
- `elements.seesaw`: 300×30 output deck (five native 60×60 NSMBU mushroom-seesaw segments, each downsampled to 60×30), displayed 320×32. `elements.seesaw_pivot`: native separate 42×42 pivot, displayed 48×48. Both are real NSMBU imagery. Render the pivot beneath the plank and rotate only the plank. The rotating-platform helper reuses the same deck.

## Terrain variants and pit edges

The old `left`, `right` and `fill` crops selected dark underside/slope cells. These are now mapped to the actual side and interior cells. Each original 64px source cell contains **60×60 content plus 2px repeated-edge source padding**. Standalone PNGs use the 60px content at display size 64px (1.067×); no source art is enlarged during the build.

Every theme supplies flat element names `${theme}_${variant}`, so existing consumers can resolve variants without a schema change:

| Variant | Intended use |
|---|---|
| `top_left`, `top`, `top_right` | Exposed upper corners/surface |
| `left`, `fill` (`inner` alias), `right` | Vertical exposed sides and interior |
| `bottom_left`, `bottom`, `bottom_right` | Exposed underside row |
| `inner_top_left`, `inner_top_right`, `inner_bottom_left`, `inner_bottom_right` | Concave corners around a missing diagonal neighbour |
| `pillar_top`, `pillar`, `pillar_bottom` | One-column vertical island |
| `single_left`, `horizontal`, `single_right` | One-row horizontal island |
| `single` | Isolated one-tile island |
| `mask_N` | Full 47-mask blob topology, including multiple simultaneous concave corners |

For `mask_N`, cardinal bits are N=1, E=2, S=4, W=8; diagonals are NE=16, SE=32, SW=64, NW=128. A diagonal bit is valid only if both adjacent cardinal neighbours exist. The 47 legal masks are assembled from native **30×30 quadrant crops**, without painting or enlarging art. `ground` aliases `top`.

`themes[theme].variants` also exposes the named entries. Additive `themes[theme].autotileAtlas` points to `tiles/<theme>/autotiles.{png,json}` with all named and mask frames. Atlas cells are 64×64; each frame rectangle is the inner 60×60 at offset (2,2), with **two exactly duplicated edge texels on all four sides**. Render from that rectangle, never include the gutter in the displayed content. Existing `themes[theme].path` and numeric `tiles` mappings keep their legacy 64px layout; they do not silently change to a padded sheet.

## Remaining provenance and pose limitations

| Asset | Current delivery / remaining exception |
|---|---|
| Big Mario | Credited NSMBU raster captures from PolskyGamer's collection, extracted from embedded PNGs without tracing the SVG wrapper. Large frames are downsampled to normalize pose scale. Its death cycle uses the separately labelled NSMBU death captures in project 829940955. Source collection mixes lighting/view angles, visible in the preview. Distinct fall frame is included. |
| **Luigi big + small** | **Authentic NSMB Wii captures**, shared by PolskyGamer, used as a same-style fallback. A full NSMBU-only high-resolution pose set was not found. Original ripper is not identified by this collection. This does **not** satisfy the exact NSMBU-provenance request. |
| **Small Mario** | **NSMB Wii captures**, credited by PolskyGamer to **Keira Sanchez**. Same-style fallback; exact NSMBU-only HD poses remain missing. |
| Luigi skid | A native run-transition pose, not a separately ripped braking pose. All nine animation keys exist, but exact skid art remains missing. |
| Wall-slide | Holds the native wall-jump/wall-contact capture. A distinct sliding loop was not found. |
| Big Mario crouch / skid | Native captures chosen for these actions; lighting/angle differs from idle. |
| Slime | Native green NSMBU mushroom-platform tile represents the high-friction surface; no genuine NSMBU slime/jelly rip was found. The Note Block substitute is removed. |
| Crate / pendulum | Authentic NSMBU wooden box and spiked pendulum ball; previous throw-block/Chain-Chomp substitutions are removed. Chain link remains a separate entry. |
| Goomba / flyer | High-resolution native NSMBU Goomba / Paragoomba stills. They replace lower-resolution captures; genuine high-resolution animated walk/stomp/fly cycles remain unavailable. Static animations do not manufacture motion. |
| Coin / big coin | Official NSMBU coin artwork plus native Star Coin; static. `coin_side` uses one native frame of the wiki coin capture. |
| Spring | Native NSMBU springboard still. `spring_extended` currently shares the still; an authentic large extended pose is missing. |
| Checkpoint / goal | Native NSMBU editor renders. Activated checkpoint and goal-wave helpers share their base appearance; state-specific large captures remain missing. |
| Locked door | Native closed door at adequate resolution; a distinct high-resolution lock overlay is not supplied. |
| Blocks | High-resolution official artwork from the NSMBU gallery. The gallery explicitly identifies brick/used artwork as originating in NSMB Wii and ? Block artwork in NSMB; Nintendo reused it for NSMBU. These are perspective promotional images, not claims of untouched gameplay texture rips. |
| Backgrounds | 21 native layers remain. Each layer is mirrored and repeated horizontally to make matching boundary texels, with no upsampling. The disclosed treatment can produce symmetrical scenery. |
| Source lighting | Diffuse sprites/editor renders do not recreate the original console normal-map lighting. |

Source URLs, credits, rights and exact SHA-256 values are in [SOURCES.md](SOURCES.md) and `sources.json`. Every mapping is in [COVERAGE.md](COVERAGE.md). This asset-only delivery modifies no game physics, web renderer, shared checklist or shared credits. The coordinator owns integration updates to `docs/CHECKLIST.md` and `assets/CREDITS.md`.
