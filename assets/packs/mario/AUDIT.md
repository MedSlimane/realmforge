# Mario pack native-resolution audit

Each row compares the native frame canvas to `displaySize × 64` gameplay pixels. Atlas padding is excluded. A uniform atlas canvas preserves pose scale and feet; transparent space is not detail. Individual source crop rectangles and any **downsampling** are in `slicing.json`. The builder forbids source upsampling. Background layers have no `displaySize` and are audited for native pixels/seams separately. No AI-generated art is used.

Before is frozen in `audit-before.json`, captured before this pass. Before/after factors include both axes; entries above 1.25 fail `npm run validate`. New entries have no before value. Compatibility aliases appear explicitly.

| Sprite | Before native → display px | Before factor | After native → display px | After factor | Status / caveat |
|---|---|---:|---|---:|---|
| `elements.spikes` | 14×14 → 64.0×64.0 | 4.571× | 96×97 → 64.0×64.0 | 0.667× | PASS; Native 128px SMM2 NSMBU Spike Trap editor render, replaces tiny mirror frames. |
| `elements.lava` | 64×38 → 64.0×64.0 | 1.684× | 128×128 → 64.0×64.0 | 0.500× | PASS |
| `elements.falling_block` | 16×14 → 64.0×64.0 | 4.571× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.saw` | 149×149 → 64.0×64.0 | 0.430× | 149×149 → 64.0×64.0 | 0.430× | PASS |
| `elements.crate` | 64×64 → 64.0×64.0 | 1.000× | 120×120 → 64.0×64.0 | 0.533× | PASS; Authentic NSMBU wooden crate, Miyamoto image collection (no editor code reused). |
| `elements.spring` | 16×16 → 64.0×64.0 | 4.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.spring_extended` | 16×16 → 64.0×64.0 | 4.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.conveyor_belt` | 128×114 → 64.0×64.0 | 0.561× | 128×114 → 64.0×64.0 | 0.561× | PASS |
| `elements.chain_link` | 92×92 → 16.0×16.0 | 0.174× | 92×92 → 16.0×16.0 | 0.174× | PASS |
| `elements.pendulum_ball` | 270×276 → 64.0×64.0 | 0.237× | 140×145 → 64.0×64.0 | 0.457× | PASS; Native NSMBU spiked pendulum ball, cropped from pendulum_0; replaces Chain Chomp. |
| `elements.seesaw` | 80×14 → 320.0×56.0 | 4.000× | 300×30 → 320.0×32.0 | 1.067× | PASS; Five native 60px NSMBU mushroom-seesaw deck segments. Pivot is a separate seesaw_pivot entry. |
| `elements.moving_platform` | 48×8 → 192.0×32.0 | 4.000× | 210×30 → 192.0×32.0 | 1.067× | PASS |
| `elements.elevator` | 48×8 → 192.0×32.0 | 4.000× | 210×30 → 192.0×32.0 | 1.067× | PASS |
| `elements.rotating_platform` | 80×14 → 320.0×56.0 | 4.000× | 300×30 → 320.0×32.0 | 1.067× | PASS; Five native 60px NSMBU mushroom-seesaw deck segments. Pivot is a separate seesaw_pivot entry. |
| `elements.chain_bridge` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; Native rope bridge plank segment; chain_link is supplied for the constraint chain. |
| `elements.coin` | 14×16 → 64.0×64.0 | 4.571× | 128×167 → 64.0×64.0 | 0.500× | PASS |
| `elements.coin_side` | 6×16 → 64.0×64.0 | 10.667× | 52×60 → 64.0×64.0 | 1.231× | PASS |
| `elements.big_coin` | 29×29 → 64.0×64.0 | 2.207× | 120×120 → 64.0×64.0 | 0.533× | PASS |
| `elements.key` | 14×16 → 64.0×64.0 | 4.571× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.powerup_double_jump` | 16×18 → 64.0×64.0 | 4.000× | 174×199 → 64.0×64.0 | 0.368× | PASS |
| `elements.powerup_dash` | 196×186 → 64.0×64.0 | 0.344× | 196×186 → 64.0×64.0 | 0.344× | PASS; Super Star represents dash. |
| `elements.start` | 76×92 → 64.0×64.0 | 0.842× | 76×92 → 64.0×64.0 | 0.842× | PASS |
| `elements.checkpoint` | 18×31 → 64.0×64.0 | 3.556× | 125×199 → 64.0×64.0 | 0.512× | PASS |
| `elements.checkpoint_active` | 17×30 → 64.0×64.0 | 3.765× | 125×199 → 64.0×64.0 | 0.512× | PASS; Native checkpoint pole; same flag design pending an authentic activated-state render. |
| `elements.door` | 156×308 → 64.0×128.0 | 0.416× | 156×308 → 64.0×128.0 | 0.416× | PASS |
| `elements.door_open` | 156×308 → 64.0×128.0 | 0.416× | 156×308 → 64.0×128.0 | 0.416× | PASS |
| `elements.locked_door` | 20×40 → 64.0×128.0 | 3.200× | 156×308 → 64.0×128.0 | 0.416× | PASS; Native closed door, with the separately supplied key indicating lock state in gameplay. |
| `elements.switch` | 64×64 → 64.0×64.0 | 1.000× | 64×64 → 64.0×64.0 | 1.000× | PASS |
| `elements.switch_on` | 64×64 → 64.0×64.0 | 1.000× | 64×64 → 64.0×64.0 | 1.000× | PASS |
| `elements.switch_block` | 64×64 → 64.0×64.0 | 1.000× | 64×64 → 64.0×64.0 | 1.000× | PASS |
| `elements.switch_block_off` | 64×64 → 64.0×64.0 | 1.000× | 64×64 → 64.0×64.0 | 1.000× | PASS |
| `elements.pswitch` | 16×16 → 64.0×64.0 | 4.000× | 66×73 → 64.0×64.0 | 0.970× | PASS |
| `elements.goal` | 48×171 → 89.6×320.0 | 1.871× | 181×600 → 89.6×320.0 | 0.533× | PASS |
| `elements.goal_wave` | 48×171 → 89.6×320.0 | 1.871× | 181×600 → 89.6×320.0 | 0.533× | PASS |
| `elements.pipe` | 128×128 → 128.0×128.0 | 1.000× | 128×128 → 128.0×128.0 | 1.000× | PASS |
| `elements.hard_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS |
| `elements.used_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS |
| `elements.ice` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.slime` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; NSMBU green mushroom-platform surface represents high-friction slime. |
| `elements.grass_ground` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_top` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_top_left` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_top_right` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_fill` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_left` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_right` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_bottom` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_brick` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.grass_question` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.grass_one_way` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_semi_solid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_hard_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.grass_used_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.grass_ice` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_slime` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; NSMBU green mushroom-platform surface stands for sticky terrain; no native NSMBU slime/jelly rip found. |
| `elements.desert_ground` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_top` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_top_left` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_top_right` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_fill` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_left` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_right` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_bottom` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_brick` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.desert_question` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.desert_one_way` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_semi_solid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_hard_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.desert_used_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.desert_ice` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_slime` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; NSMBU green mushroom-platform surface stands for sticky terrain; no native NSMBU slime/jelly rip found. |
| `elements.snow_ground` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_top` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_top_left` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_top_right` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_fill` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_left` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_right` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_bottom` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_brick` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.snow_question` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.snow_one_way` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_semi_solid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_hard_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.snow_used_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.snow_ice` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_slime` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; NSMBU green mushroom-platform surface stands for sticky terrain; no native NSMBU slime/jelly rip found. |
| `elements.castle_ground` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_top` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_top_left` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_top_right` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_fill` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_left` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_right` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_bottom` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_brick` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.castle_question` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.castle_one_way` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_semi_solid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_hard_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.castle_used_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.castle_ice` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_slime` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; NSMBU green mushroom-platform surface stands for sticky terrain; no native NSMBU slime/jelly rip found. |
| `elements.walker` | 21×19 → 64.0×64.0 | 3.368× | 104×122 → 64.0×64.0 | 0.615× | PASS; Native NSMBU Goomba render from Super Mario Wiki. Static pose; no fabricated walk/stomp frames. |
| `elements.shell` | 234×276 → 64.0×96.0 | 0.348× | 234×276 → 64.0×96.0 | 0.348× | PASS |
| `elements.flyer` | 48×40 → 64.0×64.0 | 1.600× | 85×97 → 64.0×64.0 | 0.753× | PASS; Authentic NSMBU Paragoomba replaces low-resolution composite Koopa + wings. |
| `elements.jumper` | 190×184 → 64.0×64.0 | 0.348× | 190×184 → 64.0×64.0 | 0.348× | PASS |
| `elements.cannon` | 16×16 → 64.0×64.0 | 4.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.bullet_bill` | 204×132 → 64.0×64.0 | 0.485× | 204×132 → 64.0×64.0 | 0.485× | PASS |
| `elements.ground` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.brick` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.question` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.question-block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.question_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.one-way` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.one-way-platform` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.one_way` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.oneWay` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.semi-solid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.semi_solid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.semisolid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.falling-block` | 16×14 → 64.0×64.0 | 4.571× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.fallingBlock` | 16×14 → 64.0×64.0 | 4.571× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.pendulum` | 270×276 → 64.0×64.0 | 0.237× | 140×145 → 64.0×64.0 | 0.457× | PASS; Native NSMBU spiked pendulum ball, cropped from pendulum_0; replaces Chain Chomp. |
| `elements.wrecking-ball` | 270×276 → 64.0×64.0 | 0.237× | 140×145 → 64.0×64.0 | 0.457× | PASS; Native NSMBU spiked pendulum ball, cropped from pendulum_0; replaces Chain Chomp. |
| `elements.wrecking_ball` | 270×276 → 64.0×64.0 | 0.237× | 140×145 → 64.0×64.0 | 0.457× | PASS; Native NSMBU spiked pendulum ball, cropped from pendulum_0; replaces Chain Chomp. |
| `elements.chain` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; Native rope bridge plank segment; chain_link is supplied for the constraint chain. |
| `elements.chain-bridge` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; Native rope bridge plank segment; chain_link is supplied for the constraint chain. |
| `elements.trampoline` | 16×16 → 64.0×64.0 | 4.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.conveyor` | 128×114 → 64.0×64.0 | 0.561× | 128×114 → 64.0×64.0 | 0.561× | PASS |
| `elements.conveyor-belt` | 128×114 → 64.0×64.0 | 0.561× | 128×114 → 64.0×64.0 | 0.561× | PASS |
| `elements.moving-platform` | 48×8 → 192.0×32.0 | 4.000× | 210×30 → 192.0×32.0 | 1.067× | PASS |
| `elements.movingPlatform` | 48×8 → 192.0×32.0 | 4.000× | 210×30 → 192.0×32.0 | 1.067× | PASS |
| `elements.rotating-platform` | 80×14 → 320.0×56.0 | 4.000× | 300×30 → 320.0×32.0 | 1.067× | PASS; Five native 60px NSMBU mushroom-seesaw deck segments. Pivot is a separate seesaw_pivot entry. |
| `elements.rotatingPlatform` | 80×14 → 320.0×56.0 | 4.000× | 300×30 → 320.0×32.0 | 1.067× | PASS; Five native 60px NSMBU mushroom-seesaw deck segments. Pivot is a separate seesaw_pivot entry. |
| `elements.big-coin` | 29×29 → 64.0×64.0 | 2.207× | 120×120 → 64.0×64.0 | 0.533× | PASS |
| `elements.bigCoin` | 29×29 → 64.0×64.0 | 2.207× | 120×120 → 64.0×64.0 | 0.533× | PASS |
| `elements.double-jump` | 16×18 → 64.0×64.0 | 4.000× | 174×199 → 64.0×64.0 | 0.368× | PASS |
| `elements.doubleJump` | 16×18 → 64.0×64.0 | 4.000× | 174×199 → 64.0×64.0 | 0.368× | PASS |
| `elements.dash` | 196×186 → 64.0×64.0 | 0.344× | 196×186 → 64.0×64.0 | 0.344× | PASS; Super Star represents dash. |
| `elements.power-up` | 16×18 → 64.0×64.0 | 4.000× | 174×199 → 64.0×64.0 | 0.368× | PASS |
| `elements.powerup` | 16×18 → 64.0×64.0 | 4.000× | 174×199 → 64.0×64.0 | 0.368× | PASS |
| `elements.key-lock-door` | 20×40 → 64.0×128.0 | 3.200× | 156×308 → 64.0×128.0 | 0.416× | PASS; Native closed door, with the separately supplied key indicating lock state in gameplay. |
| `elements.keyLockDoor` | 20×40 → 64.0×128.0 | 3.200× | 156×308 → 64.0×128.0 | 0.416× | PASS; Native closed door, with the separately supplied key indicating lock state in gameplay. |
| `elements.lockedDoor` | 20×40 → 64.0×128.0 | 3.200× | 156×308 → 64.0×128.0 | 0.416× | PASS; Native closed door, with the separately supplied key indicating lock state in gameplay. |
| `elements.switch-block` | 64×64 → 64.0×64.0 | 1.000× | 64×64 → 64.0×64.0 | 1.000× | PASS |
| `characters.mario` | 34×35 → 136.0×140.0 | 4.000× | 181×160 → 135.7×120.0 | 0.750× | PASS; NSMBU raster captures credited to PolskyGamer, Scratch project 839078033. Cropped extracted PNGs; pose scales normalized only by downsampling. Distinct fall capture. |
| `characters.mario_small` | 22×25 → 64.0×72.7 | 2.909× | 64×87 → 51.2×69.6 | 0.800× | PASS; Authentic NSMB Wii raster captures shared by PolskyGamer (project 784192278); same-style fallback, NOT an NSMBU rip. Original ripper credited as Keira Sanchez. Distinct Fall capture; wallSlide holds the wall-jump capture.  |
| `characters.luigi` | 34×35 → 136.0×140.0 | 4.000× | 98×144 → 81.7×120.0 | 0.833× | PASS; Authentic NSMB Wii raster captures shared by PolskyGamer (project 797092569); same-style fallback, NOT an NSMBU rip. Original ripper not stated by this collection. Distinct Fall capture; wallSlide holds the wall-jump capture. Skid reuses a run-transition pose; a separate braking capture was not found. |
| `characters.luigi_native_walk` | 17×26 → 64.0×128.0 | 4.923× | 98×144 → 81.7×120.0 | 0.833× | PASS; Authentic NSMB Wii raster captures shared by PolskyGamer (project 797092569); same-style fallback, NOT an NSMBU rip. Original ripper not stated by this collection. Distinct Fall capture; wallSlide holds the wall-jump capture. Skid reuses a run-transition pose; a separate braking capture was not found. |
| `characters.green` | 34×35 → 136.0×140.0 | 4.000× | 98×144 → 81.7×120.0 | 0.833× | PASS; Schema-1 compatibility name mapped to luigi; not a separate character rip. |
| `characters.pink` | 34×35 → 136.0×140.0 | 4.000× | 181×160 → 135.7×120.0 | 0.750× | PASS; Schema-1 compatibility name mapped to mario; not a separate character rip. |
| `characters.purple` | 34×35 → 136.0×140.0 | 4.000× | 181×160 → 135.7×120.0 | 0.750× | PASS; Schema-1 compatibility name mapped to mario; not a separate character rip. |
| `characters.beige` | 34×35 → 136.0×140.0 | 4.000× | 181×160 → 135.7×120.0 | 0.750× | PASS; Schema-1 compatibility name mapped to mario; not a separate character rip. |
| `enemies.walker` | 21×19 → 64.0×64.0 | 3.368× | 104×122 → 64.0×64.0 | 0.615× | PASS; Native NSMBU Goomba render from Super Mario Wiki. Static pose; no fabricated walk/stomp frames. |
| `enemies.shell` | 234×276 → 64.0×96.0 | 0.348× | 234×276 → 64.0×96.0 | 0.348× | PASS |
| `enemies.flyer` | 48×40 → 64.0×64.0 | 1.600× | 85×97 → 64.0×64.0 | 0.753× | PASS; Authentic NSMBU Paragoomba replaces low-resolution composite Koopa + wings. |
| `enemies.jumper` | 190×184 → 64.0×64.0 | 0.348× | 190×184 → 64.0×64.0 | 0.348× | PASS |
| `enemies.cannon` | 16×16 → 64.0×64.0 | 4.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.seesaw_pivot` | — | — | 42×42 → 48.0×48.0 | 1.143× | PASS |
| `elements.mushroom` | — | — | 128×127 → 64.0×64.0 | 0.504× | PASS; Official NSMBU Super Mushroom artwork. Form behavior is implemented in game-core. |
| `elements.grass_inner` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_bottom_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_bottom_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_pillar_top` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_pillar` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_pillar_bottom` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_single` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_horizontal` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_single_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_single_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_inner_top_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_inner_top_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_inner_bottom_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_inner_bottom_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_inner` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_bottom_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_bottom_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_pillar_top` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_pillar` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_pillar_bottom` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_single` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_horizontal` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_single_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_single_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_inner_top_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_inner_top_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_inner_bottom_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_inner_bottom_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_inner` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_bottom_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_bottom_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_pillar_top` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_pillar` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_pillar_bottom` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_single` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_horizontal` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_single_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_single_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_inner_top_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_inner_top_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_inner_bottom_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_inner_bottom_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_inner` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_bottom_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_bottom_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_pillar_top` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_pillar` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_pillar_bottom` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_single` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_horizontal` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_single_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_single_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_inner_top_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_inner_top_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_inner_bottom_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_inner_bottom_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_mask_0` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_1` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_2` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_3` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_4` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_5` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_6` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_7` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_8` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_9` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_10` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_11` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_12` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_13` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_14` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_15` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_19` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_23` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_27` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_31` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_38` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_39` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_46` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_47` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_55` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_63` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_76` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_77` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_78` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_79` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_95` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_110` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_111` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_127` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_137` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_139` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_141` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_143` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_155` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_159` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_175` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_191` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_205` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_207` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_223` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_239` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_255` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_0` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_1` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_2` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_3` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_4` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_5` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_6` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_7` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_8` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_9` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_10` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_11` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_12` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_13` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_14` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_15` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_19` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_23` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_27` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_31` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_38` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_39` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_46` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_47` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_55` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_63` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_76` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_77` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_78` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_79` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_95` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_110` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_111` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_127` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_137` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_139` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_141` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_143` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_155` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_159` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_175` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_191` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_205` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_207` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_223` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_239` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.desert_mask_255` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_0` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_1` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_2` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_3` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_4` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_5` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_6` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_7` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_8` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_9` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_10` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_11` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_12` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_13` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_14` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_15` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_19` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_23` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_27` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_31` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_38` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_39` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_46` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_47` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_55` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_63` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_76` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_77` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_78` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_79` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_95` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_110` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_111` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_127` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_137` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_139` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_141` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_143` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_155` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_159` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_175` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_191` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_205` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_207` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_223` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_239` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_255` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_0` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_1` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_2` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_3` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_4` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_5` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_6` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_7` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_8` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_9` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_10` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_11` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_12` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_13` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_14` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_15` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_19` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_23` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_27` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_31` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_38` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_39` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_46` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_47` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_55` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_63` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_76` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_77` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_78` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_79` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_95` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_110` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_111` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_127` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_137` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_139` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_141` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_143` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_155` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_159` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_175` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_191` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_205` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_207` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_223` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_239` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.castle_mask_255` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `characters.luigi_small` | — | — | 76×108 → 49.0×69.7 | 0.645× | PASS; Authentic NSMB Wii raster captures shared by PolskyGamer (project 797092569); same-style fallback, NOT an NSMBU rip. Original ripper not stated by this collection. Distinct Fall capture; wallSlide holds the wall-jump capture. Skid reuses a run-transition pose; a separate braking capture was not found. |
| `items.mushroom` | — | — | 128×127 → 64.0×64.0 | 0.504× | PASS; Official NSMBU Super Mushroom artwork. Form behavior is implemented in game-core. |

