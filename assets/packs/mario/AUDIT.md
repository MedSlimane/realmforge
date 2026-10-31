# Mario pack native-resolution audit

Current factors compare **native opaque content** against `displaySize × 64`, excluding transparent margins and atlas gutters. For an animation the maximum opaque width/height over its genuine poses defines a common content envelope: a naturally narrow edge-on coin or crouch does not get enlarged independently. Every frame below also lists its own opaque dimensions and the opaque dimensions actually drawn by the canvas-based renderer. No transparent canvas counts as native detail. The builder rejects source upsampling.

The frozen baseline only recorded canvas dimensions; its factors are historical canvas measurements, not newly verified opaque-content measurements. A scale pass does not certify exact-game provenance. See RESOLUTION_REPORT.md.

| Sprite | Before canvas → display px | Historical factor | After opaque envelope → display px | Content factor | Status / caveat |
|---|---|---:|---|---:|---|
| `elements.spikes` | 14×14 → 64.0×64.0 | 4.571× | 96×97 → 64.0×64.0 | 0.667× | PASS; Native 128px SMM2 NSMBU Spike Trap editor render, replaces tiny mirror frames. |
| `elements.lava` | 64×38 → 64.0×64.0 | 1.684× | 128×128 → 64.0×64.0 | 0.500× | PASS |
| `elements.falling_block` | 16×14 → 64.0×64.0 | 4.571× | 60×53 → 64.0×64.0 | 1.208× | PASS; Donut idle only; shake is gameplay movement, no fabricated sprite cycle. |
| `elements.saw` | 149×149 → 64.0×64.0 | 0.430× | 149×149 → 96.0×96.0 | 0.644× | PASS; 149px captured grinder still. No pre-rotated frames manufactured. |
| `elements.crate` | 64×64 → 64.0×64.0 | 1.000× | 120×120 → 64.0×64.0 | 0.533× | PASS; Authentic NSMBU wooden crate, Miyamoto image collection (no editor code reused). |
| `elements.spring` | 16×16 → 64.0×64.0 | 4.000× | 78×77 → 64.0×64.0 | 0.831× | PASS; Genuine normal-state still; compressed and extended source states unavailable. |
| `elements.spring_extended` | 16×16 → 64.0×64.0 | 4.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.conveyor_belt` | 128×114 → 64.0×64.0 | 0.561× | 64×57 → 64.0×57.0 | 1.000× | PASS; Eight genuine scroll frames. Restore exact native pixels, then crop aligned 64x57 centre segments; no belt translated to synthesize frames. |
| `elements.chain_link` | 92×92 → 16.0×16.0 | 0.174× | 92×92 → 16.0×16.0 | 0.174× | PASS |
| `elements.pendulum_ball` | 270×276 → 64.0×64.0 | 0.237× | 140×145 → 64.0×64.0 | 0.457× | PASS; Native NSMBU spiked pendulum ball, cropped from pendulum_0; replaces Chain Chomp. |
| `elements.seesaw` | 80×14 → 320.0×56.0 | 4.000× | 300×30 → 320.0×32.0 | 1.067× | PASS; Five native 60px NSMBU mushroom-seesaw deck segments. Pivot is a separate seesaw_pivot entry. |
| `elements.moving_platform` | 48×8 → 192.0×32.0 | 4.000× | 188×30 → 192.0×32.0 | 1.067× | PASS |
| `elements.elevator` | 48×8 → 192.0×32.0 | 4.000× | 188×30 → 192.0×32.0 | 1.067× | PASS |
| `elements.rotating_platform` | 80×14 → 320.0×56.0 | 4.000× | 300×30 → 320.0×32.0 | 1.067× | PASS; Five native 60px NSMBU mushroom-seesaw deck segments. Pivot is a separate seesaw_pivot entry. |
| `elements.chain_bridge` | 64×64 → 64.0×64.0 | 1.000× | 60×23 → 64.0×24.5 | 1.067× | PASS; Native rope bridge plank segment; chain_link is supplied for the constraint chain. Transparent source margins removed; previous visible size preserved. |
| `elements.coin` | 14×16 → 64.0×64.0 | 4.571× | 52×60 → 64.0×64.0 | 1.231× | PASS; Native 16-frame NSMBU Coin cycle from Mario Wiki; original GIF order and timing, no interpolated or duplicated poses. See RESOLUTION_REPORT.md. |
| `elements.coin_side` | 6×16 → 64.0×64.0 | 10.667× | 46×60 → 56.6×64.0 | 1.231× | PASS;  Transparent source margins removed; previous visible size preserved. |
| `elements.big_coin` | 29×29 → 64.0×64.0 | 2.207× | 116×116 → 64.0×64.0 | 0.552× | PASS; Native 13-frame SMM2 NSMBU 10-Coin cycle from Mario Wiki; original GIF order and timing, no interpolated or duplicated poses. See RESOLUTION_REPORT.md. |
| `elements.key` | 14×16 → 64.0×64.0 | 4.571× | 51×58 → 54.4×61.9 | 1.067× | PASS;  Transparent source margins removed; previous visible size preserved. |
| `elements.powerup_double_jump` | 16×18 → 64.0×64.0 | 4.000× | 174×199 → 64.0×64.0 | 0.368× | PASS |
| `elements.powerup_dash` | 196×186 → 64.0×64.0 | 0.344× | 196×186 → 64.0×64.0 | 0.344× | PASS; Super Star represents dash. |
| `elements.start` | 76×92 → 64.0×64.0 | 0.842× | 76×92 → 64.0×64.0 | 0.842× | PASS |
| `elements.checkpoint` | 18×31 → 64.0×64.0 | 3.556× | 106×171 → 80.0×129.3 | 0.756× | PASS; Inactive Bowser checkpoint only. No invented recoloured Mario flag. |
| `elements.checkpoint_active` | 17×30 → 64.0×64.0 | 3.765× | 125×199 → 64.0×64.0 | 0.512× | PASS; Native checkpoint pole; same flag design pending an authentic activated-state render. |
| `elements.door` | 156×308 → 64.0×128.0 | 0.416× | 78×154 → 64.0×128.0 | 0.831× | PASS; Actual six-position opening cycle and original closing poses. No warping or generated in-between frames. |
| `elements.door_open` | 156×308 → 64.0×128.0 | 0.416× | 156×308 → 64.0×128.0 | 0.416× | PASS |
| `elements.locked_door` | 20×40 → 64.0×128.0 | 3.200× | 78×154 → 64.0×128.0 | 0.831× | PASS; Authentic SMM NSMBU locked-door state with integrated keyhole, sourced from Mario Wiki/TSR. Full texture, not a separately extracted transparent lock overlay. |
| `elements.switch` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; Two genuine still states, not an invented interpolated transition. OFF image source is separately pinned. |
| `elements.switch_on` | 64×64 → 64.0×64.0 | 1.000× | 64×64 → 64.0×64.0 | 1.000× | PASS |
| `elements.switch_block` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; Solid and dotted red/blue still states. Not a flashing animation. |
| `elements.switch_block_off` | 64×64 → 64.0×64.0 | 1.000× | 54×54 → 64.0×64.0 | 1.185× | PASS |
| `elements.pswitch` | 16×16 → 64.0×64.0 | 4.000× | 82×91 → 64.0×64.0 | 0.780× | PASS; Real P-switch highlight cycle; this GIF never depresses. Existing pack key pswitch corresponds to requested p_switch. |
| `elements.goal` | 48×171 → 89.6×320.0 | 1.871× | 312×1015 → 98.6×320.0 | 0.316× | PASS; Native tall pole and Mario flag still. No wave loop supplied. |
| `elements.goal_wave` | 48×171 → 89.6×320.0 | 1.871× | 181×600 → 89.6×320.0 | 0.533× | PASS |
| `elements.pipe` | 128×128 → 128.0×128.0 | 1.000× | 120×120 → 128.0×128.0 | 1.067× | PASS; Native 120px pipe, displayed at 128px (1.067x; below 1.25x limit). |
| `elements.hard_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS |
| `elements.used_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS |
| `elements.ice` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.slime` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; NSMBU green mushroom-platform surface represents high-friction slime. |
| `elements.grass_ground` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_top` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_top_left` | 64×64 → 64.0×64.0 | 1.000× | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.grass_top_right` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_fill` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_left` | 64×64 → 64.0×64.0 | 1.000× | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.grass_right` | 64×64 → 64.0×64.0 | 1.000× | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.grass_bottom` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_brick` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.grass_question` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.grass_one_way` | 64×64 → 64.0×64.0 | 1.000× | 60×23 → 64.0×24.5 | 1.067× | PASS;  Transparent source margins removed; previous visible size preserved. |
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
| `elements.desert_one_way` | 64×64 → 64.0×64.0 | 1.000× | 60×23 → 64.0×24.5 | 1.067× | PASS;  Transparent source margins removed; previous visible size preserved. |
| `elements.desert_semi_solid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_hard_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.desert_used_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.desert_ice` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_slime` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; NSMBU green mushroom-platform surface stands for sticky terrain; no native NSMBU slime/jelly rip found. |
| `elements.snow_ground` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_top` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_top_left` | 64×64 → 64.0×64.0 | 1.000× | 59×60 → 64.0×64.0 | 1.085× | PASS |
| `elements.snow_top_right` | 64×64 → 64.0×64.0 | 1.000× | 59×60 → 64.0×64.0 | 1.085× | PASS |
| `elements.snow_fill` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_left` | 64×64 → 64.0×64.0 | 1.000× | 54×60 → 64.0×64.0 | 1.185× | PASS |
| `elements.snow_right` | 64×64 → 64.0×64.0 | 1.000× | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.snow_bottom` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_brick` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.snow_question` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.snow_one_way` | 64×64 → 64.0×64.0 | 1.000× | 60×23 → 64.0×24.5 | 1.067× | PASS;  Transparent source margins removed; previous visible size preserved. |
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
| `elements.castle_one_way` | 64×64 → 64.0×64.0 | 1.000× | 60×24 → 64.0×25.6 | 1.067× | PASS;  Transparent source margins removed; previous visible size preserved. |
| `elements.castle_semi_solid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_hard_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.castle_used_block` | 64×64 → 64.0×64.0 | 1.000× | 128×128 → 64.0×64.0 | 0.500× | PASS; Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture. |
| `elements.castle_ice` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.castle_slime` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS; NSMBU green mushroom-platform surface stands for sticky terrain; no native NSMBU slime/jelly rip found. |
| `elements.walker` | 21×19 → 64.0×64.0 | 3.368× | 104×122 → 64.0×64.0 | 0.615× | PASS; Native NSMBU Goomba render from Super Mario Wiki. Static pose; no fabricated walk/stomp frames. |
| `elements.shell` | 234×276 → 64.0×96.0 | 0.348× | 234×276 → 64.0×96.0 | 0.348× | PASS |
| `elements.flyer` | 48×40 → 64.0×64.0 | 1.600× | 85×97 → 64.0×64.0 | 0.753× | PASS; Authentic NSMBU Paragoomba replaces low-resolution composite Koopa + wings. |
| `elements.jumper` | 190×184 → 64.0×64.0 | 0.348× | 190×184 → 64.0×64.0 | 0.348× | PASS |
| `elements.cannon` | 16×16 → 64.0×64.0 | 4.000× | 78×154 → 64.0×128.0 | 0.831× | PASS; Bill Blaster idle still. Fire smoke candidate in ignored research has unverified rip attribution and is not integrated. |
| `elements.bullet_bill` | 204×132 → 64.0×64.0 | 0.485× | 204×132 → 64.0×64.0 | 0.485× | PASS |
| `elements.ground` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.brick` | 64×64 → 64.0×64.0 | 1.000× | 120×120 → 64.0×64.0 | 0.533× | PASS; Native 120px Mega Block sprite down-displayed to a one-tile brick; no resize in source files. |
| `elements.question` | 64×64 → 64.0×64.0 | 1.000× | 64×64 → 64.0×64.0 | 1.000× | PASS; 16 genuine native 64px question-symbol scroll frames. Used state is Mario Wiki native Big Empty Block; see per-frame source lock. No captured bump poses. |
| `elements.question-block` | 64×64 → 64.0×64.0 | 1.000× | 64×64 → 64.0×64.0 | 1.000× | PASS; 16 genuine native 64px question-symbol scroll frames. Used state is Mario Wiki native Big Empty Block; see per-frame source lock. No captured bump poses. |
| `elements.question_block` | 64×64 → 64.0×64.0 | 1.000× | 64×64 → 64.0×64.0 | 1.000× | PASS; 16 genuine native 64px question-symbol scroll frames. Used state is Mario Wiki native Big Empty Block; see per-frame source lock. No captured bump poses. |
| `elements.one-way` | 64×64 → 64.0×64.0 | 1.000× | 60×23 → 64.0×24.5 | 1.067× | PASS;  Transparent source margins removed; previous visible size preserved. |
| `elements.one-way-platform` | 64×64 → 64.0×64.0 | 1.000× | 60×23 → 64.0×24.5 | 1.067× | PASS;  Transparent source margins removed; previous visible size preserved. |
| `elements.one_way` | 64×64 → 64.0×64.0 | 1.000× | 60×23 → 64.0×24.5 | 1.067× | PASS;  Transparent source margins removed; previous visible size preserved. |
| `elements.oneWay` | 64×64 → 64.0×64.0 | 1.000× | 60×23 → 64.0×24.5 | 1.067× | PASS;  Transparent source margins removed; previous visible size preserved. |
| `elements.semi-solid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.semi_solid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.semisolid` | 64×64 → 64.0×64.0 | 1.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.falling-block` | 16×14 → 64.0×64.0 | 4.571× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.fallingBlock` | 16×14 → 64.0×64.0 | 4.571× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.pendulum` | 270×276 → 64.0×64.0 | 0.237× | 140×145 → 64.0×64.0 | 0.457× | PASS; Native NSMBU spiked pendulum ball, cropped from pendulum_0; replaces Chain Chomp. |
| `elements.wrecking-ball` | 270×276 → 64.0×64.0 | 0.237× | 140×145 → 64.0×64.0 | 0.457× | PASS; Native NSMBU spiked pendulum ball, cropped from pendulum_0; replaces Chain Chomp. |
| `elements.wrecking_ball` | 270×276 → 64.0×64.0 | 0.237× | 140×145 → 64.0×64.0 | 0.457× | PASS; Native NSMBU spiked pendulum ball, cropped from pendulum_0; replaces Chain Chomp. |
| `elements.chain` | 64×64 → 64.0×64.0 | 1.000× | 60×23 → 64.0×24.5 | 1.067× | PASS; Native rope bridge plank segment; chain_link is supplied for the constraint chain. Transparent source margins removed; previous visible size preserved. |
| `elements.chain-bridge` | 64×64 → 64.0×64.0 | 1.000× | 60×23 → 64.0×24.5 | 1.067× | PASS; Native rope bridge plank segment; chain_link is supplied for the constraint chain. Transparent source margins removed; previous visible size preserved. |
| `elements.trampoline` | 16×16 → 64.0×64.0 | 4.000× | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.conveyor` | 128×114 → 64.0×64.0 | 0.561× | 128×114 → 64.0×64.0 | 0.561× | PASS |
| `elements.conveyor-belt` | 128×114 → 64.0×64.0 | 0.561× | 128×114 → 64.0×64.0 | 0.561× | PASS |
| `elements.moving-platform` | 48×8 → 192.0×32.0 | 4.000× | 188×30 → 192.0×32.0 | 1.067× | PASS |
| `elements.movingPlatform` | 48×8 → 192.0×32.0 | 4.000× | 188×30 → 192.0×32.0 | 1.067× | PASS |
| `elements.rotating-platform` | 80×14 → 320.0×56.0 | 4.000× | 300×30 → 320.0×32.0 | 1.067× | PASS; Five native 60px NSMBU mushroom-seesaw deck segments. Pivot is a separate seesaw_pivot entry. |
| `elements.rotatingPlatform` | 80×14 → 320.0×56.0 | 4.000× | 300×30 → 320.0×32.0 | 1.067× | PASS; Five native 60px NSMBU mushroom-seesaw deck segments. Pivot is a separate seesaw_pivot entry. |
| `elements.big-coin` | 29×29 → 64.0×64.0 | 2.207× | 116×116 → 64.0×64.0 | 0.552× | PASS; Native 13-frame SMM2 NSMBU 10-Coin cycle from Mario Wiki; original GIF order and timing, no interpolated or duplicated poses. See RESOLUTION_REPORT.md. |
| `elements.bigCoin` | 29×29 → 64.0×64.0 | 2.207× | 116×116 → 64.0×64.0 | 0.552× | PASS; Native 13-frame SMM2 NSMBU 10-Coin cycle from Mario Wiki; original GIF order and timing, no interpolated or duplicated poses. See RESOLUTION_REPORT.md. |
| `elements.double-jump` | 16×18 → 64.0×64.0 | 4.000× | 174×199 → 64.0×64.0 | 0.368× | PASS |
| `elements.doubleJump` | 16×18 → 64.0×64.0 | 4.000× | 174×199 → 64.0×64.0 | 0.368× | PASS |
| `elements.dash` | 196×186 → 64.0×64.0 | 0.344× | 196×186 → 64.0×64.0 | 0.344× | PASS; Super Star represents dash. |
| `elements.power-up` | 16×18 → 64.0×64.0 | 4.000× | 174×199 → 64.0×64.0 | 0.368× | PASS |
| `elements.powerup` | 16×18 → 64.0×64.0 | 4.000× | 174×199 → 64.0×64.0 | 0.368× | PASS |
| `elements.key-lock-door` | 20×40 → 64.0×128.0 | 3.200× | 78×154 → 64.0×128.0 | 0.831× | PASS; Authentic SMM NSMBU locked-door state with integrated keyhole, sourced from Mario Wiki/TSR. Full texture, not a separately extracted transparent lock overlay. |
| `elements.keyLockDoor` | 20×40 → 64.0×128.0 | 3.200× | 78×154 → 64.0×128.0 | 0.831× | PASS; Authentic SMM NSMBU locked-door state with integrated keyhole, sourced from Mario Wiki/TSR. Full texture, not a separately extracted transparent lock overlay. |
| `elements.lockedDoor` | 20×40 → 64.0×128.0 | 3.200× | 78×154 → 64.0×128.0 | 0.831× | PASS; Authentic SMM NSMBU locked-door state with integrated keyhole, sourced from Mario Wiki/TSR. Full texture, not a separately extracted transparent lock overlay. |
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
| `enemies.cannon` | 16×16 → 64.0×64.0 | 4.000× | 78×154 → 64.0×128.0 | 0.831× | PASS; Bill Blaster idle still. Fire smoke candidate in ignored research has unverified rip attribution and is not integrated. |
| `elements.seesaw_pivot` | — | — | 42×42 → 48.0×48.0 | 1.143× | PASS |
| `elements.mushroom` | — | — | 92×90 → 64.0×64.0 | 0.711× | PASS; Genuine 16-frame wobble cycle, not an emerge capture. Emerge motion must be supplied by gameplay. |
| `elements.grass_inner` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_bottom_left` | — | — | 56×60 → 64.0×64.0 | 1.143× | PASS |
| `elements.grass_bottom_right` | — | — | 56×60 → 64.0×64.0 | 1.143× | PASS |
| `elements.grass_pillar_top` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_pillar` | — | — | 54×60 → 64.0×64.0 | 1.185× | PASS |
| `elements.grass_pillar_bottom` | — | — | 54×60 → 64.0×64.0 | 1.185× | PASS |
| `elements.grass_single` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_horizontal` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_single_left` | — | — | 58×60 → 64.0×64.0 | 1.103× | PASS |
| `elements.grass_single_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.grass_inner_top_left` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.grass_inner_top_right` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.grass_inner_bottom_left` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.grass_inner_bottom_right` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.desert_inner` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_bottom_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_bottom_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_pillar_top` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_pillar` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_pillar_bottom` | — | — | 58×60 → 64.0×64.0 | 1.103× | PASS |
| `elements.desert_single` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_horizontal` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_single_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_single_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_inner_top_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_inner_top_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_inner_bottom_left` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.desert_inner_bottom_right` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_inner` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_bottom_left` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.snow_bottom_right` | — | — | 56×60 → 64.0×64.0 | 1.143× | PASS |
| `elements.snow_pillar_top` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_pillar` | — | — | 54×60 → 64.0×64.0 | 1.185× | PASS |
| `elements.snow_pillar_bottom` | — | — | 54×60 → 64.0×64.0 | 1.185× | PASS |
| `elements.snow_single` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_horizontal` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS |
| `elements.snow_single_left` | — | — | 59×60 → 64.0×64.0 | 1.085× | PASS |
| `elements.snow_single_right` | — | — | 59×60 → 64.0×64.0 | 1.085× | PASS |
| `elements.snow_inner_top_left` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.snow_inner_top_right` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.snow_inner_bottom_left` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS |
| `elements.snow_inner_bottom_right` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS |
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
| `elements.grass_mask_0` | — | — | 57×59 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_1` | — | — | 57×59 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_2` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_3` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_4` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_5` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_6` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_7` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_8` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_9` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_10` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_11` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_12` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_13` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_14` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_15` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_19` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_23` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_27` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_31` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_38` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_39` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_46` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_47` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.grass_mask_55` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
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
| `elements.snow_mask_0` | — | — | 58×59 → 64.0×64.0 | 1.103× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_1` | — | — | 57×59 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_2` | — | — | 59×60 → 64.0×64.0 | 1.085× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_3` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_4` | — | — | 59×60 → 64.0×64.0 | 1.085× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_5` | — | — | 54×60 → 64.0×64.0 | 1.185× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_6` | — | — | 59×60 → 64.0×64.0 | 1.085× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_7` | — | — | 54×60 → 64.0×64.0 | 1.185× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_8` | — | — | 59×60 → 64.0×64.0 | 1.085× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_9` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_10` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_11` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_12` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_13` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_14` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_15` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_19` | — | — | 57×60 → 64.0×64.0 | 1.123× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_23` | — | — | 54×60 → 64.0×64.0 | 1.185× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_27` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_31` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_38` | — | — | 59×60 → 64.0×64.0 | 1.085× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_39` | — | — | 54×60 → 64.0×64.0 | 1.185× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_46` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_47` | — | — | 60×60 → 64.0×64.0 | 1.067× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
| `elements.snow_mask_55` | — | — | 54×60 → 64.0×64.0 | 1.185× | PASS; 47-mask autotile assembled from native 30px quadrants; no upsampling. |
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
| `elements.p_switch` | — | — | 82×91 → 64.0×64.0 | 0.780× | PASS; Real P-switch highlight cycle; this GIF never depresses. Existing pack key pswitch corresponds to requested p_switch. |
| `characters.luigi_small` | — | — | 76×108 → 49.0×69.7 | 0.645× | PASS; Authentic NSMB Wii raster captures shared by PolskyGamer (project 797092569); same-style fallback, NOT an NSMBU rip. Original ripper not stated by this collection. Distinct Fall capture; wallSlide holds the wall-jump capture. Skid reuses a run-transition pose; a separate braking capture was not found. |
| `items.mushroom` | — | — | 92×90 → 64.0×64.0 | 0.711× | PASS; Genuine 16-frame wobble cycle, not an emerge capture. Emerge motion must be supplied by gameplay. |
| `fx.coin_pop` | — | — | 52×60 → 48.0×56.0 | 0.933× | PASS; Actual 16-frame coin spin usable as the sprite of a coin-pop effect. Pop trajectory is renderer movement; no captured rise/burst claimed. |
| `fx.star` | — | — | 98×94 → 48.0×51.2 | 0.545× | PASS; Actual 21-frame Super Star wobble, usable as a decorative star effect. This is the power-up sprite, not an invincibility-particle rip. |
| `fx.brick_debris` | — | — | 44×43 → 28.8×28.8 | 0.670× | PASS; Four native fragment variants; select a piece for each particle. No brick was quartered or hand-painted to invent debris. |

