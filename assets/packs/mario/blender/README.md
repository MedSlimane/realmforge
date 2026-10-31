# Model-render attempt — blocked, no renders delivered

The installed headless executable is `/Applications/Blender.app/Contents/MacOS/Blender`.
A real `--background --factory-startup --python-expr` probe identified Blender
5.2.1 LTS, an available FBX importer, and an unavailable Collada importer
(`get_rna_type()` checked; `hasattr` on Blender dynamic operators is unreliable).

The Mario and Luigi Models Resource listings offer `.dae` models plus textures.
The Mario uploader explicitly answers “No” to the animation question. The Luigi
listing does not list animation clips. Browser attempts to fetch the actual
model ZIP and the Goomba fallback sheet returned HTTP 403. No model was imported,
no genuine action was sampled, and no render pipeline is claimed as verified.

A future pass needs actual compatible model/clip files before implementing and
visually verifying camera yaw, source FPS, shared per-form scale, feet anchoring,
lighting, Eevee transparency, 2× rendering/downsampling, and atlas assembly.
Do not fill that input gap with hand-keyframed poses or a renamed T-pose.
Evidence and source links: ../RESOLUTION_REPORT.md and ../evidence/.
