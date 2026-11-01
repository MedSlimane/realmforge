# Goomba import — coordinator handoff

Prepared 1 November 2026. **Assets and manifest fragment are ready; the shared
manifest/build and gameplay renderer are deliberately unchanged.** Only
`assets/packs/mario/goomba-import/` and
`web/public/packs/mario/enemies/goomba-import/` were written. Originals in
`~/Downloads/realmforge-rips/` remain intact. No git add, commit or push.

## Source and accurate credits

Downloaded file:
`Nintendo Switch - Super Mario Maker 2 - New Super Mario Bros. U_ Enemies - Goomba (NSMBU).png`

SHA-256: `ba3f122c226d4ece1cfef057dc7b32d99c5eaf456d5cb7f0c3f6c7f8429f567b`.
The local `source/goomba-tsr-238649.png` is a byte-for-byte copy, **994×1249 RGBA**.
[TSR asset 238649](https://www.spriters-resource.com/nintendo_switch/supermariomaker2/asset/238649/)
identifies Nintendo Switch, Super Mario Maker 2, section **New Super Mario Bros.
U: Enemies**, uploader **DogToon64**. This is SMM2's NSMBU style, not a claim that
the image was ripped directly from the Wii U NSMBU release.

The sheet's actual text is:

> Goomba [NSMBU] from Super Mario Maker 2 ripped by DogToon64.
> If used, give credit to Nintendo.
> Credit to DogToon64 is optional, but would be nice.

Credit **Nintendo; ripped by DogToon64, The Spriters Resource asset 238649** in
shared `SOURCES.md` and `assets/CREDITS.md` when integrating. This is Nintendo
imagery, not CC0. The repository's private educational-demo restriction applies.
No dependency was added; the existing Pillow 12.3.0 dependency is MIT-CMU/HPND.
`provenance.json` records the original filename, hashes and prior still source.

## Sheet interpretation and crop recipe

The **full sheet** was inspected, including credits, all diffuse groups and the
blue/purple blocks interpreted as normal maps. There are **no action-name labels
or timing labels** on the image. Action names below are visual interpretations;
the neutral group names deliberately preserve uncertainty.

Coordinates are zero-based. Every diffuse cell is 120×106, at x = 2 + 122×column.
`recipe.json` records every row's y coordinate and cell count; `frames.json`
records all 62 exact source rectangles, opaque bounds, placement and RGBA hashes.
Read each group left to right, then top to bottom:

| Name | Source row starts / counts | Frames | Use |
|---|---|---:|---|
| `walk` | y=2 / 8; y=110 / 8 | 16 | Walk inferred from alternating feet/body sway |
| `source_group_b` | y=273 / 8; y=381 / 3 | 11 | Unlabelled action; preserve separately, no gameplay mapping |
| `source_group_c` | y=544 / 8; y=652 / 8; y=760 / 5 | 21 | Unlabelled action; preserve separately, no gameplay mapping |
| `stomp` | y=978 / 8; y=1086 / 6 | 14 | Flattened stomp/death inferred visually |

The stomp group **starts flattened**. No upright-to-squash transition was invented.
Normal-map blocks at y=218..270, 489..541, 868..975 and 1194..1246 are excluded,
as are the cyan grid and credit region. They are not extra colour-animation
frames. The sheet's transparent pixels are used directly; no colour-key removal,
recolouring, lighting reconstruction, resampling, generated art or interpolation.
Source edge pixels and partial alpha are retained without smoothing.

Each cell is trimmed only to its alpha bounds, then copied at native resolution
onto a **120×100 transparent canvas**. Its feet end at y=100, with horizontal
alpha bounds centred to the nearest integer pixel. Per-frame translation is
intentional to normalize feet/centre; it is not scaling. All frames use anchor
`{x:0.5,y:1}`. Atlas frames are untrimmed/unrotated, with two transparent pixels
of gutter. Runtime PNGs preserve exact source RGBA, including partial alpha.

The 16-frame walk uses an authored **12 fps**, repeat -1 (1.333 seconds).
The 14-frame stomp uses an authored **24 fps**, repeat 0 (0.583 seconds).
Original timing was not supplied. The two unconfirmed groups use 12 fps only
for inspection and are absent from the runtime animation map. GIF previews round
to centiseconds (80/40 ms, respectively); the PNG atlas and manifest are the
runtime authority. GIF colour quantization/opaque preview background are solely
presentation limitations, not changes to the RGBA assets.

## Resolution tradeoff — animation instead of the larger still

| Asset | Native opaque pixels | Presentation at a 64px gameplay tile |
|---|---|---|
| Existing original Wiki render | 208×243 | Existing slicer downsamples to 104×122 |
| Existing served still | **104×122** | Existing manifest stretches to **64×64**, x=0.6154 / y=0.5246 |
| New walk frames | **81..85 × 94..100** | At uniform 0.64×: **51.84..54.4 × 60.16..64** |
| Unconfirmed group B | 82..85 × 93..96 | At uniform 0.64×: 52.48..54.4 × 59.52..61.44 |
| Unconfirmed group C | 81..85 × 92..98 | At uniform 0.64×: 51.84..54.4 × 58.88..62.72 |
| New flattened stomp frames | **105..120 × 38..44** | At uniform 0.64×: **67.2..76.8 × 24.32..28.16** |

Opaque means alpha > 0, matching the current pack audit convention. Walk envelope
85×100 has **18.3% fewer horizontal and 18.0% fewer vertical pixels** than the
current 104×122 output (33.0% less envelope area). The full old source is larger
still. The new sheet supplies genuine gameplay motion and stomp imagery with a
flatter rendered appearance; it is **not a higher-resolution replacement**.

The common 120×100 canvas includes the genuinely wider stomp. `displaySize`
**{w:1.2,h:1}** maps that canvas to **76.8×64** at a 64px tile, applying uniform
0.64× scaling and displaying the upright walk at about **54.4×64** maximum.
The gameplay collision footprint remains one tile. The small transparent walk
margins are not claimed as extra native resolution. Do not enlarge frames to
104×122 or stretch this canvas to 64×64 to disguise the tradeoff.

`comparison.png` shows old/new native pixels at 1:1. `contact-sheet.png` shows
all 62 crops at 1:1, with feet guides. `preview.gif` plays all groups in source
order. The GIF is a review artifact, not a game texture.

## Integrating the fragment

`manifest-fragment.json` contains only these four entries:

- `elements.walker` and `enemies.walker`: both existing runtime entries.
- `elements.goomba` and `enemies.goomba`: explicit descriptive aliases.

All four use the same **mario-walker** texture, initial `goomba_walk_00` frame,
common anchor/size and walk/stomp definitions. The importer also scans the current
manifest for any further entry using `mario-walker` and fails if uncovered. The
current manifest has only `elements.walker` and `enemies.walker` as existing
Goomba/walker aliases. `flyer`/Paragoomba is a different enemy and stays unchanged;
`editor.palette_walker` is a separate editor icon, not a runtime Goomba alias.

After the normal shared pack build, merge **entry-by-entry**:

```python
for section in ("elements", "enemies"):
    manifest.setdefault(section, {}).update(fragment[section])
```

Do not replace either entire section, and do not use a shallow root-level merge.
The relative paths resolve against the existing `/packs/mario/` baseUrl. Public
output is `enemies/goomba-import/atlas.{png,json}`, with 62 exact frames;
`goomba.png` is the first walk frame and `frames/*.png` are standalone inspection
copies. No old public enemy file needs deletion. Unknown groups are packed but
are not assigned to invented gameplay actions.

The existing shared builder will restore its old `walker` manifest entries on a
subsequent build. Coordinator must either merge the fragment **after each pack
build** or add a scoped hook to that builder; no shared hook was added here.
`verify-registry.ts` exercises the real web registry with this merge **in memory**:
one atlas is queued, URLs/anchors/sizes and animation counts match, aliases
resolve identically, and every unrelated manifest entry stays unchanged.

## Remaining runtime work / unresolved blockers

1. Shared manifest and builder integration is pending the coordinator's merge.
   This task does not claim the new Goomba is already active in gameplay.
2. `game-core/src/elements/display.ts:106` (`stompVisuals`) applies an additional
   scaleY×0.25 tween and destroys/fades the ghost over **220 ms**. With this
   fragment it would further flatten already-flattened genuine art and truncate
   the 583ms sequence after roughly 5 frames. Coordinator should adjust that
   sourced-animation path to preserve shape and allow animation completion;
   this runtime path is outside ownership. No runtime code was edited.
3. Original animation rates and semantic names for groups B/C remain unverified.
   No labels were fabricated to close these gaps.
4. This sheet contains no winged Paragoomba cycle. Unrelated enemies and the
   broader character/fidelity gaps in RESOLUTION_REPORT.md remain open.

Coordinator checklist update: record the downloaded SMM2 NSMBU Goomba source,
16 genuine walking frames and 14 distinct flattened stomp frames, smaller native
resolution and pending runtime stomp correction. Keep **Exact NSMBU fidelity**
open. Shared CHECKLIST.md and credit files were intentionally not edited.

## Rebuild and actual verification

Run from the repository root, using existing installed dependencies:

```sh
python3 assets/packs/mario/goomba-import/build.py
python3 assets/packs/mario/goomba-import/build.py --verify-only
assets/node_modules/.bin/tsx assets/packs/mario/goomba-import/verify-registry.ts
(cd web && npx tsc --noEmit)
```

`build.py` is offline and needs only the pinned local source copy and baseline
snapshot. It writes exclusively inside this import's two owned trees, never the
shared manifest/build/checklist. The external original is optional for rebuild;
if present, validation checks its unchanged hash. `sha256.json` records every
source/recipe/script and generated runtime/review output, except itself and the
human handoff/log files. Verification independently reconstructs every crop from
the source and compares exact decoded RGBA against standalone PNGs and atlas
rectangles, checks bounds/non-overlap, feet, all 62 globally unique crops,
transparent/header-free content, references, aliases and GIF frame count.

Actual commands, exit codes and output, including a byte-identical second build,
are recorded in `VALIDATION.txt`. No full pack build or validate was run: those
mutate shared paths and the current global character-fidelity gate is already
known incomplete. TypeScript was checked without emission. No whole-game visual
verification is claimed before coordinator integration.