## Animation frames

Opaque display dimensions include the real fraction of each fixed canvas occupied by the pose. Frame names resolve to exact source crops in slicing.json. The final column checks the shared opaque envelope against the requested display size; it cannot be improved by adding transparent padding.

| Sprite / frame | Native opaque px | Actual opaque display px | Content-envelope factor |
|---|---|---|---:|
| `elements.falling_block/falling_block_000` | 60×53 | 64.0×56.5 | 1.208× |
| `elements.saw/saw_000` | 149×149 | 96.0×96.0 | 0.644× |
| `elements.spring/spring_000` | 78×77 | 64.0×64.0 | 0.831× |
| `elements.conveyor_belt/conveyor_belt_000` | 64×57 | 64.0×57.0 | 1.000× |
| `elements.conveyor_belt/conveyor_belt_001` | 64×57 | 64.0×57.0 | 1.000× |
| `elements.conveyor_belt/conveyor_belt_002` | 64×57 | 64.0×57.0 | 1.000× |
| `elements.conveyor_belt/conveyor_belt_003` | 64×57 | 64.0×57.0 | 1.000× |
| `elements.conveyor_belt/conveyor_belt_004` | 64×57 | 64.0×57.0 | 1.000× |
| `elements.conveyor_belt/conveyor_belt_005` | 64×57 | 64.0×57.0 | 1.000× |
| `elements.conveyor_belt/conveyor_belt_006` | 64×57 | 64.0×57.0 | 1.000× |
| `elements.conveyor_belt/conveyor_belt_007` | 64×57 | 64.0×57.0 | 1.000× |
| `elements.chain_link/chain_link_0` | 92×92 | 16.0×16.0 | 0.174× |
| `elements.coin/coin_0` | 50×60 | 61.5×64.0 | 1.231× |
| `elements.coin/coin_1` | 52×60 | 64.0×64.0 | 1.231× |
| `elements.coin/coin_2` | 50×60 | 61.5×64.0 | 1.231× |
| `elements.coin/coin_3` | 46×60 | 56.6×64.0 | 1.231× |
| `elements.coin/coin_4` | 43×60 | 52.9×64.0 | 1.231× |
| `elements.coin/coin_5` | 36×60 | 44.3×64.0 | 1.231× |
| `elements.coin/coin_6` | 30×60 | 36.9×64.0 | 1.231× |
| `elements.coin/coin_7` | 22×60 | 27.1×64.0 | 1.231× |
| `elements.coin/coin_8` | 14×60 | 17.2×64.0 | 1.231× |
| `elements.coin/coin_9` | 22×60 | 27.1×64.0 | 1.231× |
| `elements.coin/coin_10` | 30×60 | 36.9×64.0 | 1.231× |
| `elements.coin/coin_11` | 36×60 | 44.3×64.0 | 1.231× |
| `elements.coin/coin_12` | 43×60 | 52.9×64.0 | 1.231× |
| `elements.coin/coin_13` | 46×60 | 56.6×64.0 | 1.231× |
| `elements.coin/coin_14` | 50×60 | 61.5×64.0 | 1.231× |
| `elements.coin/coin_15` | 52×60 | 64.0×64.0 | 1.231× |
| `elements.big_coin/big_coin_0` | 116×116 | 62.9×62.9 | 0.552× |
| `elements.big_coin/big_coin_1` | 116×116 | 62.9×62.9 | 0.552× |
| `elements.big_coin/big_coin_2` | 110×116 | 59.7×62.9 | 0.552× |
| `elements.big_coin/big_coin_3` | 98×116 | 53.2×62.9 | 0.552× |
| `elements.big_coin/big_coin_4` | 80×116 | 43.4×62.9 | 0.552× |
| `elements.big_coin/big_coin_5` | 60×116 | 32.5×62.9 | 0.552× |
| `elements.big_coin/big_coin_6` | 36×116 | 19.5×62.9 | 0.552× |
| `elements.big_coin/big_coin_7` | 36×116 | 19.5×62.9 | 0.552× |
| `elements.big_coin/big_coin_8` | 60×116 | 32.5×62.9 | 0.552× |
| `elements.big_coin/big_coin_9` | 80×116 | 43.4×62.9 | 0.552× |
| `elements.big_coin/big_coin_10` | 98×116 | 53.2×62.9 | 0.552× |
| `elements.big_coin/big_coin_11` | 110×116 | 59.7×62.9 | 0.552× |
| `elements.big_coin/big_coin_12` | 116×116 | 62.9×62.9 | 0.552× |
| `elements.powerup_dash/powerup_dash_0` | 180×186 | 58.8×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_1` | 180×186 | 58.8×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_2` | 180×184 | 58.8×63.3 | 0.344× |
| `elements.powerup_dash/powerup_dash_3` | 180×182 | 58.8×62.6 | 0.344× |
| `elements.powerup_dash/powerup_dash_4` | 188×178 | 61.4×61.2 | 0.344× |
| `elements.powerup_dash/powerup_dash_5` | 196×176 | 64.0×60.6 | 0.344× |
| `elements.powerup_dash/powerup_dash_6` | 196×174 | 64.0×59.9 | 0.344× |
| `elements.powerup_dash/powerup_dash_7` | 188×176 | 61.4×60.6 | 0.344× |
| `elements.powerup_dash/powerup_dash_8` | 184×180 | 60.1×61.9 | 0.344× |
| `elements.powerup_dash/powerup_dash_9` | 184×184 | 60.1×63.3 | 0.344× |
| `elements.powerup_dash/powerup_dash_10` | 184×186 | 60.1×64.0 | 0.344× |
| `elements.powerup_dash/powerup_dash_11` | 180×186 | 58.8×64.0 | 0.344× |
| `elements.start/start_0` | 76×92 | 64.0×64.0 | 0.842× |
| `elements.start/start_1` | 76×92 | 64.0×64.0 | 0.842× |
| `elements.start/start_2` | 76×92 | 64.0×64.0 | 0.842× |
| `elements.start/start_3` | 76×92 | 64.0×64.0 | 0.842× |
| `elements.start/start_4` | 75×91 | 63.2×63.3 | 0.842× |
| `elements.start/start_5` | 76×92 | 64.0×64.0 | 0.842× |
| `elements.checkpoint/checkpoint_000` | 106×171 | 80.0×129.3 | 0.756× |
| `elements.door/door_000` | 78×154 | 64.0×128.0 | 0.831× |
| `elements.door/door_001` | 78×154 | 64.0×128.0 | 0.831× |
| `elements.door/door_002` | 78×154 | 64.0×128.0 | 0.831× |
| `elements.door/door_003` | 78×154 | 64.0×128.0 | 0.831× |
| `elements.door/door_004` | 78×154 | 64.0×128.0 | 0.831× |
| `elements.door/door_005` | 78×154 | 64.0×128.0 | 0.831× |
| `elements.door_open/door_open_0` | 156×308 | 64.0×128.0 | 0.416× |
| `elements.switch/switch_000` | 60×60 | 64.0×64.0 | 1.067× |
| `elements.switch/switch_001` | 60×60 | 64.0×64.0 | 1.067× |
| `elements.switch_on/switch_on_0` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.switch_block/switch_block_000` | 60×60 | 64.0×64.0 | 1.067× |
| `elements.switch_block/switch_block_001` | 54×54 | 57.6×57.6 | 1.067× |
| `elements.switch_block/switch_block_002` | 60×60 | 64.0×64.0 | 1.067× |
| `elements.switch_block/switch_block_003` | 54×54 | 57.6×57.6 | 1.067× |
| `elements.pswitch/pswitch_000` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.pswitch/pswitch_001` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.pswitch/pswitch_002` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.pswitch/pswitch_003` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.pswitch/pswitch_004` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.pswitch/pswitch_005` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.pswitch/pswitch_006` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.pswitch/pswitch_007` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.pswitch/pswitch_008` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.pswitch/pswitch_009` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.pswitch/pswitch_010` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.pswitch/pswitch_011` | 82×91 | 64.0×64.0 | 0.780× |
| `elements.goal/goal_000` | 312×1015 | 98.6×320.0 | 0.316× |
| `elements.pipe/pipe_000` | 120×120 | 128.0×128.0 | 1.067× |
| `elements.walker/walker_0` | 104×122 | 64.0×64.0 | 0.615× |
| `elements.shell/shell_0` | 174×274 | 47.6×95.3 | 0.348× |
| `elements.shell/shell_1` | 234×268 | 64.0×93.2 | 0.348× |
| `elements.shell/shell_2` | 206×276 | 56.3×96.0 | 0.348× |
| `elements.shell/shell_3` | 194×264 | 53.1×91.8 | 0.348× |
| `elements.shell/shell_4` | 164×148 | 44.9×51.5 | 0.348× |
| `elements.shell/shell_5` | 164×148 | 44.9×51.5 | 0.348× |
| `elements.shell/shell_6` | 166×148 | 45.4×51.5 | 0.348× |
| `elements.shell/shell_7` | 160×148 | 43.8×51.5 | 0.348× |
| `elements.shell/shell_8` | 166×148 | 45.4×51.5 | 0.348× |
| `elements.shell/shell_9` | 166×148 | 45.4×51.5 | 0.348× |
| `elements.flyer/flyer_0` | 85×97 | 64.0×64.0 | 0.753× |
| `elements.jumper/jumper_0` | 182×184 | 61.3×64.0 | 0.348× |
| `elements.jumper/jumper_1` | 176×178 | 59.3×61.9 | 0.348× |
| `elements.jumper/jumper_2` | 176×172 | 59.3×59.8 | 0.348× |
| `elements.jumper/jumper_3` | 182×170 | 61.3×59.1 | 0.348× |
| `elements.jumper/jumper_4` | 184×176 | 62.0×61.2 | 0.348× |
| `elements.jumper/jumper_5` | 176×184 | 59.3×64.0 | 0.348× |
| `elements.jumper/jumper_6` | 190×182 | 64.0×63.3 | 0.348× |
| `elements.jumper/jumper_7` | 184×180 | 62.0×62.6 | 0.348× |
| `elements.jumper/jumper_8` | 174×170 | 58.6×59.1 | 0.348× |
| `elements.jumper/jumper_9` | 178×170 | 60.0×59.1 | 0.348× |
| `elements.jumper/jumper_10` | 180×176 | 60.6×61.2 | 0.348× |
| `elements.jumper/jumper_11` | 186×184 | 62.7×64.0 | 0.348× |
| `elements.cannon/cannon_000` | 78×154 | 64.0×128.0 | 0.831× |
| `elements.bullet_bill/bullet_bill_0` | 204×128 | 64.0×62.1 | 0.485× |
| `elements.bullet_bill/bullet_bill_1` | 204×128 | 64.0×62.1 | 0.485× |
| `elements.bullet_bill/bullet_bill_2` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_3` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_4` | 204×128 | 64.0×62.1 | 0.485× |
| `elements.bullet_bill/bullet_bill_5` | 204×128 | 64.0×62.1 | 0.485× |
| `elements.bullet_bill/bullet_bill_6` | 204×128 | 64.0×62.1 | 0.485× |
| `elements.bullet_bill/bullet_bill_7` | 204×128 | 64.0×62.1 | 0.485× |
| `elements.bullet_bill/bullet_bill_8` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_9` | 204×132 | 64.0×64.0 | 0.485× |
| `elements.bullet_bill/bullet_bill_10` | 204×128 | 64.0×62.1 | 0.485× |
| `elements.bullet_bill/bullet_bill_11` | 204×128 | 64.0×62.1 | 0.485× |
| `elements.mushroom/mushroom_000` | 88×88 | 61.2×62.6 | 0.711× |
| `elements.mushroom/mushroom_001` | 86×90 | 59.8×64.0 | 0.711× |
| `elements.mushroom/mushroom_002` | 86×90 | 59.8×64.0 | 0.711× |
| `elements.mushroom/mushroom_003` | 86×90 | 59.8×64.0 | 0.711× |
| `elements.mushroom/mushroom_004` | 86×90 | 59.8×64.0 | 0.711× |
| `elements.mushroom/mushroom_005` | 86×89 | 59.8×63.3 | 0.711× |
| `elements.mushroom/mushroom_006` | 88×88 | 61.2×62.6 | 0.711× |
| `elements.mushroom/mushroom_007` | 88×87 | 61.2×61.9 | 0.711× |
| `elements.mushroom/mushroom_008` | 90×86 | 62.6×61.2 | 0.711× |
| `elements.mushroom/mushroom_009` | 90×85 | 62.6×60.4 | 0.711× |
| `elements.mushroom/mushroom_010` | 92×85 | 64.0×60.4 | 0.711× |
| `elements.mushroom/mushroom_011` | 92×84 | 64.0×59.7 | 0.711× |
| `elements.mushroom/mushroom_012` | 90×85 | 62.6×60.4 | 0.711× |
| `elements.mushroom/mushroom_013` | 90×86 | 62.6×61.2 | 0.711× |
| `elements.mushroom/mushroom_014` | 88×87 | 61.2×61.9 | 0.711× |
| `elements.mushroom/mushroom_015` | 88×88 | 61.2×62.6 | 0.711× |
| `elements.brick/brick_000` | 120×120 | 64.0×64.0 | 0.533× |
| `elements.question/question_block_000` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_001` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_002` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_003` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_004` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_005` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_006` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_007` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_008` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_009` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_010` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_011` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_012` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_013` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_014` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_015` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.question/question_block_016` | 64×64 | 64.0×64.0 | 1.000× |
| `elements.conveyor/conveyor_belt_0` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor/conveyor_belt_1` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor/conveyor_belt_2` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor/conveyor_belt_3` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor/conveyor_belt_4` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor/conveyor_belt_5` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor/conveyor_belt_6` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.conveyor/conveyor_belt_7` | 128×114 | 64.0×64.0 | 0.561× |
| `elements.switch-block/switch_block_0` | 64×64 | 64.0×64.0 | 1.000× |
| `characters.mario/mario_0` | 110×160 | 82.5×120.0 | 0.750× |
| `characters.mario/mario_1` | 114×160 | 85.5×120.0 | 0.750× |
| `characters.mario/mario_2` | 97×160 | 72.7×120.0 | 0.750× |
| `characters.mario/mario_3` | 94×160 | 70.5×120.0 | 0.750× |
| `characters.mario/mario_4` | 94×160 | 70.5×120.0 | 0.750× |
| `characters.mario/mario_5` | 92×160 | 69.0×120.0 | 0.750× |
| `characters.mario/mario_6` | 100×160 | 75.0×120.0 | 0.750× |
| `characters.mario/mario_7` | 120×160 | 90.0×120.0 | 0.750× |
| `characters.mario/mario_8` | 158×160 | 118.5×120.0 | 0.750× |
| `characters.mario/mario_9` | 139×160 | 104.2×120.0 | 0.750× |
| `characters.mario/mario_10` | 181×160 | 135.7×120.0 | 0.750× |
| `characters.mario/mario_11` | 114×150 | 85.5×112.5 | 0.750× |
| `characters.mario/mario_12` | 83×160 | 62.2×120.0 | 0.750× |
| `characters.mario/mario_13` | 107×160 | 80.2×120.0 | 0.750× |
| `characters.mario/mario_14` | 77×160 | 57.7×120.0 | 0.750× |
| `characters.mario/mario_15` | 77×160 | 57.7×120.0 | 0.750× |
| `characters.mario/mario_16` | 93×96 | 69.7×72.0 | 0.750× |
| `characters.mario/mario_17` | 70×160 | 52.5×120.0 | 0.750× |
| `characters.mario/mario_18` | 85×85 | 63.7×63.8 | 0.750× |
| `characters.mario/mario_19` | 84×90 | 63.0×67.5 | 0.750× |
| `characters.mario/mario_20` | 84×85 | 63.0×63.8 | 0.750× |
| `characters.mario_small/mario_small_0` | 56×75 | 44.8×60.0 | 0.800× |
| `characters.mario_small/mario_small_1` | 50×73 | 40.0×58.4 | 0.800× |
| `characters.mario_small/mario_small_2` | 50×75 | 40.0×60.0 | 0.800× |
| `characters.mario_small/mario_small_3` | 58×79 | 46.4×63.2 | 0.800× |
| `characters.mario_small/mario_small_4` | 58×79 | 46.4×63.2 | 0.800× |
| `characters.mario_small/mario_small_5` | 52×85 | 41.6×68.0 | 0.800× |
| `characters.mario_small/mario_small_6` | 54×75 | 43.2×60.0 | 0.800× |
| `characters.mario_small/mario_small_7` | 62×71 | 49.6×56.8 | 0.800× |
| `characters.mario_small/mario_small_8` | 62×74 | 49.6×59.2 | 0.800× |
| `characters.mario_small/mario_small_9` | 48×63 | 38.4×50.4 | 0.800× |
| `characters.mario_small/mario_small_10` | 62×61 | 49.6×48.8 | 0.800× |
| `characters.mario_small/mario_small_11` | 44×87 | 35.2×69.6 | 0.800× |
| `characters.mario_small/mario_small_12` | 52×87 | 41.6×69.6 | 0.800× |
| `characters.mario_small/mario_small_13` | 52×85 | 41.6×68.0 | 0.800× |
| `characters.mario_small/mario_small_14` | 48×82 | 38.4×65.6 | 0.800× |
| `characters.mario_small/mario_small_15` | 44×48 | 35.2×38.4 | 0.800× |
| `characters.mario_small/mario_small_16` | 52×79 | 41.6×63.2 | 0.800× |
| `characters.mario_small/mario_small_17` | 62×72 | 49.6×57.6 | 0.800× |
| `characters.mario_small/mario_small_18` | 64×73 | 51.2×58.4 | 0.800× |
| `characters.luigi/luigi_0` | 80×144 | 66.7×120.0 | 0.833× |
| `characters.luigi/luigi_1` | 74×142 | 61.7×118.3 | 0.833× |
| `characters.luigi/luigi_2` | 68×143 | 56.7×119.2 | 0.833× |
| `characters.luigi/luigi_3` | 57×136 | 47.5×113.3 | 0.833× |
| `characters.luigi/luigi_4` | 83×132 | 69.2×110.0 | 0.833× |
| `characters.luigi/luigi_5` | 73×132 | 60.8×110.0 | 0.833× |
| `characters.luigi/luigi_6` | 78×134 | 65.0×111.7 | 0.833× |
| `characters.luigi/luigi_7` | 98×121 | 81.7×100.8 | 0.833× |
| `characters.luigi/luigi_8` | 65×132 | 54.2×110.0 | 0.833× |
| `characters.luigi/luigi_9` | 98×121 | 81.7×100.8 | 0.833× |
| `characters.luigi/luigi_10` | 53×137 | 44.2×114.2 | 0.833× |
| `characters.luigi/luigi_11` | 63×135 | 52.5×112.5 | 0.833× |
| `characters.luigi/luigi_12` | 76×133 | 63.3×110.8 | 0.833× |
| `characters.luigi/luigi_13` | 61×126 | 50.8×105.0 | 0.833× |
| `characters.luigi/luigi_14` | 64×85 | 53.3×70.8 | 0.833× |
| `characters.luigi/luigi_15` | 68×137 | 56.7×114.2 | 0.833× |
| `characters.luigi/luigi_16` | 64×87 | 53.3×72.5 | 0.833× |
| `characters.luigi/luigi_17` | 70×88 | 58.3×73.3 | 0.833× |
| `characters.luigi/luigi_18` | 52×76 | 43.3×63.3 | 0.833× |
| `characters.luigi_small/luigi_small_0` | 64×93 | 41.3×60.0 | 0.645× |
| `characters.luigi_small/luigi_small_1` | 62×91 | 40.0×58.7 | 0.645× |
| `characters.luigi_small/luigi_small_2` | 60×91 | 38.7×58.7 | 0.645× |
| `characters.luigi_small/luigi_small_3` | 58×94 | 37.4×60.6 | 0.645× |
| `characters.luigi_small/luigi_small_4` | 66×91 | 42.6×58.7 | 0.645× |
| `characters.luigi_small/luigi_small_5` | 58×94 | 37.4×60.6 | 0.645× |
| `characters.luigi_small/luigi_small_6` | 66×94 | 42.6×60.6 | 0.645× |
| `characters.luigi_small/luigi_small_7` | 68×98 | 43.9×63.2 | 0.645× |
| `characters.luigi_small/luigi_small_8` | 76×94 | 49.0×60.6 | 0.645× |
| `characters.luigi_small/luigi_small_9` | 68×98 | 43.9×63.2 | 0.645× |
| `characters.luigi_small/luigi_small_10` | 56×105 | 36.1×67.7 | 0.645× |
| `characters.luigi_small/luigi_small_11` | 58×108 | 37.4×69.7 | 0.645× |
| `characters.luigi_small/luigi_small_12` | 66×106 | 42.6×68.4 | 0.645× |
| `characters.luigi_small/luigi_small_13` | 64×104 | 41.3×67.1 | 0.645× |
| `characters.luigi_small/luigi_small_14` | 62×65 | 40.0×41.9 | 0.645× |
| `characters.luigi_small/luigi_small_15` | 56×97 | 36.1×62.6 | 0.645× |
| `characters.luigi_small/luigi_small_16` | 64×87 | 41.3×56.1 | 0.645× |
| `characters.luigi_small/luigi_small_17` | 70×88 | 45.2×56.8 | 0.645× |
| `characters.luigi_small/luigi_small_18` | 52×76 | 33.5×49.0 | 0.645× |
| `fx.coin_pop/coin_pop_000` | 50×60 | 46.2×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_001` | 52×60 | 48.0×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_002` | 50×60 | 46.2×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_003` | 46×60 | 42.5×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_004` | 43×60 | 39.7×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_005` | 36×60 | 33.2×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_006` | 30×60 | 27.7×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_007` | 22×60 | 20.3×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_008` | 14×60 | 12.9×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_009` | 22×60 | 20.3×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_010` | 30×60 | 27.7×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_011` | 36×60 | 33.2×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_012` | 43×60 | 39.7×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_013` | 46×60 | 42.5×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_014` | 50×60 | 46.2×56.0 | 0.933× |
| `fx.coin_pop/coin_pop_015` | 52×60 | 48.0×56.0 | 0.933× |
| `fx.star/star_000` | 90×93 | 44.1×50.7 | 0.545× |
| `fx.star/star_001` | 90×94 | 44.1×51.2 | 0.545× |
| `fx.star/star_002` | 90×93 | 44.1×50.7 | 0.545× |
| `fx.star/star_003` | 90×92 | 44.1×50.1 | 0.545× |
| `fx.star/star_004` | 90×92 | 44.1×50.1 | 0.545× |
| `fx.star/star_005` | 90×91 | 44.1×49.6 | 0.545× |
| `fx.star/star_006` | 92×89 | 45.1×48.5 | 0.545× |
| `fx.star/star_007` | 94×89 | 46.0×48.5 | 0.545× |
| `fx.star/star_008` | 96×88 | 47.0×47.9 | 0.545× |
| `fx.star/star_009` | 98×88 | 48.0×47.9 | 0.545× |
| `fx.star/star_010` | 98×87 | 48.0×47.4 | 0.545× |
| `fx.star/star_011` | 98×87 | 48.0×47.4 | 0.545× |
| `fx.star/star_012` | 96×88 | 47.0×47.9 | 0.545× |
| `fx.star/star_013` | 94×88 | 46.0×47.9 | 0.545× |
| `fx.star/star_014` | 94×89 | 46.0×48.5 | 0.545× |
| `fx.star/star_015` | 92×90 | 45.1×49.0 | 0.545× |
| `fx.star/star_016` | 92×92 | 45.1×50.1 | 0.545× |
| `fx.star/star_017` | 92×92 | 45.1×50.1 | 0.545× |
| `fx.star/star_018` | 92×93 | 45.1×50.7 | 0.545× |
| `fx.star/star_019` | 92×93 | 45.1×50.7 | 0.545× |
| `fx.star/star_020` | 90×93 | 44.1×50.7 | 0.545× |
| `fx.brick_debris/brick_debris_000` | 30×32 | 13.5×14.4 | 0.670× |
| `fx.brick_debris/brick_debris_001` | 34×33 | 15.3×14.8 | 0.670× |
| `fx.brick_debris/brick_debris_002` | 37×43 | 16.7×19.4 | 0.670× |
| `fx.brick_debris/brick_debris_003` | 44×35 | 19.8×15.8 | 0.670× |

## Result

- Historical canvas baseline: **50/159** entries above 1.25×.
- Current opaque-content audit: **0/411** entries above 1.25×.
- Remaining semantic substitutions are disclosed in README.md and RESOLUTION_REPORT.md.
