# Completed object / FX integration handoff

`staging/objects/DONE` arrived after 403 seconds. `objects.json` is a staging
descriptor, not a runtime manifest: its `anims` contain staged PNG paths and
explicit still/animation kinds. The object agent owns staging only.

`python3 scripts/object_integration.py` prepares the finished runtime fragment
and 54 lossless files in `integrated/`. Every decoded atlas rectangle is compared
byte-for-byte with its SHA-256-locked staged PNG. `integrated/manifest-fragment.json`
is the concrete proposed runtime addition. `files.json` records generated hashes.
No images are interpolated, enlarged, recoloured or posed. Static debris variants
have no temporal animation; single-frame object states are explicitly labelled
`kind: still`. Missing state names are not manufactured.

Current public publication is blocked on an asynchronous ownership question: the
user listed public characters, enemies and manifest as this agent's owned paths,
but the object agent only stages files. The prepared addition needs a new public
`objects/` directory. No files have been published there while that question is
unanswered.

After the user authorizes that narrow publication, run from this package:

```sh
npm run build -- --publish-objects
npm run preview
npm test
npm run validate
npm run validate:registry
```

The build copies only the 54 explicitly hashed prepared files into public
`objects/`, merges 15 object entries and 3 FX entries into schema 1, synchronizes
mushroom/cannon consumers and adds question/P-switch compatibility aliases.
Subsequent ordinary builds merge the completed inbox only when its generated
public files match the prepared hashes; otherwise they retain the prior manifest
entries and report the publication blocker. `--full` is the separate maintainer
option for rebuilding the legacy full pack after parallel ownership ends.

`npm run validate` deliberately continues to fail the character fidelity gate:
existing walk/run cycles have only 3–4 frames, and source/pose fallback flags remain.
No replacement character/enemy art or model renders were obtained. Do not remove
those flags to make the check green. Character-model research is in SOURCES.md,
RESOLUTION_REPORT.md and blender/README.md.

The independent staging validator passes 114 RGBA PNGs against 70 original source
checksums and records exact restoration of upstream duplicated 2× pixels. Read
`staging/objects/REPORT.md` for provenance, missing states and source timing limits.
Four absent FX keys must keep the renderer's procedural fallback. P-switch's
variable source durations are retained in metadata; current playback uses average
FPS. No exact variable-rate playback is claimed.
