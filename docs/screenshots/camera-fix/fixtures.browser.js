async (page) => {
 await page.bringToFront();
 const pack='PACK',mode='MODE',label='LABEL';
 await page.goto('http://127.0.0.1:8080/'+(mode==='play'?'play/1':'editor'));
 await page.evaluate(p=>localStorage.setItem('realmforge:asset-pack',p),pack);await page.reload();
 await page.waitForFunction(()=>window.__rfGame?.scene.getScenes(true).some(s=>s.scene.key==='PlayScene'||s.scene.key==='EditorScene'));
 if(mode==='play')await page.getByRole('button',{name:'Start run',exact:true}).click();
 const kind='KIND';
 await page.evaluate(async({mode,kind})=>{
  const fixture=await (await fetch('/@fs/Users/slimane/realmforge/docs/screenshots/camera-fix/fixture.level.v1.json')).json();
  fixture.meta.name='Camera regression '+kind;
  if(kind==='fall'){fixture.layers.terrain='0*2700,1*300';fixture.spawn.y=3;}
  if(kind==='forms'){fixture.entities.push({id:3,type:'mushroom',x:20,y:23,props:{direction:-1,speed:0.5}});}
  if(kind==='spring'){fixture.spawn.y=21;fixture.entities.push({id:2,type:'spring',x:16,y:23,props:{launch:9}});}
  const {EventBus}=await import('/src/game/EventBus.ts');
  if(mode==='play')window.__play.scene.restart({level:fixture,from:'play',levelId:null});
  else localStorage.setItem('realmforge:editor:autosave:v1',JSON.stringify(fixture));
 },{mode,kind});
 if(mode==='editor'){await page.reload();await page.waitForFunction(()=>window.__rfGame?.scene.getScenes(true).some(s=>s.scene.key==='EditorScene'&&s.doc.meta.name==='Camera regression '+'KIND'));await page.keyboard.press('t');}
 await page.waitForFunction(()=>window.__play?.scene.isActive()&&window.__play.doc.meta.name==='Camera regression '+ 'KIND'&&window.__play.sequence===null&&!window.__play.paused);
 if(kind!=='fall'&&kind!=='spring')await page.waitForTimeout(600);
 if(kind==='slope')await page.evaluate(()=>{
  const s=window.__play,verts=[{x:18*64,y:24*64},{x:28*64,y:22*64},{x:28*64,y:24*64}];
  const body=s.matter.add.fromVertices((18+28+28)/3*64,(24+22+24)/3*64,verts,{isStatic:true,collisionFilter:{category:4,mask:0xffff,group:0}});
  body.label='Camera verification ramp';s.add.graphics().fillStyle(0xffc83d).fillPoints(body.vertices,true).setDepth(1);
 });
  await page.evaluate(async()=>{
    const s=window.__play,cam=s.cameras.main,canvas=s.game.canvas;
    const {EventBus}=await import('/src/game/EventBus.ts');
    const factors=(await import('/src/game/assets/registry.ts')).themeLayers(s.doc.meta.theme).map(l=>l.scrollFactor);
    const layers=s.children.list.filter(v=>v.type==='TileSprite'&&v.depth<0);
    const e=window.__cameraCapture={samples:[],phase:'standing',factors,counts:{hud:0,resize:0,canvasMutations:0,canvasReplacements:0,backgroundSize:0,backgroundScale:0,internalCanvasResizes:0,uploads:0},events:[]};
    EventBus.on('play:hud',()=>e.counts.hud++);
    s.scale.on('resize',()=>e.counts.resize++);
    const mo=new MutationObserver(ms=>{for(const m of ms) if(m.type==='attributes'&&(m.attributeName==='width'||m.attributeName==='height'))e.counts.canvasMutations++;else if(m.type==='childList'&&[...m.addedNodes,...m.removedNodes].some(n=>n.nodeName==='CANVAS'))e.counts.canvasReplacements++;});
    mo.observe(canvas.parentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['width','height']});
    const upload=s.game.renderer.canvasToTexture;
    s.game.renderer.canvasToTexture=function(source,...args){if(layers.some(l=>l.fillCanvas===source))e.counts.uploads++;return upload.call(this,source,...args)};
    for(const layer of layers){const orig=layer.updateCanvas;layer.updateCanvas=function(...args){if(this.canvas.width!==this.width||this.canvas.height!==this.height)e.counts.internalCanvasResizes++;return orig.apply(this,args)}}
    for(const layer of layers)for(const name of ['setSize','setTileScale']){const orig=layer[name];layer[name]=function(...args){e.counts[name==='setSize'?'backgroundSize':'backgroundScale']++;return orig.apply(this,args)}}
    const pre=cam.preRender;
    cam.preRender=function(...args){e.before={x:this.scrollX,y:this.scrollY};return pre.apply(this,args)};
    s.events.on('render',()=>{
      const b=s.player.body,hull=b.parts[1]??b,r=canvas.getBoundingClientRect();
      e.samples.push({at:performance.now(),f:s.frame,phase:e.phase,scroll:{x:cam.scrollX,y:cam.scrollY},viewport:{w:cam.width,h:cam.height},preScroll:e.before,zoom:cam.zoom,round:cam.roundPixels,renderRound:cam.renderRoundPixels,visualTarget:cam._follow===s.playerSprite,target:cam._follow&&{x:cam._follow.x,y:cam._follow.y},physical:{x:b.position.x,y:b.position.y,hullY:hull.position.y,foot:s.player.sensors.foot.position.y,boundsFoot:hull.bounds.max.y,height:hull.bounds.max.y-hull.bounds.min.y,physicalHeight:s.player.sensors.foot.position.y-s.player.sensors.head.position.y,vy:s.player.state.vy,vx:s.player.state.vx,mode:s.player.state.mode,grounded:s.player.state.grounded},sprite:{x:s.playerSprite.x,y:s.playerSprite.y,sx:s.playerSprite.scaleX,sy:s.playerSprite.scaleY,height:s.playerSprite.displayHeight,frame:s.playerSprite.frame.name},canvas:{x:r.x,y:r.y,w:r.width,h:r.height,width:canvas.width,height:canvas.height,same:canvas===document.querySelector('canvas')&&s.game===window.__rfGame},layers:layers.map(l=>({key:l.texture.key,x:l.x,y:l.y,w:l.width,h:l.height,cw:l.canvas.width,ch:l.canvas.height,scale:l.tileScaleX,tileX:l.tilePositionX,tileY:l.tilePositionY})),counts:{...e.counts},shake:cam.shakeEffect.isRunning});
    });
  });

 const phase=async(name,ms,keys=[])=>{
  await page.evaluate(n=>window.__cameraCapture.phase=n,name);
  for(const k of keys)await page.keyboard.down(k);
  await page.waitForTimeout(ms);
  await page.screenshot({path:`/Users/slimane/realmforge/docs/screenshots/camera-fix/${label}-${pack}-${mode}-${kind}-${name}.png`});
  for(const k of keys.reverse())await page.keyboard.up(k);
 };
 if(kind==='flat'){
  await phase('standing',400);await phase('walk',1400,['ArrowRight']);await phase('run',700,['ArrowRight','Shift']);
  await phase('jump',300,['ArrowRight','Shift','Space']);await phase('land',1000);await phase('reverse',500,['ArrowLeft','Shift']);await phase('settled',1000);
  if(mode==='play'){
   const before=await page.evaluate(()=>({f:window.__play.frame,game:!!window.__rfGame}));
   await page.getByRole('button',{name:'Pause',exact:true}).click();await page.waitForTimeout(250);
   await page.getByRole('dialog').getByRole('button',{name:'Resume',exact:true}).click();
   await page.evaluate(b=>window.__cameraCapture.events.push({name:'react-pause-resume',before:b,after:window.__play.frame}),before);
  }
  await page.setViewportSize({width:1100,height:850});await phase('resize-small',600,['ArrowRight']);
  await page.setViewportSize({width:1440,height:1000});await phase('resize-restored',600,['ArrowRight']);
 }else if(kind==='slope'){
  await phase('slope-up',2300,['ArrowRight']);await phase('slope-reverse',1800,['ArrowLeft']);await phase('slope-jump',250,['Space']);await phase('slope-land',900);
 }else if(kind==='forms'){await phase('pickup-grow',900,['ArrowRight']);await phase('form-jump',300,['Space']);await phase('form-land',1000);}
 else if(kind==='fall'){await phase('vertical-fall',2100);await phase('vertical-land',500);}
 else if(kind==='spring'){await phase('vertical-launch',650,['Space']);await phase('vertical-return',1400,['ArrowRight']);}
  const data=await page.evaluate(()=>JSON.parse(JSON.stringify(window.__cameraCapture)));
  const range=a=>Math.max(...a)-Math.min(...a);
  const summary={pack,mode,label,count:data.samples.length,counts:data.counts,phases:{}};
  for(const phase of [...new Set(data.samples.map(s=>s.phase))]){const a=data.samples.filter(s=>s.phase===phase);summary.phases[phase]={scrollX:range(a.map(s=>s.scroll.x)),scrollY:range(a.map(s=>s.scroll.y)),foot:range(a.map(s=>s.physical.foot)),height:range(a.map(s=>s.physical.height)),maxSpriteFootError:Math.max(...a.map(s=>Math.abs(s.sprite.y-s.physical.foot))),maxParallaxError:Math.max(...a.flatMap(s=>s.layers.map((l,i)=>Math.abs(l.tileX*l.scale-(label==='baseline'?0:((s.viewport?.w??s.layers[0].x*2)-l.w)/2)-s.scroll.x*data.factors[i])))),canvasSizes:[...new Set(a.map(s=>JSON.stringify(s.canvas)))],modes:[...new Set(a.map(s=>s.physical.mode))]};}
  return {summary,data};
}