## Animation frames

Every current atlas frame is listed below. The factor applies to the full fixed native canvas, including deliberately transparent pose margins; no animation may use a different runtime scale. Frame names map to exact native source crops in `slicing.json`.

| Sprite / frame | Native px | Display px | Upscale |
|---|---|---|---:|
| `elements.conveyor_belt/conveyor_belt_0` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor_belt/conveyor_belt_1` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor_belt/conveyor_belt_2` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor_belt/conveyor_belt_3` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor_belt/conveyor_belt_4` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor_belt/conveyor_belt_5` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor_belt/conveyor_belt_6` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor_belt/conveyor_belt_7` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.chain_link/chain_link_0` | 92×92 | 16.0×16.0 | 0.174× |
| `elements.coin/coin_0` | 128×167 | 64.0×64.0 | 0.500× |
| `elements.powerup_dash/powerup_dash_0` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_1` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_2` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_3` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_4` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_5` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_6` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_7` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_8` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_9` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_10` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_11` | 196×186 | 64.0×64.0 | 0.344× |
| `elements.start/start_0` | 76×92 | 64.0×64.0 | 0.842× |
| `elements.start/start_1` | 76×92 | 64.0×64.0 | 0.842× |
| `elements.start/start_2` | 76×92 | 64.0×64.0 | 0.842× |
| `elements.start/start_3` | 76×92 | 64.0×64.0 | 0.842× |
| `elements.start/start_4` | 76×92 | 64.0×64.0 | 0.842× |
| `elements.start/start_5` | 76×92 | 64.0×64.0 | 0.842× |
| `elements.door/door_0` | 156×308 | 64.0×128.0 | 0.416× |
| `elements.door_open/door_open_0` | 156×308 | 64.0×128.0 | 0.416× |
| `elements.switch/switch_0` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.switch_on/switch_on_0` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.switch_block/switch_block_0` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.walker/walker_0` | 104×122 | 64.0×64.0 | 0.615× |
| `elements.shell/shell_0` | 234×276 | 64.0×96.0 | 0.348× |
| `elements.shell/shell_1` | 234×276 | 64.0×96.0 | 0.348× |
| `elements.shell/shell_2` | 234×276 | 64.0×96.0 | 0.348× |
| `elements.shell/shell_3` | 234×276 | 64.0×96.0 | 0.348× |
| `elements.shell/shell_4` | 234×276 | 64.0×96.0 | 0.348× |
| `elements.shell/shell_5` | 234×276 | 64.0×96.0 | 0.348× |
| `elements.shell/shell_6` | 234×276 | 64.0×96.0 | 0.348× |
| `elements.shell/shell_7` | 234×276 | 64.0×96.0 | 0.348× |
| `elements.shell/shell_8` | 234×276 | 64.0×96.0 | 0.348× |
| `elements.shell/shell_9` | 234×276 | 64.0×96.0 | 0.348× |
| `elements.flyer/flyer_0` | 85×97 | 64.0×64.0 | 0.753× |
| `elements.jumper/jumper_0` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.jumper/jumper_1` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.jumper/jumper_2` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.jumper/jumper_3` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.jumper/jumper_4` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.jumper/jumper_5` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.jumper/jumper_6` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.jumper/jumper_7` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.jumper/jumper_8` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.jumper/jumper_9` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.jumper/jumper_10` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.jumper/jumper_11` | 190×184 | 64.0×64.0 | 0.348× |
| `elements.bullet_bill/bullet_bill_0` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_1` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_2` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_3` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_4` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_5` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_6` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_7` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_8` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_9` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_10` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_11` | 204×132 | 64.0×64.0 | 0.485× |
| `characters.mario/mario_0` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_1` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_2` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_3` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_4` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_5` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_6` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_7` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_8` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_9` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_10` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_11` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_12` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_13` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_14` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_15` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_16` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_17` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_18` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_19` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_20` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario_small/mario_small_0` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_1` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_2` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_3` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_4` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_5` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_6` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_7` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_8` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_9` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_10` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_11` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_12` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_13` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_14` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_15` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_16` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_17` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_18` | 64×87 | 51.2×69.6 | 0.800× |
| `characters.luigi/luigi_0` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_1` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_2` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_3` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_4` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_5` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_6` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_7` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_8` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_9` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_10` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_11` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_12` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_13` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_14` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_15` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_16` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_17` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi/luigi_18` | 98×144 | 81.7×120.0 | 0.833× |
| `characters.luigi_small/luigi_small_0` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_1` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_2` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_3` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_4` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_5` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_6` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_7` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_8` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_9` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_10` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_11` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_12` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_13` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_14` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_15` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_16` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_17` | 76×108 | 49.0×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_18` | 76×108 | 49.0×69.7 | 0.645× |

## Result

- Before: **50/159** sprite entries above 1.25×.
- After: **0/407** sprite entries above 1.25×.
- Known semantic substitutions are disclosed in README.md and the entry notes; a scale pass is not a provenance or pose-completeness claim.
