# -*- coding: utf-8 -*-
"""Concrete tools (putting off less, managing time), "what is hard for me
now?", notes, and the don't-forget strip on Today."""

JS_TOOLS2 = r"""
/* ================= concrete tools =================
   Every tool looks the same: why it helps, three steps, an example for the
   user's age, one action, and at the end "did it help?" - which feeds the
   tool of the day. */
function ageK(){ var n=Number(P.age); return n && n<=12 ? 'k' : n && n<=17 ? 't' : 'a'; }
var TL2={
  five:   {icon:'zap',      v:'init',  m:5,  ex:1, kind:'timer'},
  tiny:   {icon:'flag',     v:'init',  m:2,  ex:1, kind:'tiny'},
  two:    {icon:'check',    v:'init',  m:2,  ex:1, kind:'timer'},
  frog:   {icon:'target',   v:'init',  m:1,  ex:0, kind:'frog'},
  stuck:  {icon:'help',     v:'init',  m:2,  ex:0, kind:'stuck'},
  ifthen: {icon:'clock',    v:'init',  m:2,  ex:1, kind:'ifthen'},
  top3:   {icon:'star',     v:'ahead', m:3,  ex:0, kind:'top3'},
  focus:  {icon:'clock',    v:'ahead', m:25, ex:0, kind:'focus'},
  matrix: {icon:'target',   v:'ahead', m:3,  ex:0, kind:'matrix'},
  blocks: {icon:'calendar', v:'ahead', m:3,  ex:0, kind:'blocks'},
  rocks:  {icon:'gem',      v:'ahead', m:3,  ex:0, kind:'rocks'},
  ground: {icon:'seedling', v:'pause', m:2, ex:0, kind:'seq', seq:['5','4','3','2','1']},
  stop:   {icon:'shield',   v:'pause', m:1, ex:0, kind:'seq', seq:['1','2','3','4']},
  name:   {icon:'face',     v:'pause', m:1, ex:0, kind:'name'},
  move:   {icon:'activity', v:'pause', m:1, ex:0, kind:'timer'},
  therm:  {icon:'gauge',    v:'pause', m:1, ex:0, kind:'therm'},
  calmbox:{icon:'gift',     v:'pause', m:2, ex:0, kind:'calmbox'},
  phone:  {icon:'zap',      v:'init',  m:20, ex:0, kind:'timer'},
  draft:  {icon:'edit',     v:'init',  m:10, ex:0, kind:'timer'},
  pros:   {icon:'target',   v:'choose', m:5, dex:1, kind:'pros'},
  ten:    {icon:'clock',    v:'choose', m:3, dex:1, kind:'ten'},
  friend: {icon:'users',    v:'choose', m:3, dex:0, kind:'friend'},
  vfit:   {icon:'compass',  v:'choose', m:3, dex:1, kind:'vfit'},
  coin:   {icon:'star',     v:'choose', m:1, dex:1, kind:'coin'},
  enough: {icon:'check',    v:'choose', m:3, dex:1, kind:'enough'}
};
/* ---- deciding ---- */
function decV(k){ return esc((tl2 && tl2[k])||''); }
function decAB(){ return '<div class="dc-ab"><input type="text" class="tl2-in" data-dc="a" maxlength="60" placeholder="'+esc(t('dc.a'))+'" value="'+decV('a')+'">'+
  '<input type="text" class="tl2-in" data-dc="b" maxlength="60" placeholder="'+esc(t('dc.b'))+'" value="'+decV('b')+'"></div>'; }
function decName(o){ return (tl2[o]||'').trim() || t(o==='a'?'dc.a':'dc.b'); }
function decFoot(){ return '<div class="dc-foot"><input type="text" class="tl2-in" data-dc="first" maxlength="80" placeholder="'+esc(t('dc.step'))+'" value="'+decV('first')+'">'+
  '<div class="row-btns"><button class="btn btn-primary" id="dcAdd">'+ic('plus')+'<span>'+esc(t('tl2.toDay'))+'</span></button>'+
  '<button class="btn btn-ghost" id="dcDone">'+esc(t('dc.done'))+'</button></div></div>'; }
function decLean(sa,sb){ return '<p class="dc-lean">'+esc(sa===sb ? t('dc.even') : t('dc.lean',{o:decName(sa>sb?'a':'b')}))+'</p>'; }
var DEC_KINDS={
  pros:function(){
    if(!tl2.pc) tl2.pc={a:[],b:[]};
    var sc=function(o){ return tl2.pc[o].reduce(function(n,x){ return n+(x.pro?x.w:-x.w); },0); };
    return decAB()+['a','b'].map(function(o){
      return '<div class="dc-opt"><b><span data-dcname="'+o+'">'+esc(decName(o))+'</span> <span class="dc-sc numf">'+(sc(o)>0?'+':'')+sc(o)+'</span></b>'+
        tl2.pc[o].map(function(x,i){ return '<div class="dc-it'+(x.pro?' pro':' con')+'"><span>'+(x.pro?'＋ ':'－ ')+esc(x.t)+'</span>'+
          '<button type="button" class="dc-w" data-dcw="'+o+i+'">×'+x.w+'</button><button type="button" class="t3act" data-dcdel="'+o+i+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></div>'; }).join('')+
        '<div class="dc-add"><input type="text" data-dcpro="'+o+'" maxlength="60" placeholder="'+esc(t('tl2.pros.pro'))+'"><input type="text" data-dccon="'+o+'" maxlength="60" placeholder="'+esc(t('tl2.pros.con'))+'"></div></div>'; }).join('')+
      ((tl2.pc.a.length||tl2.pc.b.length) ? decLean(sc('a'),sc('b')) : '')+decFoot();
  },
  ten:function(){ return '<input type="text" class="tl2-in" data-dc="what" maxlength="80" placeholder="'+esc(t('dc.what'))+'" value="'+decV('what')+'">'+
    '<input type="text" class="tl2-in" data-dc="lean" maxlength="80" placeholder="'+esc(t('tl2.ten.lean'))+'" value="'+decV('lean')+'">'+
    [['m','tl2.ten.m'],['mo','tl2.ten.mo'],['y','tl2.ten.y']].map(function(x){ return '<label class="dc-lab">'+esc(t(x[1]))+'</label><input type="text" class="tl2-in" data-dc="'+x[0]+'" maxlength="100" value="'+decV(x[0])+'">'; }).join('')+decFoot(); },
  friend:function(){ return '<textarea class="tl2-in" data-dc="sit" rows="3" maxlength="300" placeholder="'+esc(t('tl2.friend.sit'))+'">'+decV('sit')+'</textarea>'+
    '<textarea class="tl2-in" data-dc="say" rows="3" maxlength="300" placeholder="'+esc(t('tl2.friend.say'))+'">'+decV('say')+'</textarea>'+decFoot(); },
  vfit:function(){
    var vals=(S.values&&S.values.list)||[];
    if(!vals.length) return '<p class="hint">'+esc(t('tl2.vfit.none'))+'</p><button class="btn btn-primary btn-block" id="dcVals">'+esc(t('vl.t'))+'</button>';
    if(!tl2.vf) tl2.vf={};
    var na=0, nb=0; vals.forEach(function(k){ if(tl2.vf[k]==='a') na++; if(tl2.vf[k]==='b') nb++; });
    return decAB()+'<div class="dc-vals">'+vals.map(function(k){ return '<div class="dc-v"><span>'+vlEmo(k)+' '+esc(vlName(k))+'</span>'+
      ['a','b'].map(function(o){ return '<button type="button" class="t3o'+(tl2.vf[k]===o?' on':'')+'" data-dcv="'+k+'|'+o+'"><span data-dcname="'+o+'">'+esc(decName(o))+'</span></button>'; }).join('')+'</div>'; }).join('')+'</div>'+
      ((na||nb) ? decLean(na,nb) : '')+decFoot(); },
  coin:function(){
    var r=tl2.coin;
    return decAB()+'<div class="dc-coin'+(r?' on':'')+'"><span class="dc-c">🪙</span>'+(r ? '<b>'+esc(t('tl2.coin.res',{o:decName(r)}))+'</b>' : '')+'</div>'+
      '<button class="btn btn-ghost btn-block" id="dcToss">'+esc(t('tl2.coin.go'))+'</button>'+
      (r ? '<p class="tl2-q">'+esc(t('tl2.coin.feel'))+'</p><div class="row-btns tl2-fb"><button class="btn btn-ghost'+(tl2.cf==='rel'?' on':'')+'" data-dcf="rel">'+esc(t('tl2.coin.rel'))+'</button>'+
        '<button class="btn btn-ghost'+(tl2.cf==='dis'?' on':'')+'" data-dcf="dis">'+esc(t('tl2.coin.dis'))+'</button></div>'+
        (tl2.cf ? '<div class="tl2-tip">'+ic('sparkles')+'<p>'+esc(t('tl2.coin.'+tl2.cf+'.t',{o:decName(tl2.cf==='rel'?r:(r==='a'?'b':'a'))}))+'</p></div>'+decFoot() : '') : ''); },
  enough:function(){
    if(!tl2.by){ var d=new Date(); d.setDate(d.getDate()+3); tl2.by=dayKey(d); }
    return '<input type="text" class="tl2-in" data-dc="what" maxlength="80" placeholder="'+esc(t('dc.what'))+'" value="'+decV('what')+'">'+
      [1,2,3].map(function(n){ return '<input type="text" class="tl2-in" data-dc="m'+n+'" maxlength="80" placeholder="'+esc(t('tl2.enough.must',{n:n}))+'" value="'+decV('m'+n)+'">'; }).join('')+
      '<label class="dc-lab">'+esc(t('tl2.enough.by'))+' <input type="date" data-dc="by" value="'+decV('by')+'"></label>'+
      '<button class="btn btn-primary btn-block" id="dcSave">'+ic('check')+'<span>'+esc(t('c.save'))+'</span></button>'; }
};
function decBind(box,d){
  box.querySelectorAll('[data-dc]').forEach(function(inp){ inp.addEventListener('input',function(){ tl2[inp.dataset.dc]=inp.value; });
    if(inp.dataset.dc==='a'||inp.dataset.dc==='b') inp.addEventListener('input',function(){ var o=inp.dataset.dc;
      box.querySelectorAll('[data-dcname="'+o+'"]').forEach(function(el){ el.textContent=decName(o); }); }); });
  var add=box.querySelector('#dcAdd'); if(add) add.addEventListener('click',function(){
    var v=(tl2.first||'').trim(); if(!v){ box.querySelector('[data-dc="first"]').focus(); return; }
    if(addDayItem(v)){ toast(t('tl2.added')); tl2Done(t('dc.ok')); } });
  var dn=box.querySelector('#dcDone'); if(dn) dn.addEventListener('click',function(){ tl2Done(t('dc.ok')); });
  if(d.kind==='pros'){
    /* after adding, the field the person moved to keeps the focus (or the same one, after Enter) */
    var put=function(o,pro,inp,enter){ var v=inp.value.trim(); if(!v) return; inp.value=''; tl2.pc[o].push({t:v, pro:pro, w:2});
      setTimeout(function(){
        var a=document.activeElement, sel = enter ? (pro?'[data-dcpro="'+o+'"]':'[data-dccon="'+o+'"]')
          : a && a.dataset && a.dataset.dcpro ? '[data-dcpro="'+a.dataset.dcpro+'"]' : a && a.dataset && a.dataset.dccon ? '[data-dccon="'+a.dataset.dccon+'"]'
          : a && a.dataset && a.dataset.dc ? '[data-dc="'+a.dataset.dc+'"]' : null;
        tl2Render(); var n=sel && document.querySelector('#tlBody '+sel); if(n) n.focus(); },0); };
    box.querySelectorAll('[data-dcpro]').forEach(function(inp){ inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); put(inp.dataset.dcpro,true,inp,true); } });
      inp.addEventListener('change',function(){ put(inp.dataset.dcpro,true,inp); }); });
    box.querySelectorAll('[data-dccon]').forEach(function(inp){ inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); put(inp.dataset.dccon,false,inp,true); } });
      inp.addEventListener('change',function(){ put(inp.dataset.dccon,false,inp); }); });
    box.querySelectorAll('[data-dcw]').forEach(function(b){ b.addEventListener('click',function(){ var x=tl2.pc[b.dataset.dcw[0]][+b.dataset.dcw.slice(1)]; x.w=x.w%3+1; tl2Render(); }); });
    box.querySelectorAll('[data-dcdel]').forEach(function(b){ b.addEventListener('click',function(){ tl2.pc[b.dataset.dcdel[0]].splice(+b.dataset.dcdel.slice(1),1); tl2Render(); }); });
  }
  if(d.kind==='vfit'){
    var gv=box.querySelector('#dcVals'); if(gv) gv.addEventListener('click',function(){ tl2Close(); goPage('values'); });
    box.querySelectorAll('[data-dcv]').forEach(function(b){ b.addEventListener('click',function(){ var p=b.dataset.dcv.split('|'); tl2.vf[p[0]] = tl2.vf[p[0]]===p[1] ? null : p[1]; tl2Render(); }); });
  }
  if(d.kind==='coin'){
    box.querySelector('#dcToss').addEventListener('click',function(){ tl2.coin=Math.random()<.5?'a':'b'; tl2.cf=null; tl2Render(); });
    box.querySelectorAll('[data-dcf]').forEach(function(b){ b.addEventListener('click',function(){ tl2.cf=b.dataset.dcf; tl2Render(); }); });
  }
  if(d.kind==='enough') box.querySelector('#dcSave').addEventListener('click',function(){
    var w=(tl2.what||'').trim(); if(!w){ box.querySelector('[data-dc="what"]').focus(); return; }
    var musts=[1,2,3].map(function(n){ return (tl2['m'+n]||'').trim(); }).filter(Boolean);
    if(!S.notes) S.notes=[];
    S.notes.unshift({id:Date.now(), k:'todo', t:t('tl2.enough.note',{d:w, by:fmtDay(tl2.by)})+(musts.length?' · '+musts.join(', '):'')});
    save(); tl2Done(t('tl2.enough.ok')); });
}
var STUCK_TO={bore:'five', fear:'pz:day', unclear:'tiny', big:'tiny', tired:'five', perfect:'focus'};
var tl2=null, tl2Hist=false;
function tl2St(){ if(!S.tl2) S.tl2={help:{}, used:{}}; return S.tl2; }
function tl2Open(id){
  var d=TL2[id]; if(!d) return;
  tl2Stop();
  tl2={id:id, step:'intro'};
  var m=document.getElementById('toolModal');
  m.className='modal-bg v-'+d.v;
  document.getElementById('tlTitle').innerHTML=ic(d.icon)+'<span>'+esc(t('tl2.'+id+'.t'))+'</span>';
  tl2Render(); m.classList.add('on');
  try{ history.pushState({tl2:1},''); tl2Hist=true; }catch(e){}
}
function tl2Close(fromBack){
  tl2Stop(); tl2=null; document.getElementById('toolModal').classList.remove('on');
  if(tl2Hist && fromBack!==true){ tl2Hist=false; try{ history.back(); }catch(e){} } else tl2Hist=false;
  if(typeof renderDash==='function') renderDash();
}
window.addEventListener('popstate',function(){ if(document.getElementById('toolModal').classList.contains('on')){ tl2Hist=false; tl2Close(true); } });
document.getElementById('tlX').addEventListener('click',function(){ tl2Close(); });
document.getElementById('toolModal').addEventListener('click',function(e){ if(e.target.id==='toolModal') tl2Close(); });

function tl2Intro(id){
  var d=TL2[id];
  return '<p class="tl2-sub">'+esc(t('tl2.'+id+'.s'))+' · <span class="tl2-min">'+ic('clock')+esc(t('tl2.mins',{n:d.kind==='focus'&&ageK()==='k'?15:d.m}))+'</span></p>'+
    '<div class="tl2-why"><b>'+esc(t('tl2.why'))+'</b> '+esc(t('tl2.'+id+'.w'))+'</div>'+
    '<ol class="tl2-steps">'+[1,2,3].map(function(n){ return '<li>'+esc(t('tl2.'+id+'.'+n))+'</li>'; }).join('')+'</ol>'+
    (d.ex ? '<p class="tl2-ex"><b>'+esc(t('tl2.ex'))+':</b> '+esc(t('tl2.'+id+'.ex.'+ageK()))+'</p>' : '')+
    (d.dex ? '<p class="tl2-ex">'+esc(t('dc.ex.'+ageK()))+'</p>' : '');
}
/* the end of every tool: a step was taken, and did it help? */
function tl2Done(msg){
  var st=tl2St(), today=dayKey(), id=tl2.id;
  if(!st.used[today]) st.used[today]=[];
  if(st.used[today].indexOf(id)<0){ st.used[today].push(id); addPts(5); }
  markActiveToday(); save();
  tl2.step='end'; tl2.msg=msg; tl2Render();
}
function tl2EndHtml(){
  return '<div class="pz-done"><div class="pz-ok">'+ic('check')+'</div><p class="pz-felt">'+esc(tl2.msg||t('tl2.timeup'))+'</p></div>'+
    '<p class="tl2-q">'+esc(t('tl2.helped'))+'</p>'+
    '<div class="row-btns tl2-fb"><button class="btn btn-ghost" data-tlfb="1">'+esc(t('tl2.yes'))+'</button><button class="btn btn-ghost" data-tlfb="0">'+esc(t('tl2.no'))+'</button></div>'+
    '<div class="row-btns"><button class="btn btn-quiet" id="tlEnd">'+esc(t('tl2.finish'))+'</button></div>';
}

/* ---- the timer: an end time, so a pause or a locked phone keeps it right ---- */
var tlTimer=null;
function tl2Stop(){ if(tlTimer){ clearInterval(tlTimer); tlTimer=null; } }
function fmtMS(s){ s=Math.max(0,Math.round(s)); return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2); }
function tl2TimerHtml(){
  var left=tl2.run ? (tl2.end-Date.now())/1000 : tl2.left;
  return '<div class="tl2-clock'+(tl2.phase==='break'?' brk':'')+'">'+
    (tl2.id==='focus' ? '<small>'+esc(t(tl2.phase==='break'?'tl2.focus.break':'tl2.focus.work'))+'</small>' : '')+
    '<b class="numf" id="tlLeft">'+fmtMS(left)+'</b></div>'+
    '<div class="row-btns tl2-tb">'+(tl2.run ? '<button class="btn btn-ghost" id="tlPause">'+esc(t('tl2.pause'))+'</button>'
      : '<button class="btn btn-primary" id="tlGo">'+esc(t(tl2.left<tl2.total?'tl2.resume':'tl2.start'))+'</button>')+
    (tl2.left<tl2.total||tl2.run ? '<button class="btn btn-quiet" id="tlReset">'+esc(t('tl2.reset'))+'</button>' : '')+'</div>'+
    (tl2.id==='focus' ? '<p class="tl2-n">'+esc(t('tl2.focus.n',{n:((S.focus||{})[dayKey()]||0)}))+'</p>' : '');
}
function tl2SetTimer(mins,phase){ tl2.total=mins*60; tl2.left=tl2.total; tl2.run=false; tl2.phase=phase||'work'; }
function tl2Tick(){
  var left=(tl2.end-Date.now())/1000, el=document.getElementById('tlLeft');
  if(el) el.textContent=fmtMS(left);
  if(left<=0){
    tl2Stop(); tl2.run=false; tl2.left=0;
    try{ if(navigator.vibrate) navigator.vibrate([200,100,200]); }catch(e){}
    if(tl2.id==='focus'){
      if(tl2.phase==='work'){ if(!S.focus) S.focus={}; S.focus[dayKey()]=(S.focus[dayKey()]||0)+1; save(); toast(t('tl2.focus.brk')); tl2SetTimer(5,'break'); tl2Render(); return; }
      tl2Done(t('tl2.timeup')); return;
    }
    tl2Done(t('tl2.timeup'));
  }
}

function tl2Render(){
  if(!tl2) return;
  var box=document.getElementById('tlBody'), id=tl2.id, d=TL2[id];
  if(tl2.step==='end'){
    box.innerHTML=tl2EndHtml();
    box.querySelectorAll('[data-tlfb]').forEach(function(b){ b.addEventListener('click',function(){
      var st=tl2St(); if(!st.help[id]) st.help[id]=[0,0]; st.help[id][b.dataset.tlfb==='1'?0:1]++; save();
      toast(t('tl2.thanks')); tl2Close(); }); });
    box.querySelector('#tlEnd').addEventListener('click',function(){ tl2Close(); });
    if(id==='five'){ var more=document.createElement('button'); more.className='btn btn-primary'; more.textContent=t('tl2.more5');
      box.querySelector('.tl2-fb').before(more);
      more.addEventListener('click',function(){ tl2SetTimer(5); tl2.step='timer'; tl2Render(); document.getElementById('tlGo').click(); }); }
    return;
  }
  var html=tl2Intro(id), td=today3();
  if(d.kind==='timer' || d.kind==='focus'){
    if(tl2.total==null) tl2SetTimer(d.kind==='focus' ? (ageK()==='k'?15:25) : d.m);
    if(id==='five') html+='<input type="text" class="tl2-in" id="tlWhat" maxlength="80" placeholder="'+esc(t('tl2.what'))+'" value="'+esc(tl2.what||'')+'">';
    html+=tl2TimerHtml();
  }
  else if(d.kind==='tiny'){
    html+='<input type="text" class="tl2-in" id="tlBig" maxlength="80" placeholder="'+esc(t('tl2.tiny.big'))+'">'+
      '<input type="text" class="tl2-in" id="tlSmall" maxlength="80" placeholder="'+esc(t('tl2.tiny.small'))+'">'+
      '<button class="btn btn-primary btn-block" id="tlAdd">'+ic('plus')+'<span>'+esc(t('tl2.toDay'))+'</span></button>';
  }
  else if(d.kind==='ifthen'){
    html+='<div class="tl2-if"><label>'+esc(t('tl2.ifthen.if'))+' <input type="time" id="tlTime" value="17:00"></label>'+
      '<input type="text" class="tl2-in" id="tlThen" maxlength="80" placeholder="'+esc(t('tl2.ifthen.then'))+'"></div>'+
      '<button class="btn btn-primary btn-block" id="tlAdd">'+ic('plus')+'<span>'+esc(t('tl2.toDay'))+'</span></button>';
  }
  else if(d.kind==='top3'){
    var imp=td.items.filter(function(x){ return x.imp && !x.done; }).map(function(x){ return x.t; });
    html+=[0,1,2].map(function(i){ return '<input type="text" class="tl2-in" data-top="'+i+'" maxlength="80" placeholder="'+(i+1)+'." value="'+esc(imp[i]||'')+'">'; }).join('')+
      '<button class="btn btn-primary btn-block" id="tlAdd">'+ic('plus')+'<span>'+esc(t('tl2.toDay'))+'</span></button>';
  }
  else if(d.kind==='frog'){
    var open=td.items.map(function(x,i){ return {x:x,i:i}; }).filter(function(o){ return !o.x.done; });
    html+= open.length ? '<div class="tl2-pick">'+open.map(function(o){ return '<button type="button" class="tl2-opt'+(o.x.frog?' on':'')+'" data-frog="'+o.i+'">'+(o.x.frog?'🐸 ':'')+esc(o.x.t)+'</button>'; }).join('')+'</div>'
      : '<p class="hint">'+esc(t('tl2.empty'))+'</p><input type="text" class="tl2-in" id="tlFrogIn" maxlength="80"><button class="btn btn-primary btn-block" id="tlFrogAdd">'+esc(t('tl2.frog.pick'))+'</button>';
  }
  else if(d.kind==='stuck'){
    html+='<p class="tl2-q">'+esc(t('tl2.stuck.q'))+'</p><div class="mg-picks pz-chips">'+Object.keys(STUCK_TO).map(function(r){
      return '<button type="button" class="t3idea t3chip'+(tl2.r===r?' on':'')+'" data-why="'+r+'"><span>'+esc(t('tl2.r.'+r))+'</span></button>'; }).join('')+'</div>'+
      (tl2.r ? '<div class="tl2-tip">'+ic('sparkles')+'<p>'+esc(t('tl2.tip.'+tl2.r))+'</p></div>'+
        '<button class="btn btn-primary btn-block" id="tlNext">'+esc(t('tl2.go'))+': '+esc(STUCK_TO[tl2.r].indexOf('pz:')===0 ? t('pz.btn') : t('tl2.'+STUCK_TO[tl2.r]+'.t'))+'</button>' : '');
  }
  else if(d.kind==='matrix' || d.kind==='blocks'){
    if(!td.items.length) html+='<p class="hint">'+esc(t('tl2.empty'))+'</p>';
    if(d.kind==='matrix'){
      var q=function(x){ return x.imp&&x.urg ? 1 : x.imp ? 2 : x.urg ? 3 : 4; };
      html+=td.items.map(function(x,i){ return x.done ? '' : '<div class="tl2-row"><span>'+esc(x.t)+'</span>'+
        '<button type="button" class="t3o'+(x.imp?' on':'')+'" data-mimp="'+i+'">⭐ '+esc(t('tm.imp'))+'</button>'+
        '<button type="button" class="t3o'+(x.urg?' on':'')+'" data-murg="'+i+'">⏰ '+esc(t('tm.urg'))+'</button>'+
        '<small class="tl2-qn">'+esc(t('tl2.q.'+q(x)))+'</small></div>'; }).join('');
    } else {
      html+=td.items.map(function(x,i){ return x.done ? '' : '<div class="tl2-row"><span>'+esc(x.t)+'</span><input type="time" data-btime="'+i+'" value="'+esc(x.time||'')+'"></div>'; }).join('');
    }
    if(td.items.length) html+='<button class="btn btn-primary btn-block" id="tlOk">'+ic('check')+'<span>'+esc(t('c.save'))+'</span></button>';
  }
  else if(d.kind==='rocks'){
    if(!S.rocks) S.rocks={}; var r=S.rocks[weekKey()]||[];
    html+=[0,1,2].map(function(i){ return '<div class="tl2-rock"><input type="text" class="tl2-in" data-rock="'+i+'" maxlength="80" placeholder="'+esc(t('tl2.rocks.ph',{n:i+1}))+'" value="'+esc(r[i]||'')+'">'+
      (r[i] ? '<button type="button" class="btn btn-ghost btn-sm" data-rockday="'+i+'">'+esc(t('tl2.rocks.today'))+'</button>' : '')+'</div>'; }).join('')+
      '<button class="btn btn-primary btn-block" id="tlOk">'+ic('check')+'<span>'+esc(t('c.save'))+'</span></button>';
  }
  else if(d.kind==='seq'){
    var si=tl2.si||0, k=d.seq[si], last=si===d.seq.length-1;
    html+='<div class="rg-card"><span class="rg-n">'+(id==='ground' ? k : 'STOP'.charAt(si))+'</span>'+
      (id==='ground' ? '<b>'+esc(t('tl2.g.'+k))+'</b><small>'+esc(t('tl2.g.h'))+'</small>' : '<b>'+esc(t('tl2.stop.p'+k))+'</b><small>'+esc(t('tl2.stop.b'+k))+'</small>')+
      '<div class="tour-dots">'+d.seq.map(function(_,i){ return '<i'+(i===si?' class="on"':'')+'></i>'; }).join('')+'</div></div>'+
      '<button class="btn btn-primary btn-block" id="rgNext">'+esc(t(last?'dc.done':'tr.next'))+' '+(last?'':ic('arrow'))+'</button>';
  }
  else if(d.kind==='name'){
    html+='<div class="mg-picks pz-chips">'+FEELINGS.slice(7).map(function(f){ return '<button type="button" class="t3idea t3chip'+(tl2.f===f.k?' on':'')+'" data-rgf="'+f.k+'"><span>'+f.e+' '+esc(t('fe.'+f.k))+'</span></button>'; }).join('')+'</div>'+
      (tl2.f ? '<div class="tl2-tip rg-say">'+ic('sparkles')+'<p>'+esc(t('tl2.name.say',{f:t('fe.'+tl2.f).toLowerCase()}))+'</p></div><button class="btn btn-primary btn-block" id="rgDone">'+esc(t('dc.done'))+'</button>' : '');
  }
  else if(d.kind==='therm'){
    var go={2:['tool:name'],3:['pz:day'],4:['tool:stop'],5:['tool:ground','tool:calmbox']};
    html+='<div class="rg-therm">'+[5,4,3,2,1].map(function(n){ return '<button type="button" class="rg-t t'+n+(tl2.n===n?' on':'')+'" data-rgt="'+n+'"><b class="numf">'+n+'</b><span>'+esc(t('tl2.therm.l'+n))+'</span></button>'; }).join('')+'</div>'+
      (tl2.n ? '<div class="tl2-tip">'+ic('sparkles')+'<p>'+esc(t('tl2.therm.a'+tl2.n))+'</p></div>'+
        (go[tl2.n]||[]).map(function(a){ var L=pracLabel(a); return '<button class="pr-item" data-rggo="'+a+'">'+ic(L[0])+'<span><b>'+esc(L[1])+'</b></span>'+ic('chevron')+'</button>'; }).join('')+
        '<button class="btn btn-ghost btn-block" id="rgDone">'+esc(t('dc.done'))+'</button>' : '');
  }
  else if(d.kind==='calmbox'){
    if(!S.calmbox) S.calmbox=[];
    var mine=S.calmbox;
    html+='<div class="nt-sg">'+t('tl2.calmbox.sg.'+ageK()).split('|').map(function(x){ var on=mine.indexOf(x)>=0;
        return '<button type="button" class="t3idea'+(on?' on':'')+'" data-rgcb="'+esc(x)+'">'+ic(on?'check':'plus')+'<span>'+esc(x)+'</span></button>'; }).join('')+'</div>'+
      '<div class="addrow"><input type="text" id="rgCbIn" maxlength="60" placeholder="'+esc(t('tl2.calmbox.ph'))+'"><button class="btn btn-ghost" id="rgCbAdd">'+ic('plus')+'<span>'+esc(t('c.add'))+'</span></button></div>'+
      '<div class="rg-box"><b>🧰 '+esc(t('tl2.calmbox.mine'))+'</b>'+(mine.length ? '<div class="rg-items">'+mine.map(function(x,i){
        return '<span class="ns-chip">'+esc(x)+'<button type="button" class="rg-x" data-rgcbdel="'+i+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></span>'; }).join('')+'</div>'
        : '<p class="hint">'+esc(t('tl2.calmbox.empty'))+'</p>')+'</div>'+
      '<button class="btn btn-primary btn-block" id="rgDone">'+esc(t('dc.done'))+'</button>';
  }
  else if(d.kind in DEC_KINDS) html+=DEC_KINDS[d.kind]();
  box.innerHTML=html;
  tl2Bind(box,d,td);
  if(d.kind in DEC_KINDS) decBind(box,d);
  regBind(box,d);
}
function regBind(box,d){
  var nx=box.querySelector('#rgNext'); if(nx) nx.addEventListener('click',function(){
    tl2.si=(tl2.si||0)+1; if(tl2.si>=d.seq.length) tl2Done(t('tl2.well')); else tl2Render(); });
  box.querySelectorAll('[data-rgf]').forEach(function(b){ b.addEventListener('click',function(){ tl2.f=b.dataset.rgf; tl2Render(); }); });
  box.querySelectorAll('[data-rgt]').forEach(function(b){ b.addEventListener('click',function(){ tl2.n=+b.dataset.rgt; tl2Render(); }); });
  box.querySelectorAll('[data-rggo]').forEach(function(b){ b.addEventListener('click',function(){ var a=b.dataset.rggo;
    if(a.indexOf('pz:')===0){ tl2Close(); pzOpen(a.slice(3)); } else tl2Open(a.slice(5)); }); });
  box.querySelectorAll('[data-rgcb]').forEach(function(b){ b.addEventListener('click',function(){ var x=b.dataset.rgcb, i=S.calmbox.indexOf(x);
    if(i<0) S.calmbox.push(x); else S.calmbox.splice(i,1); save(); tl2Render(); }); });
  box.querySelectorAll('[data-rgcbdel]').forEach(function(b){ b.addEventListener('click',function(){ S.calmbox.splice(+b.dataset.rgcbdel,1); save(); tl2Render(); }); });
  var ca=box.querySelector('#rgCbAdd'); if(ca){ var ci=box.querySelector('#rgCbIn');
    var add=function(){ var v=ci.value.trim(); if(!v) return; if(S.calmbox.indexOf(v)<0) S.calmbox.push(v); save(); tl2Render(); var n=document.getElementById('rgCbIn'); if(n) n.focus(); };
    ca.addEventListener('click',add); ci.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); add(); } }); }
  var dn=box.querySelector('#rgDone'); if(dn) dn.addEventListener('click',function(){ tl2Done(t('tl2.well')); });
}
function tl2Bind(box,d,td){
  var $=function(s){ return box.querySelector(s); };
  if(d.kind==='timer' || d.kind==='focus'){
    var w=$('#tlWhat'); if(w) w.addEventListener('input',function(){ tl2.what=w.value; });
    var go=$('#tlGo'); if(go) go.addEventListener('click',function(){
      if(tl2.id==='five' && tl2.what && tl2.what.trim() && !tl2.added){ addDayItem(tl2.what.trim()); tl2.added=true; }
      tl2.end=Date.now()+tl2.left*1000; tl2.run=true; tl2Stop(); tlTimer=setInterval(tl2Tick,500); tl2Render(); });
    var pa=$('#tlPause'); if(pa) pa.addEventListener('click',function(){ tl2.left=Math.max(0,(tl2.end-Date.now())/1000); tl2.run=false; tl2Stop(); tl2Render(); });
    var rs=$('#tlReset'); if(rs) rs.addEventListener('click',function(){ tl2Stop(); tl2SetTimer(tl2.total/60, tl2.phase); tl2Render(); });
  }
  if(d.kind==='tiny') $('#tlAdd').addEventListener('click',function(){
    var s=$('#tlSmall').value.trim(), b=$('#tlBig').value.trim();
    if(!s){ (b ? $('#tlSmall') : $('#tlBig')).focus(); return; }
    if(b){ if(!S.notes) S.notes=[]; S.notes.unshift({id:Date.now(), k:'todo', t:b}); }
    if(addDayItem(s)){ toast(t('tl2.added')); tl2Done(t('tl2.added')); } });
  if(d.kind==='ifthen') $('#tlAdd').addEventListener('click',function(){
    var th=$('#tlThen').value.trim(), tm=$('#tlTime').value; if(!th){ $('#tlThen').focus(); return; }
    if(addDayItem(th)){ var it=today3().items.filter(function(x){ return x.t===th; })[0]; if(it && tm) it.time=tm; save(); tl2Done(t('tl2.added')); } });
  if(d.kind==='top3') $('#tlAdd').addEventListener('click',function(){
    var n=0; box.querySelectorAll('[data-top]').forEach(function(inp){ var v=inp.value.trim(); if(!v) return;
      if(addDayItem(v)){ var it=today3().items.filter(function(x){ return normLine(x.t)===normLine(v); })[0]; if(it){ it.imp=true; n++; } } });
    if(!n){ box.querySelector('[data-top]').focus(); return; } save(); tl2Done(t('tl2.added')); });
  if(d.kind==='frog'){
    box.querySelectorAll('[data-frog]').forEach(function(b){ b.addEventListener('click',function(){ tl2Frog(+b.dataset.frog); }); });
    var fa=$('#tlFrogAdd'); if(fa) fa.addEventListener('click',function(){ var v=$('#tlFrogIn').value.trim(); if(!v) return;
      if(addDayItem(v)) tl2Frog(today3().items.length-1); });
  }
  if(d.kind==='stuck'){
    box.querySelectorAll('[data-why]').forEach(function(b){ b.addEventListener('click',function(){ tl2.r=b.dataset.why; tl2Render(); }); });
    var nx=$('#tlNext'); if(nx) nx.addEventListener('click',function(){
      var to=STUCK_TO[tl2.r], st=tl2St(), today=dayKey(); if(!st.used[today]) st.used[today]=[]; if(st.used[today].indexOf('stuck')<0) st.used[today].push('stuck'); save();
      if(to.indexOf('pz:')===0){ tl2Close(); pzOpen(to.slice(3)); } else tl2Open(to); });
  }
  if(d.kind==='matrix'){
    box.querySelectorAll('[data-mimp]').forEach(function(b){ b.addEventListener('click',function(){ var x=td.items[+b.dataset.mimp]; x.imp=!x.imp; save(); tl2Render(); }); });
    box.querySelectorAll('[data-murg]').forEach(function(b){ b.addEventListener('click',function(){ var x=td.items[+b.dataset.murg]; x.urg=!x.urg; save(); tl2Render(); }); });
  }
  if(d.kind==='blocks') box.querySelectorAll('[data-btime]').forEach(function(inp){ inp.addEventListener('change',function(){ td.items[+inp.dataset.btime].time=inp.value; save(); }); });
  if(d.kind==='rocks'){
    var keep=function(){ var r=[]; box.querySelectorAll('[data-rock]').forEach(function(inp){ r.push(inp.value.trim()); }); S.rocks[weekKey()]=r; save(); };
    box.querySelectorAll('[data-rockday]').forEach(function(b){ b.addEventListener('click',function(){ keep(); var v=S.rocks[weekKey()][+b.dataset.rockday]; if(v && addDayItem(v)) toast(t('tl2.added')); }); });
    $('#tlOk').addEventListener('click',function(){ keep(); tl2Done(t('vis.saved')); });
  }
  var okb=$('#tlOk'); if(okb && (d.kind==='matrix'||d.kind==='blocks')) okb.addEventListener('click',function(){ save(); tl2Done(t('gl.saved')); });
}
function tl2Frog(i){
  var td=today3(); td.items.forEach(function(x,j){ x.frog = j===i; }); save();
  toast(t('tl2.frog.ok')); tl2Done(t('tl2.frog.ok'));
}

/* ================= what is hard for me now ================= */
var HARD={procr:['tool:five','tool:tiny','tool:stuck'], time:['tool:top3','tool:matrix','tool:blocks'], much:['page:notes','tool:top3','tool:frog'],
          energy:['tool:two','tool:five','pz:day'], stress:['tool:stop','pz:day','tool:ground'], strong:['tool:therm','tool:ground','tool:calmbox'], lost:['page:values','vision','mean'],
          decide:['tool:pros','tool:ten','tool:coin'], fear:['tool:draft','tool:tiny','pz:sc'], sad:['tool:name','pz:sc','game:kind'],
          phone:['tool:phone','tool:focus','tool:five'], forget:['page:notes','tool:ifthen','tool:blocks']};
var hardOn=null;
function pracLabel(a){
  var k=a.split(':')[0], v=a.split(':')[1];
  if(k==='tool') return [TL2[v].icon, t('tl2.'+v+'.t'), t('tl2.'+v+'.s')];
  if(k==='pz') return {day:['wind',t('pz.btn'),t('pz.d.s')], feel:['face',t('pz.ck.t'),t('pz.ck.s')], sc:['shield',t('sc.t'),'']}[v];
  if(a==='page:notes') return ['edit', t('nt.t'), t('nt.sub')];
  if(a==='page:values') return ['compass', t('vl.t'), t('more.values')];
  if(a==='vision') return ['compass', t('vis.t'), t('vis.s')];
  if(a==='mean') return ['seedling', t('mn.t'), ''];
  if(k==='game'){ var g=GAME_IDS.filter(function(x){ return x.id===v; })[0]; return [g?g.icon:'star', t('gm.'+v), t('gm.'+v+'.s')]; }
  if(a==='well:grat') return ['book', t('gr.t'), ''];
  return ['star', a, ''];
}
function renderHard(){
  var box=document.getElementById('hardBox'); if(!box) return;
  document.querySelectorAll('[data-hard]').forEach(function(b){ b.classList.toggle('on', b.dataset.hard===hardOn); });
  if(!hardOn){ box.innerHTML=''; box.hidden=true; return; }
  box.hidden=false;
  box.innerHTML=HARD[hardOn].map(function(a){ var L=pracLabel(a);
    return '<button class="pr-item" data-prac="'+a+'">'+ic(L[0])+'<span><b>'+esc(L[1])+'</b>'+(L[2]?'<small>'+esc(L[2])+'</small>':'')+'</span>'+ic('chevron')+'</button>'; }).join('');
  box.querySelectorAll('[data-prac]').forEach(pracBind);
}
document.querySelectorAll('[data-hard]').forEach(function(b){ b.addEventListener('click',function(){ hardOn = hardOn===b.dataset.hard ? null : b.dataset.hard; renderHard(); }); });

/* ================= notes =================
   To do (no day yet), don't forget (shown on Today at its time), ideas. */
var ntTab='todo', ntWhen='am';
function ntList(){ if(!S.notes) S.notes=[]; return S.notes; }
function ntDue(n,now){
  var h=now.getHours();
  if(n.w==='am') return h>=4 && h<12;
  if(n.w==='out') return h>=5 && h<11;
  if(n.w==='pm') return h>=17;
  if(n.w==='any') return true;
  if(n.w && n.w.charAt(0)==='d') return now.getDay()===Number(n.w.slice(1));
  return false;
}
function ntWhenLabel(w){
  if(w && w.charAt(0)==='d'){ var d=new Date(2026,10,1+Number(w.slice(1))); /* Nov 1 2026 is a Sunday */
    try{ return new Intl.DateTimeFormat(cur,{weekday:'long'}).format(d); }catch(e){ return w; } }
  return t('nt.w.'+(w||'any'));
}
function renderNotes(){
  var box=document.getElementById('notesBox'); if(!box) return;
  var L=ntList(), mine=L.filter(function(n){ return n.k===ntTab; });
  var tabs='<div class="nt-tabs" role="tablist">'+['todo','rem','idea'].map(function(k){ var c=L.filter(function(n){ return n.k===k; }).length;
    return '<button type="button" role="tab" class="nt-tab'+(ntTab===k?' on':'')+'" data-ntab="'+k+'">'+esc(t('nt.'+k))+(c?' <span class="numf">'+c+'</span>':'')+'</button>'; }).join('')+'</div>';
  var when = ntTab==='rem' ? '<div class="nt-when"><span>'+esc(t('nt.when'))+'</span>'+['am','out','pm','any'].map(function(w){
      return '<button type="button" class="t3o'+(ntWhen===w?' on':'')+'" data-nwhen="'+w+'">'+esc(t('nt.w.'+w))+'</button>'; }).join('')+
    '<select data-nday aria-label="'+esc(t('nt.w.day'))+'" class="t3o'+(ntWhen.charAt(0)==='d'?' on':'')+'"><option value="">'+esc(t('nt.w.day'))+'</option>'+
      [0,1,2,3,4,5,6].map(function(d){ return '<option value="d'+d+'"'+(ntWhen==='d'+d?' selected':'')+'>'+esc(ntWhenLabel('d'+d))+'</option>'; }).join('')+'</select></div>' : '';
  var sg = ntTab==='idea' ? '' : '<div class="nt-sg"><span>'+esc(t('nt.sg'))+'</span>'+t('nt.sg.'+ntTab+'.'+ageK()).split('|').map(function(x){
      return '<button type="button" class="t3idea" data-nsg="'+esc(x)+'">'+ic('plus')+'<span>'+esc(x)+'</span></button>'; }).join('')+'</div>';
  var list = mine.length ? '<div class="nt-list">'+mine.map(function(n){
      return '<div class="nt-item"><span class="nt-t">'+esc(n.t)+(n.k==='rem'?'<small>'+esc(ntWhenLabel(n.w))+'</small>':'')+'</span>'+
        (n.k==='todo' ? '<button type="button" class="btn btn-ghost btn-sm" data-nday-add="'+n.id+'">'+esc(t('nx.day.go'))+'</button>' : '')+
        (n.k==='idea' ? '<button type="button" class="btn btn-ghost btn-sm" data-ngoal="'+n.id+'">'+esc(t('nt.toGoal'))+'</button>' : '')+
        '<button type="button" class="t3act" data-ndel="'+n.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></div>'; }).join('')+'</div>'
    : '<p class="hint nt-empty">'+esc(t('nt.e.'+ntTab))+'</p>';
  box.innerHTML=tabs+'<div class="addrow nt-add"><input type="text" id="ntIn" maxlength="100" placeholder="'+esc(t('nt.ph.'+ntTab))+'">'+
    '<button class="btn btn-primary" id="ntAdd">'+ic('plus')+'<span>'+esc(t('c.add'))+'</span></button></div>'+when+sg+list;
  var inp=box.querySelector('#ntIn');
  function add(v){ v=String(v||inp.value).trim(); if(!v){ inp.focus(); return; }
    L.unshift({id:Date.now()+Math.floor(Math.random()*1000), k:ntTab, t:v, w: ntTab==='rem' ? ntWhen : null}); save(); renderNotes(); renderNoteStrip();
    var ni=document.getElementById('ntIn'); if(ni) ni.focus(); }
  box.querySelector('#ntAdd').addEventListener('click',function(){ add(); });
  inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); add(); } });
  box.querySelectorAll('[data-ntab]').forEach(function(b){ b.addEventListener('click',function(){ ntTab=b.dataset.ntab; renderNotes(); }); });
  box.querySelectorAll('[data-nwhen]').forEach(function(b){ b.addEventListener('click',function(){ ntWhen=b.dataset.nwhen; renderNotes(); }); });
  var sel=box.querySelector('[data-nday]'); if(sel) sel.addEventListener('change',function(){ if(sel.value){ ntWhen=sel.value; renderNotes(); } });
  box.querySelectorAll('[data-nsg]').forEach(function(b){ b.addEventListener('click',function(){ add(b.dataset.nsg); }); });
  var byId=function(id){ return L.filter(function(n){ return String(n.id)===String(id); })[0]; };
  var drop=function(id){ S.notes=L.filter(function(n){ return String(n.id)!==String(id); }); L=S.notes; };
  box.querySelectorAll('[data-ndel]').forEach(function(b){ b.addEventListener('click',function(){ drop(b.dataset.ndel); save(); renderNotes(); renderNoteStrip(); }); });
  box.querySelectorAll('[data-nday-add]').forEach(function(b){ b.addEventListener('click',function(){ var n=byId(b.dataset.ndayAdd);
    if(n && addDayItem(n.t)){ drop(n.id); save(); toast(t('tl2.added')); renderNotes(); } }); });
  box.querySelectorAll('[data-ngoal]').forEach(function(b){ b.addEventListener('click',function(){ var n=byId(b.dataset.ngoal); if(!n) return;
    if(typeof goalLimitReached==='function' && goalLimitReached()){ toast(t('pro.goalmax',{n:GOAL_FREE_MAX})); return; }
    S.goals.unshift(newGoal(n.t)); drop(n.id); save(); toast(t('nt.goal.ok')); renderNotes(); if(typeof renderGoals==='function') renderGoals(); }); });
}
/* on Today: what not to forget right now, ticked off for today; and the way to the notes */
function renderNoteStrip(){
  var box=document.getElementById('noteStrip'); if(!box) return;
  var L=ntList(), now=new Date(), today=dayKey(), done=(S.remDone&&S.remDone.day===today) ? S.remDone.ids : [];
  var due=L.filter(function(n){ return n.k==='rem' && ntDue(n,now); });
  var todo=L.filter(function(n){ return n.k==='todo'; }).length;
  box.innerHTML=(due.length ? '<div class="ns-rem"><b>🔔 '+esc(t('nt.strip'))+':</b>'+due.map(function(n){ var d=done.indexOf(n.id)>=0;
      return '<button type="button" class="ns-chip'+(d?' on':'')+'" data-nsdone="'+n.id+'">'+(d?ic('check'):'')+'<span>'+esc(n.t)+'</span></button>'; }).join('')+'</div>' : '')+
    '<button type="button" class="ns-open" data-prac="page:notes">'+ic('edit')+'<span>'+esc(t('nt.open'))+(todo?' · '+esc(t('nt.n',{n:todo})):'')+'</span>'+ic('chevron')+'</button>';
  box.querySelectorAll('[data-nsdone]').forEach(function(b){ b.addEventListener('click',function(){
    if(!S.remDone || S.remDone.day!==today) S.remDone={day:today, ids:[]};
    var id=Number(b.dataset.nsdone), i=S.remDone.ids.indexOf(id); if(i<0) S.remDone.ids.push(id); else S.remDone.ids.splice(i,1); save(); renderNoteStrip(); }); });
  box.querySelectorAll('[data-prac]').forEach(pracBind);
}
"""
