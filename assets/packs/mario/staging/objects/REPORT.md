# Object-art handoff — 31 October 2026

This pass is partial: authentic available frames are staged, unavailable states are
listed below. All changes made by this agent are in `assets/packs/mario/staging/objects/`
and ignored `assets/_downloads/objects/`. No manifest, build script, web/public,
AGENTS.md or checklist was edited; no git add/commit/push was run.

## Integration contract

`objects.json` is a **staging descriptor**, schema 1, with `elements` and `fx` maps.
Every entry contains the requested `manifestKey`, `anims`, `anchor`, `displaySize`
(in tiles, 64px per tile), and `source: {url,game,ripper,method}`. All PNG paths are
relative to this staging directory. Entries also explicitly identify still states
and unavailable animations. `source-lock.json` pins source hashes, source-frame
indices, crops, exact decimation, padding and output hashes.

**The characters agent must copy/publish or atlas these staging frames.** The current
`integrate_staged` implementation in the concurrently edited build script appears
to require already-published web/public paths. That assumption conflicts with this
agent's staging-only ownership and with the user's handoff instruction. This
agent has deliberately not written web/public. Please adjust the owning integration
code to consume these staging paths and `anims`; do not directly merge this descriptor
as a runtime manifest. This integration issue is not a failed asset validator.

For each actual sequence, preserve source order. Keep still states as one-frame
states, and do not invent missing names. P-switch GIF durations vary; they are
preserved in `frameDurationsMs`, and its `frameRate` is only the average. Other
Scratch presentation rates are chosen rates, explicitly not verified original clocks.

Use the existing runtime IDs: `pswitch` is the existing pack P-switch entry
(request terminology `p_switch`), `switch` is the ON/OFF switch,
`falling_block` is the donut, and `saw` is the grinder. No game-core IDs are added.
`switch_block` supplies red solid/dotted and blue solid/dotted still states.

`fx.brick_debris.anims.piece_0` through `piece_3` are independent particle texture
variants, **not four temporal frames**. The renderer should select one per particle.
`fx.coin_pop` is a real spinning coin sprite: upward travel is renderer movement,
not a captured pop trajectory. `fx.star` is a real Super Star wobble sprite usable
as a decorative effect; it is not a claimed invincibility-particle texture.

## Delivered

| Entry | Actual delivered source states |
|---|---|
| `elements.spring` | Native normal-state still only |
| `elements.checkpoint` | Native inactive checkpoint still only |
| `elements.goal` | Native pole + Mario flag still only |
| `elements.question_block` | 16 native question-symbol scroll frames; authentic used-state block still |
| `elements.brick` | Authentic native Mega Block still, displayed at one tile |
| `elements.pswitch` | Genuine 12-frame SMM2 NSMBU highlight cycle |
| `elements.switch` | Genuine ON and OFF stills |
| `elements.switch_block` | Red solid/dotted and blue solid/dotted stills |
| `elements.falling_block` | Native donut still |
| `elements.conveyor_belt` | Eight genuine scroll frames, aligned native centre segments |
| `elements.saw` | Native grinder capture still |
| `elements.door` | Genuine six-position opening and closing sequences; closed still |
| `elements.pipe` | Native warp pipe still |
| `elements.cannon` | Native Bill Blaster idle still |
| `elements.mushroom` | Genuine 16-frame wobble cycle |
| `fx.coin_pop` | Genuine 16-frame coin spin |
| `fx.star` | Complete 21-source-frame Super Star wobble cycle |
| `fx.brick_debris` | Four actual native fragment cells, independent still variants |

## Missing / blocked — retain renderer fallbacks

- Spring `compress` / `extend`: known SMM2 sheet exists, image fetch blocked by HTTP 403.
- Checkpoint `active` and goal `wave`: no adequately sized verified original sequence
  obtained. The accessible SMM2 checkpoint Wiki file is a **blue-background screenshot**,
  not a transparent sprite; it was rejected. No background was hand-removed or recoloured.
