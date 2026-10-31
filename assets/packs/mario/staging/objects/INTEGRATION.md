# Object staging in progress

The objects agent owns only this staging folder and ignored `assets/_downloads/objects/`.
`objects.json` and `DONE` will be written when extraction and validation finish.

Important source audit: cached Scratch qblock, conveyor, door, and star images
(`hq_qblock`, `hq_cinta_middle`, `hq_door`, `hq_star`) are **exact 2× nearest-neighbour
pixel duplicates**, including all nontransparent 2×2 source blocks. They must not
be presented as native HD images. This staging pass restores their native pixel
grid by exact decimation and records that operation; it never enlarges source art.

The Models Resource, Textures Resource and current TSR trampoline image URL
returned HTTP 403 in headless Chromium. Blender README independently reports the
characters agent's blocked model downloads. No model renders are delivered.

The existing ELEMENT_TYPES use `switch` (ON/OFF), `falling_block` (donut), `saw`
(grinder), `pipe` and `cannon`. P-switch has a pack `pswitch` entry but no game-core
mechanic; its frozen animation name is `p_switch`. Final entries preserve these
identifiers explicitly; aliases, where useful, are metadata only.

# Final handoff

See REPORT.md. `objects.json` contains staging metadata, not an already-published
manifest. Its PNG paths and anim frame paths are relative to this folder. The
characters agent is responsible for copying/atlasing to web/public as instructed
by the user. The current build helper's expectation of already-published art needs
an integration change in the owning agent's paths. The objects agent cannot make
that change or publish web/public files.
