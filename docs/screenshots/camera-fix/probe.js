async (page) => {
  // Run through playwright-cli run-code; observation only, real keyboard drives Matter.
  await page.goto('http://127.0.0.1:8080/play/1');
  await page.waitForFunction(() => !!window.__play);
  await page.getByRole('button', { name: 'Start run', exact: true }).click();
  const fixture = await page.evaluate(async () => (await fetch('/@fs/Users/slimane/realmforge/docs/screenshots/camera-fix/fixture.level.v1.json')).json()).catch(async () => page.evaluate(async () => (await fetch('/@fs/Users/slimane/realmforge/docs/screenshots/camera-fix/fixture.level.v1.json')).json()));
  await page.keyboard.up('ArrowRight'); await page.keyboard.up('Space');
  await page.evaluate(fixture => window.__play.scene.restart({ level: fixture, from: 'play', levelId: null }), fixture);
  await page.waitForFunction(() => window.__play.sequence === null && !window.__play.paused);
  await page.waitForFunction(() => window.__play.frame > 45);
  await page.evaluate(async () => {
    const factors = (await import('/src/game/assets/registry.ts')).themeLayers('grass').map(l=>l.scrollFactor);
    const s = window.__play, cam = s.cameras.main, canvas = s.game.canvas;
    const layers = s.children.list.filter(v => v.type === 'TileSprite');
    const e = window.__cameraEvidence = { factors, samples: [], inputs: [], phase: 'idle', start: s.frame, counts: {size:0, tileScale:0, canvasResize:0, uploads:0}, shakes:[] };
    for (const v of layers) for (const name of ['setSize','setTileScale','updateCanvas']) {
      const original = v[name];
      v[name] = function(...args) {
        if (name === 'setSize') e.counts.size++;
        if (name === 'setTileScale') e.counts.tileScale++;
        if (name === 'updateCanvas' && (this.canvas.width !== this.width || this.canvas.height !== this.height)) e.counts.canvasResize++;
        return original.apply(this,args);
      };
    }
    const renderer = s.game.renderer, upload = renderer.canvasToTexture;
    renderer.canvasToTexture = function(source, ...args) {
      if (layers.some(v => v.fillCanvas === source)) e.counts.uploads++;
      return upload.call(this,source,...args);
    };
    const shake = cam.shake;
    cam.shake = function(...args) { e.shakes.push({f:s.frame,args}); return shake.apply(this,args); };
    const preRender = cam.preRender;
    cam.preRender = function(...args) { e.preScroll = {x:this.scrollX,y:this.scrollY}; return preRender.apply(this,args); };
    s.events.on('render', () => {
      const hull = s.player.body.parts[1] ?? s.player.body, r = canvas.getBoundingClientRect();
      e.samples.push({f:s.frame,at:performance.now(),phase:e.phase,scroll:{x:cam.scrollX,y:cam.scrollY},preScroll:e.preScroll,zoom:cam.zoom,round:cam.roundPixels,renderRound:cam.renderRoundPixels,
        target:{x:cam._follow?.x,y:cam._follow?.y,visual:cam._follow===s.playerSprite},
        input:{...s.currentInput},keys:Object.fromEntries(Object.entries(s.keys).map(([k,v])=>[k,v.isDown])),physics:{x:hull.position.x,y:hull.position.y,sensorFoot:s.player.sensors.foot.position.y,foot:hull.bounds.max.y,mode:s.player.state.mode,vy:s.player.state.vy},
        sprite:{x:s.playerSprite.x,y:s.playerSprite.y,frame:s.playerSprite.frame.name},
        shake:cam.shakeEffect.isRunning, matrix:Array.from(cam.matrix.matrix),
        canvas:{x:r.x,y:r.y,w:r.width,h:r.height,width:canvas.width,height:canvas.height,same:canvas===s.game.canvas&&canvas===document.querySelector('canvas')},
        layers:layers.map(v=>({key:v.texture.key,x:v.x,y:v.y,w:v.width,h:v.height,cw:v.canvas.width,ch:v.canvas.height,scale:v.tileScaleX,tileX:v.tilePositionX,tileY:v.tilePositionY,dirty:v.dirty})),counts:{...e.counts}});
    });
    e.restore = () => { renderer.canvasToTexture = upload; };
  });
  const phase = async (name, frames, keys=[]) => {
    const start = await page.evaluate(name => {window.__cameraEvidence.phase=name; return window.__play.frame;},name);
    for(const key of keys) {await page.keyboard.down(key); await page.evaluate(key=>window.__cameraEvidence.inputs.push({f:window.__play.frame,key,down:true}),key);}
    await page.waitForFunction(end => window.__play.frame >= end, start+frames, {polling:'raf'});
    for(const key of [...keys].reverse()) {await page.keyboard.up(key); await page.evaluate(key=>window.__cameraEvidence.inputs.push({f:window.__play.frame,key,down:false}),key);}
  };
  await phase('idle',30);
  await phase('walk',100,['ArrowRight']);
  await phase('walk-settle',30);
  await phase('jump',22,['Space']);
  await phase('landing',95);
  await phase('moving-jump',22,['ArrowRight','Space']);
  await phase('moving-landing',95);
  await phase('idle-end',30);
  return page.evaluate(() => {
    const e=window.__cameraEvidence; e.restore(); delete e.restore;
    const range=(a)=>Math.max(...a)-Math.min(...a);
    const summary={frames:e.samples.length,shakes:e.shakes,counts:e.counts,phases:{}};
    for(const phase of new Set(e.samples.map(s=>s.phase))) {
      const a=e.samples.filter(s=>s.phase===phase);
      summary.phases[phase]={frames:a.length,scrollXRange:range(a.map(s=>s.scroll.x)),scrollYRange:range(a.map(s=>s.scroll.y)),footRange:range(a.map(s=>s.physics.foot)),visualFeetOffsetRange:range(a.map(s=>s.sprite.y-s.physics.foot)),maxVisualVsPhysicalFoot:Math.max(...a.map(s=>Math.abs(s.sprite.y-s.physics.sensorFoot))),
        maxParallaxError:Math.max(...a.flatMap(s=>s.layers.map((l,i)=>Math.abs(l.tileX*l.scale-s.scroll.x*e.factors[i])))),
        maxScrollStep:Math.max(...a.map(s=>Math.abs(s.scroll.x-s.preScroll.x))),canvasBounds:new Set(a.map(s=>JSON.stringify(s.canvas))).size};
    }
    return {summary,evidence:e};
  });
}
