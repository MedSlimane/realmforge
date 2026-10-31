# Remaining-compromises resolution — 31 October 2026

This pass replaces the coin artwork with genuine sourced spin cycles and replaces the unmarked closed door with an authentic locked-door texture. Exact character forms/poses and the other object cycles remain incomplete. No AI art, model rendering, recolouring, pose interpolation, source upscaling or renamed still presented as animation was used. Existing manifest IDs and schema 1 remain intact.

Nintendo retains the image rights. The team's private class-demo authorization is **not a Nintendo copyright licence**; educational use does not itself grant one. No downloaded executable source code was copied or run.

## Every requested gap

| Requested gap | Result | Evidence / remaining blocker |
|---|---|---|
| Genuine NSMBU/Deluxe/SMM NSMBU **big Luigi** | **Unresolved; retained Wii fallback** | Existing project [797092569](https://scratch.mit.edu/projects/797092569/) explicitly identifies NSMB Wii. Cached project 491846454 says its Wii imagery was adjusted to match Wii U colour resolution; rejected. Project 487872992 is a single pose with restricted collection instructions, not a complete authentic pose set. No verified, adequately sized exact-game capture cycle obtained. |
| Genuine NSMBU **small Luigi** | **Unresolved; retained Wii fallback** | Same Wii collection. Cached Multiverse sheets do not establish original NSMBU gameplay-capture provenance. They were not substituted or relabelled. |
| Genuine NSMBU **small Mario** | **Unresolved; retained Wii fallback** | Current [784192278](https://scratch.mit.edu/projects/784192278/) explicitly labels itself NSMBW and credits Keira Sanchez. Cached project 830398156 contains a Multiverse sheet; the public [SMM2 source discussion](https://www.spriters-resource.com/nintendo_switch/supermariomaker2/page-2/) also distinguishes that fangame sheet. No verified exact-game HD sequence obtained. |
| Genuine **skid poses** | **Partly present, still incomplete** | Existing big-Mario captures and small-Mario Wii skid stay; Luigi still uses a run-transition pose. No new independently verified Luigi braking capture found. |
| Genuine **wall-slide poses** | **Unresolved; retained contact captures** | Existing wall-contact/jump captures remain held poses. No distinct verified slide loop added. |
| Goomba **walk cycle** | **Unresolved; retained high-resolution still** | [TSR 238649](https://www.spriters-resource.com/nintendo_switch/supermariomaker2/asset/238649/) identifies an SMM2 NSMBU gameplay sheet by DogToon64, 994×1249. Its public download returned HTTP 403. Cached Scratch project 779565941 serves 15 walking frames, but supplies no original ripper/source evidence; not promoted to a verified exact-game replacement. Existing OpenWE walk frames are only 20×20, roughly 16×19 opaque. |
| Goomba **stomp** | **Unresolved; retained explicit still substitute** | Same inaccessible TSR sheet. Existing cached OpenWE stomp is 24×16 with only 21×7 opaque content, inadequate at current display size. No manufactured squash. |
| Paragoomba **wing cycle** | **Unresolved; retained native still** | Miyamoto supplies a 96×105 Paragoomba still, not a wing sequence. No verified adequate native cycle obtained. No stills alternated or transformed to imply flapping. |
| **Spinning coin** | **Replaced** | [NSMBUCoin.gif](https://www.mariowiki.com/File:NSMBUCoin.gif), native 52×60, **16 distinct frames**, 50 ms each (20 fps), all used in source order. Wiki identifies NSMBU and credits TSR; original uploader TheMorningFlash, border crop Cheese Head (2025). `items/coin.png`, `items/coin/atlas.{png,json}`; existing `idle` preserved, `spin` added. |
| **Spinning big coin** | **Replaced with authentic 10-Coin design** | [SMM2-NSMBU-10Coin.gif](https://www.mariowiki.com/File:SMM2-NSMBU-10Coin.gif), native 118×118, **13 distinct frames**, 60 ms each, all used in source order. Thejohnston7's 16 April 2025 file history credits TSR. `items/big_coin.png`, `items/big_coin/atlas.{png,json}`. Replaces the static Star Coin design under the same `big_coin` ID. |
| Springboard **compressed / extended** | **Unresolved; retained stills** | [TSR trampoline 155137](https://www.spriters-resource.com/nintendo_switch/supermariomaker2/asset/155137/) identifies a 368×488 SMM2 NSMBU sheet by DogToon64; image download returned 403. Wiki's 78×77 SMM spring is only a normal-state still. Cached OpenWE cycles are 16×16. `spring_extended` remains explicitly a normal-state substitute. |
| **Active checkpoint** | **Unresolved; retained inactive design** | Accessible Wiki checkpoint images are single inactive designs. Existing Miyamoto still supplies no active frame. [TSR checkpoint 155107](https://www.spriters-resource.com/nintendo_switch/supermariomaker2/asset/155107/) was inaccessible (403); no state invented by recolouring. |
| **Waving goal** | **Unresolved; retained static pole** | [TSR goal 121521](https://www.spriters-resource.com/nintendo_switch/supermariomaker2/asset/121521/) was inaccessible (403). Wiki has static goal-pole captures. Cached OpenWE flags are only 29×24. `goal_wave` remains an explicitly static helper, not a wave cycle. |
| **Locked-door overlay / visible lock** | **Visible lock replaced; separate overlay unresolved** | [SMM-NSMBU-Locked-Door.png](https://www.mariowiki.com/File:SMM-NSMBU-Locked-Door.png), native **78×154**, identifies SMM NSMBU locked door and credits TSR; current image by MatiasNTRM (2021), bump maps applied. `flow/locked_door.png` now has the actual integrated keyhole. No separate transparent overlay was available or fabricated. |
| **Thin physical seesaw** | **Outside this pass's ownership** | Requires game-core physics/integration changes, not an image replacement. No physics file edited. Coordinator/physics owner must verify the concurrent fix and update the shared checklist. |
| **Kenney mushroom placeholder** | **Outside this pass's ownership** | Requires the CC0 pack's source/build/manifest paths outside `assets/packs/mario/` and `web/public/packs/mario/`. No Kenney file edited by this pass. Coordinator/CC0 owner must verify the concurrent replacement and record its licence. Nintendo mushroom imagery is not a CC0 replacement. |

## Audit and build corrections

- Audit factors now use decoded alpha-content bounds, excluding empty canvas and atlas gutters. For animation, maximum genuine pose width/height forms the common native content envelope, so a naturally edge-on coin or crouch keeps the same runtime scale. Every frame's own native opaque and actual displayed opaque dimensions are listed in `AUDIT.md`.
- Regression coverage rejects 8×8 opaque art padded to a 128×128 canvas and requested at 128×128 display; padding cannot improve its content budget.
- Source margins were removed from the static one-way decks, chain-bridge segment, key and coin-side capture. Their `displaySize` values were reduced proportionally, preserving their exact previous visible sizes. No art was enlarged to pass the audit.
- The legacy terrain builder restores transparent tile space below a trimmed thin deck, then adds edge extrusion. It rejects terrain upscaling; a regression prevents stretching that deck to fill the tile.
- `animationFrameRates` in the slicing config records the two GIFs' actual timing. This is build metadata; generated manifest entries keep their existing schema.
- Previous working specs for all three replaced entries are in `resolution-fallbacks.json`; old source records remain pinned. Source fetching stays separate from the offline build, so failed research/downloads do not remove the working pack.

## Research boundary

Started with SOURCES.md, existing research metadata and downloaded images. Direct TSR pages/media returned 403; web search could read some metadata but did not deliver the image bytes. The in-app browser tool reported “The browser access host is unavailable.” No login, authentication bypass or CAPTCHA work was attempted. No raw public texture repository with a verified complete missing pose set was found in the reviewed material. Accessible Wiki image originals supplied the actual replacements. Unverified Scratch captures were left as research candidates in ignored downloads.

## Coordinator handoff

Do not mark “exact NSMBU fidelity” complete. Record the two sourced coin cycles, actual locked-door state, content-based audit and remaining caveats in `docs/CHECKLIST.md`; add the three source-page credits to the shared asset credits as appropriate. These shared files were deliberately not edited. Physics and Kenney work require their owners' evidence. No commits, staging or pushes were performed by this pass.

Validation commands and real output are in `VALIDATION.txt`. `PREVIEW.png` includes all sourced coin frames as well as the full pack. `pack-sha256.json` records final output hashes and the repeated build/preview check.