- Question-block `bump`: idle scroll and used state exist; no separate captured bump frames.
  Ordinary positional bump motion may be implemented by the renderer.
- P-switch `pressed`: the 12-frame GIF only highlights the unpressed switch. It is
  never labelled a pressed animation.
- Donut `shake`, grinder `spin`, Bill Blaster `fire`, mushroom `emerge`: no verified
  native source cycles obtained. No rotated stills, squashed stills or fake emerge frames.
- Lava surface animation: existing pack lava art is retained by the integrator; no
  verified native sequence staged in this pass.
- `fx.dust`, `fx.land_puff`, `fx.sparkle`, `fx.stomp_poof`: absent. Use the required
  procedural Phaser fallbacks. Small NSMBU-labelled OpenWE mirror samples were
  inspected in the ignored cache but **not promoted**, because their original ripper
  and unmodified game-rip provenance could not be established.

## Research evidence

The headless browser was Chromium, using the repository's
`assets/packs/mario/playwright.config.json`, with a dedicated `realmforge-objects`
Playwright CLI session. Actual command output from browser navigation:

```text
Page URL: https://www.spriters-resource.com/nintendo_switch/supermariomaker2/asset/155137/
Page Title: Just a moment...
HTTP status: 403

Page URL: https://models.spriters-resource.com/wii_u/newsupermariobrosu/
Page Title: Just a moment...
HTTP status: 403

Page URL: https://textures.spriters-resource.com/wii_u/newsupermariobrosu/
Page Title: Just a moment...
HTTP status: 403

Page URL: https://www.spriters-resource.com/media/assets/152/155137.png?updated=1755483989
Page Title: Just a moment...
HTTP status: 403
```

These are access blockers, not evidence that the underlying game animations do not
exist. The independently written `assets/packs/mario/blender/README.md` also reports
blocked model downloads. No model was imported or rendered by this pass.

Wiki originals were downloaded with browser download links, preserving original
bytes, to `assets/_downloads/objects/`. Metadata was fetched from the public MediaWiki
API and pinned in `source-lock.json`. Cached project 105789235 credits Random Talking
Bush; project 105733943 also credits Woody601 for Goomba, which this pass does not use.
Only costume PNGs were extracted; no source-project code was copied or executed.

The prior cached `hq_qblock`, `hq_star`, `hq_cinta_middle` and `hq_door` files all have
**100% identical pixels within every opaque 2×2 block**. They were already enlarged
before this pass. Staged frames restore their native pixel grid by exact decimation.
The validator checks every source pixel and reconstructs every staged output byte
for byte, including transparent padding. The used Mega Block is downsampled to 64px
so that it and the 64px idle frames share one canvas without shrinking idle art.

## Rights / provenance

Nintendo retains the rights to the imagery. The team's authorization is solely for
its private educational class demo, and is **not a copyright licence**. No source is
claimed to be CC0, open-source or licensed by its hosting site. Original rippers are
named only when the source actually credits them; otherwise that absence is explicit.
The tilesheet mirror does not identify its original ripper. It is used only as
Nintendo imagery under the user's private-demo authorization; no mirror code is reused.

The coordinator should add the source pages in `source-lock.json` to the shared
`assets/CREDITS.md` / `assets/packs/mario/SOURCES.md`; those files are outside this
agent's ownership and have not been edited here.

## Requested checklist update (coordinator only)

Keep “Exact NSMBU fidelity” **in progress**, not complete. Record the staged genuine
question-block, door, conveyor, P-switch, mushroom, coin and Super Star sequences,
four real brick-debris variants, source-enlargement reversal and successful staging
validator. Leave the blocked states and missing particle effects open. Do not mark
integration complete until the owning agent publishes the staging output and runs
its pack/build checks.

## Local validation

From repo root:

```sh
python3 assets/packs/mario/staging/objects/validate.py
```

Actual output is saved in `VALIDATION.txt`. This is a staging-only asset change;
no application test suite or production build was run by this agent. No dependencies
were installed. `prepare.py` reproduces the extraction from the ignored original
source cache and verifies native-grid restoration as it goes.
