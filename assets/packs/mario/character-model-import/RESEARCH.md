# Original animation acquisition research — 1 November 2026

**Result: no publicly downloadable original NSMBU/SMM NSMBU character clip file was obtained in this investigation. Compatibility remains untested.** This is a bounded search result, not a claim that no such files exist anywhere. The two user-supplied ZIPs were the only character asset bytes imported. No third-party executable was downloaded or run.

## Reviewed sources

| Primary source | Observation and disposition |
|---|---|
| [Mario, DogToon64, Models Resource](https://models.spriters-resource.com/wii_u/newsupermariobrosu/asset/332841/) | Lists 12 DAE files and textures matching the supplied archive. The uploader's 25 May 2022 reply to a request for animations says they are absent. Local XML independently confirms zero animation channels. An initially tried incorrect asset URL (`329037`) returned 403; the correct Mario page was found through the game's Mario link. |
| [Luigi, DogToon64, Models Resource](https://models.spriters-resource.com/wii_u/newsupermariobrosu/asset/329038/) | Lists the supplied Luigi models/textures. Comments describe broken eye UVs without mirrored texture wrapping. Actual DAE samplers supply MIRROR settings, which the preview pipeline preserves. No animation file appears in the supplied ZIP. |
| [NSMBU game listing](https://models.spriters-resource.com/wii_u/newsupermariobrosu/) | Playable-character listings, including Mario and Luigi; no verified matching clip download obtained. |
| [SMM2 Models Resource listing](https://models.spriters-resource.com/nintendo_switch/supermariomaker2/) | Its NSMBU character section lists story-mode Toad and Yoshi. No downloadable original Mario/Luigi animation archive found there. Listing models is not evidence of compatible clips. |
| [Switch Toolbox author README](https://github.com/KillzXGaming/Switch-Toolbox) | Describes Wii U/Switch BFRES support and skeletal, texture-pattern and material animation inspection/export. This is a **tool**, not animation content. Archived; GPL-3.0; reference only, no code copied, installed or run. |
| [Cafe Shader Studio author README](https://github.com/KillzXGaming/Cafe-Shader-Studio) and [releases](https://github.com/KillzXGaming/Cafe-Shader-Studio/releases) | Describes NSMBU shader viewing and interpolated animation playback. A viewer requiring the user's own assets, not a clip source. Top-level MIT licence; ancillary resources have additional terms. Nothing installed/copied/run. |
| [BFRES Blender importer author README](https://github.com/ranidspace/BlenderBfresImporter) | Explicitly says Wii U files and animation cannot be imported; also mentions first-frame-only animation data. Rejected as a full-cycle solution. Archived and GPL-3.0; no code copied/installed. |
| [NSMB Hacking Domain animation list](https://nsmbhd.net/wiki/List_of_Player_Animations/) | Explicitly describes the **DS** game and NSBCA data. These are not demonstrated NSMBU skeleton mappings or downloadable compatible FSKA clips. Not used. |
| [pycollada repository](https://github.com/pycollada/pycollada), [licence](https://raw.githubusercontent.com/pycollada/pycollada/master/COPYING), [0.9.3 documentation](https://pycollada.readthedocs.io/en/latest/) | BSD-licensed maintained Collada parser. Used in a scratch Python environment for geometry, material, skeleton and skin inspection. No executable add-on or old Blender binary needed. |

Searches included `NSMBU Mario Luigi skeletal animations download bfska`, `NSMBU player animation Wait Walk Run bfres download`, `NSMBU "animation" "bfska"`, `"New Super Mario Bros. U" "animations" "download" model`, `"NSMBU" ".dae" "animation" download`, `"NSMBU" "animation pack"`, and `"Super Mario Maker" "NSMBU" "skeletal" animation download`. Results describing mods, DS/Wii assets, sprite captures, model-only archives or viewers were not treated as original compatible clips. No skeleton-channel compatibility claim is made from a title, file extension or similar appearance.

## Exact additional inputs required

Obtain original **Wii U NSMBU** player animation resources, or original **SMM NSMBU** clips with their corresponding reference skeletons. Request raw `.bfres` files with nonempty **FSKA skeletal animation sections**, their enclosing `.szs`/SARC archive if separate files depend on it, or faithfully exported `.bfska`, animated `.dae` or skeletal `.smd` files. A model-only DAE, renamed still, texture alternate, first-frame-only import, or video of an animation is insufficient for this model pipeline.

For **each of Mario big, Mario small, Luigi big and Luigi small**, supply clips for these requested runtime states: `idle`, `walk`, `run`, `skid`, `jump`, `fall`, `crouch`, `wallSlide`, `dead`. These are required state meanings, **not asserted original clip filenames**. Preserve the native names and provide an observed state mapping. No verified original container path or per-clip filename was available from the supplied archives; do not present a guessed filename as an acquisition result.

Each delivery must include:

1. Original game/version/platform, archive-relative paths, credited source and SHA-256 of the original container and exports. Keep the raw container intact.
2. Matching reference skeleton with exact bone names, parent indices, rest/local matrices, inverse binds and coordinate/unit conventions. Target names/rest matrices are in `model-inventory.json` and `geometry-evidence.json`.
3. Actual time-varying translation/rotation/scale channels with key times, interpolation, rotation convention, frame rate, duration and loop flags. Walking/running must have at least six distinct genuinely sampled visible poses; repeated names/pixels do not count. Preserve non-looping jump, skid and death clips as non-looping when the source specifies that.
4. Any companion texture-pattern/material/visibility tracks controlling eyes, alternate materials or hidden head parts, with the referenced texture table. The supplied `.0/.1/.2` textures alone give no animation timing or state association.
5. Separate head/cap animation channels where present; otherwise preserve the original attachment behavior through `face_1` and `CapPosition`. An animation using a different root name is a candidate requiring inspection, not automatically compatible.

## Acquisition procedure

- Ask the ripper for the missing **animation exports plus their reference rig**, explicitly naming `MB/MH`, `SMB/SMH`, `LB/LH`, `SLB/SLH` from these archives. The currently published model ZIPs do not solve the missing-channel problem.
- Alternatively, from the team's own extracted Wii U game resources, inspect BFRES resources inside player/common actor archives for nonempty FSKA sections. Retain the whole container and compare its FMDL skeleton with the source rig before exporting clips. For an SMM source, select the NSMBU style and retain its own reference skeleton; 3D World, DS and Wii clips are not assumed interchangeable.
- In an established BFRES inspector/exporter, enumerate the skeleton-animation section, record native clip names and channel targets, export the reference model and full clips together, and inspect at multiple source key times. The Switch Toolbox author's documented skeletal-animation export is a reference route; it has not been installed or validated here, and its GPL code is not to be copied into this repository.
- Accept a candidate only after mapping every animated target by hierarchy/rest transform, checking axis/units and Euler/quaternion conventions, evaluating source interpolation, and confirming real movement without rest-pose distortion. Follow the head socket every sample. Do not repair mismatched bones with invented keys or guessed offsets.
- Only after successful channel inspection and true-cycle renders should an owner produce `manifest-fragment.json`. The current bridge intentionally refuses animated DAE input and needs a separate verified animation evaluator at that stage.

No acquisition message was sent to anyone; these are instructions for the coordinator. No real compatible clips were available, so this task stops at useful model previews as requested.
