# Asset-agent progress (owned paths only)

## High-resolution pass — 31 October 2026

- [x] Read AGENTS.md, SPEC.md, Assets checklist, screenshots, mockup and prior pack docs.
- [x] Capture frozen baseline in audit-before.json; generate per-entry/per-animation-frame before/after AUDIT.md.
- [x] Replace all 50 baseline native/display scale violations; validator rejects >1.25× and build rejects source enlargement.
- [x] Replace Mario big with credited larger NSMBU raster captures, including distinct fall.
- [x] Remove the Mario-recolour Luigi; supply genuine big/small Luigi atlases and small Mario as explicitly documented NSMB Wii same-style fallbacks.
- [~] Exact NSMBU-only HD Luigi + small Mario pose sets remain missing. Luigi skid is a run-transition pose, wall-slide holds wall-contact art. Do not mark this exact-game requirement complete.
- [x] Replace throw-block crate with NSMBU wooden crate; Chain Chomp pendulum with native spiked pendulum ball; Note Block slime with permitted green mushroom-platform sticky-tile substitute.
- [x] Add native five-segment mushroom-seesaw plank and separate pivot; native Super Mushroom under elements.mushroom + items.mushroom.
- [x] Correct terrain side/fill crops, add all named variants and all 47 legal blob masks per theme, verify 2px extruded atlas gutters.
- [x] Update exact-rectangle config, pin used sources, regenerate coverage and PREVIEW.png.
- [x] Four validator regression probes, pack validation and real web registry validation.
- [~] Some high-resolution objects are stills replacing low-resolution cycles: spring extended, Goomba/Paragoomba, state-specific flags and lock overlay. Details in README.md.

## Coordinator integration notes

This agent owns only assets/packs/mario/, web/public/packs/mario/ and ignored downloads. The user's strict ownership rule overrides broad repo requests to edit shared docs. Coordinator must update docs/CHECKLIST.md and assets/CREDITS.md, preserving the exact-game and pose caveats above.

No files staged or committed. No dependencies added. Real command output, pack bytes and deterministic rebuild evidence are recorded in VALIDATION.txt; every output SHA-256 is in pack-sha256.json.

## Final verification

- [x] fetch, build, preview, four validator regression tests, validate and validate:registry all exit 0 (VALIDATION.txt).
- [x] Second build/preview: all 433 pack file SHA-256 values identical.
- [x] 407 sprite entries and every animation frame ≤1.25×; all 50 baseline violations removed.
- [x] Pack size 11,646,109 bytes, below the 25,000,000-byte limit.
- [x] Owned-path git diff --check passes; staging area untouched.
