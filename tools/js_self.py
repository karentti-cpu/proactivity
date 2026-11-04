# -*- coding: utf-8 -*-
"""Knowing yourself: who I want to be, the circle of influence, and the
monthly nudge to back up.

P.vision is one sentence the user writes about who they want to be; Home
shows it under the greeting and My week opens with it. S.circle holds what
is on the user's mind, sorted into what is in their hands and what is not.
The last backup date is kept per device in proactive_bk, outside the
backup itself, so restoring an old file does not reset it.
"""

JS_SELF = r"""
/* ================= who I want to be ================= */
/* Suggestions: the area the check-in found weakest, two for the age band,
   then the general ones. Seven at most. */
var VISION=['vis.c1','vis.c2','vis.c3','vis.c4','vis.c5'];
function visionPicks(){
  var band=P.age ? ageBand(P.age) : 'a13', keys=[];
  if(hasProfile()) keys.push('vis.dim.'+weakDim());
  keys.push('vis.'+band+'.1','vis.'+band+'.2');
  var seen={}, out=[];
  keys.concat(VISION).forEach(function(k){ var x=t(k); if(!seen[x]){ seen[x]=1; out.push(x); } });
  return out.slice(0,7);
}
function inDays(n){ var d=new Date(); d.setDate(d.getDate()+n); return dayKey(d); }
var visEdit=false;
function renderVision(){
  var box=document.getElementById('visionBox'); if(!box) return;
  var v=(P.vision||'').trim();
  if(v && !visEdit){
    /* a week after choosing, and then once a month: is this still it? */
    if(!P.visionNext){ P.visionNext=inDays(7); save(); }
    var due=P.visionNext<=dayKey();
    box.className='vision';
    box.innerHTML='<button type="button" class="vision-line" data-vis-edit aria-label="'+esc(t('ge.btn'))+'">'+ic('compass')+
      '<span><small>'+esc(t('vis.lab'))+'</small><b>'+esc(v)+'</b></span></button>'+
      (due ? '<div class="vis-chk"><p>'+esc(t('vis.chk'))+'</p><div class="row-btns">'+
        '<button class="btn btn-ghost btn-sm" data-vis-keep>'+ic('check')+'<span>'+esc(t('vis.keep'))+'</span></button>'+
        '<button class="btn btn-quiet btn-sm" data-vis-change>'+ic('edit')+'<span>'+esc(t('vis.change'))+'</span></button></div></div>' : '');
    box.querySelector('[data-vis-edit]').addEventListener('click',function(){ visEdit=true; renderVision(); });
    var kp=box.querySelector('[data-vis-keep]');
    if(kp) kp.addEventListener('click',function(){ P.visionNext=inDays(30); save(); toast(t('vis.saved')); renderVision(); });
    var ch=box.querySelector('[data-vis-change]');
    if(ch) ch.addEventListener('click',function(){ visEdit=true; renderVision(); });
    return;
  }
  /* not written yet: asked once, and "later" puts it away for a week */
  if(!v && !visEdit && P.visionLater && P.visionLater>dayKey()){ box.className='vision'; box.innerHTML=''; return; }
  box.className='vision dash-box';
  box.innerHTML='<h2 class="boxh">'+ic('compass')+'<span>'+esc(t('vis.t'))+'</span></h2>'+
    '<p class="psub">'+esc(t('vis.s'))+'</p>'+
    '<div class="field"><label for="visIn">'+esc(t('vis.lab'))+'</label>'+
      '<input type="text" id="visIn" maxlength="120" value="'+esc(v)+'" placeholder="'+esc(t('why.ph'))+'"></div>'+
    '<div class="mg-picks">'+visionPicks().map(function(x){
      return '<button type="button" class="t3idea" data-vis="'+esc(x)+'">'+ic('plus')+'<span>'+esc(x)+'</span></button>'; }).join('')+'</div>'+
    '<div class="row-btns">'+
      '<button class="btn btn-primary btn-sm" data-vis-save>'+ic('check')+'<span>'+esc(t('c.save'))+'</span></button>'+
      '<button class="btn btn-quiet btn-sm" data-vis-later>'+esc(t(v?'c.cancel':'vis.later'))+'</button>'+
    '</div>';
  var inp=box.querySelector('#visIn');
  box.querySelectorAll('[data-vis]').forEach(function(b){
    b.addEventListener('click',function(){
      inp.value=b.dataset.vis; inp.focus();
      box.querySelectorAll('[data-vis]').forEach(function(o){ o.classList.toggle('on',o===b); });
    });
  });
  function go(){
    var val=inp.value.trim(); if(!val){ inp.focus(); return; }
    P.vision=val; P.visionNext=inDays(7); visEdit=false; save(); toast(t('vis.saved')); renderVision();
  }
  box.querySelector('[data-vis-save]').addEventListener('click',go);
  inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); go(); } });
  box.querySelector('[data-vis-later]').addEventListener('click',function(){
    if(!v){ P.visionLater=inDays(7); save(); }
    visEdit=false; renderVision();
  });
}

/* ================= the circle of influence =================
   What is on my mind, sorted: in my hands (or part of it) becomes one small
   step that can go straight into My day; not in my hands can be let go. */
function cirItems(){ if(!S.circle) S.circle=[]; return S.circle; }
function cirById(id){ return cirItems().filter(function(x){ return x.id===id; })[0]; }
function renderCircle(){
  var box=document.getElementById('cirBox'); if(!box) return;
  var all=cirItems(), today=dayKey();
  var ask=all.filter(function(x){ return !x.k; });
  var mine=all.filter(function(x){ return x.k==='in' || x.k==='part'; });
  var out=all.filter(function(x){ return x.k==='out'; });
  function askCard(x){
    return '<div class="cir-item ask"><p class="cir-t">'+esc(x.t)+'</p>'+
      '<div class="mg-lab">'+esc(t('cir.ask'))+'</div>'+
      '<div class="cir-opts">'+
        '<button type="button" class="opt" data-cir-k="in" data-id="'+x.id+'">'+ic('check')+'<span>'+esc(t('cir.in'))+'</span></button>'+
        '<button type="button" class="opt" data-cir-k="part" data-id="'+x.id+'">'+ic('compass')+'<span>'+esc(t('cir.part'))+'</span></button>'+
        '<button type="button" class="opt" data-cir-k="out" data-id="'+x.id+'">'+ic('seedling')+'<span>'+esc(t('cir.out'))+'</span></button>'+
      '</div></div>';
  }
  function mineCard(x){
    var body = x.step
      ? '<p class="cir-step">'+ic('arrow')+'<span>'+esc(x.step)+'</span></p>'+
        (x.day===today
          ? '<span class="cir-in-day">'+ic('check')+esc(t('cir.added'))+'</span>'
          : '<button class="btn btn-ghost btn-sm" data-cir-day="'+x.id+'">'+ic('sun')+'<span>'+esc(t('cir.toDay'))+'</span></button>')
      : '<div class="field"><label for="cirStep'+x.id+'">'+esc(t(x.k==='part'?'cir.step.p':'cir.step'))+'</label>'+
          '<div class="addrow"><input type="text" id="cirStep'+x.id+'" data-cir-step-in="'+x.id+'" maxlength="80">'+
          '<button class="btn btn-primary" data-cir-step="'+x.id+'">'+esc(t('c.save'))+'</button></div></div>';
    return '<div class="cir-item in"><div class="cir-top"><p class="cir-t">'+esc(x.t)+'</p>'+
      '<button class="icon-btn" data-cir-del="'+x.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></div>'+body+'</div>';
  }
  function outCard(x){
    return '<div class="cir-item out"><div class="cir-top"><p class="cir-t">'+esc(x.t)+'</p></div>'+
      '<p class="cir-note">'+esc(t('cir.out.n'))+'</p>'+
      '<div class="row-btns"><button class="btn btn-ghost btn-sm" data-cir-let="'+x.id+'">'+ic('seedling')+'<span>'+esc(t('cir.let'))+'</span></button>'+
      '<button class="btn btn-quiet btn-sm" data-cir-k="in" data-id="'+x.id+'">'+esc(t('cir.backin'))+'</button></div></div>';
  }
  /* things that often weigh on someone of this age, minus what is already here */
  var band=P.age ? ageBand(P.age) : 'a13', have={};
  all.forEach(function(x){ have[normLine(x.t)]=1; });
  var sug=[1,2,3,4,5].map(function(n){ return t('cirw.'+band+'.'+n); }).filter(function(x){ return !have[normLine(x)]; });
  box.innerHTML=
    '<div class="field"><label for="cirIn">'+esc(t('cir.q'))+'</label>'+
      '<div class="addrow"><input type="text" id="cirIn" maxlength="100" placeholder="'+esc(t('cir.ph'))+'">'+
      '<button class="btn btn-primary" id="cirAdd" aria-label="'+esc(t('c.add'))+'">'+ic('plus')+'</button></div>'+
      (sug.length ? '<div class="mg-lab cir-sug">'+esc(t('cir.sug'))+'</div><div class="mg-picks">'+sug.map(function(x){
        return '<button type="button" class="t3idea" data-cirw="'+esc(x)+'">'+ic('plus')+'<span>'+esc(x)+'</span></button>'; }).join('')+'</div>' : '')+
    '</div>'+
    ask.map(askCard).join('')+
    (mine.length ? '<div class="cir-ring in"><h3>'+ic('target')+'<span>'+esc(t('cir.h.in'))+'</span></h3>'+mine.map(mineCard).join('')+'</div>' : '')+
    (out.length ? '<div class="cir-ring out"><h3>'+ic('seedling')+'<span>'+esc(t('cir.h.out'))+'</span></h3>'+out.map(outCard).join('')+'</div>' : '')+
    (all.length ? '' : '<p class="hint">'+ic('compass')+'<span>'+esc(t('cir.empty'))+'</span></p>');
  var inp=box.querySelector('#cirIn');
  function add(){
    var v=inp.value.trim(); if(!v){ inp.focus(); return; }
    cirItems().unshift({id:uid++, t:v, k:null, step:'', day:null});
    save(); renderCircle();
  }
  box.querySelector('#cirAdd').addEventListener('click',add);
  box.querySelectorAll('[data-cirw]').forEach(function(b){
    b.addEventListener('click',function(){
      inp.value=b.dataset.cirw; inp.focus();
      box.querySelectorAll('[data-cirw]').forEach(function(o){ o.classList.toggle('on',o===b); });
    });
  });
  inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); add(); } });
  box.querySelectorAll('[data-cir-k]').forEach(function(b){
    b.addEventListener('click',function(){
      var x=cirById(Number(b.dataset.id)); x.k=b.dataset.cirK; save(); renderCircle();
      var s=box.querySelector('[data-cir-step-in="'+x.id+'"]'); if(s) s.focus();
    });
  });
  box.querySelectorAll('[data-cir-step]').forEach(function(b){
    var x=cirById(Number(b.dataset.cirStep)), s=box.querySelector('[data-cir-step-in="'+x.id+'"]');
    function go(){ if(!s.value.trim()){ s.focus(); return; } x.step=s.value.trim(); markActiveToday(); save(); renderCircle(); }
    b.addEventListener('click',go);
    s.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); go(); } });
  });
  box.querySelectorAll('[data-cir-day]').forEach(function(b){
    b.addEventListener('click',function(){
      var x=cirById(Number(b.dataset.cirDay));
      if(!addDayItem(x.step)) return;
      x.day=dayKey(); save(); toast(t('cir.added')); renderCircle();
    });
  });
  box.querySelectorAll('[data-cir-del]').forEach(function(b){
    b.addEventListener('click',function(){
      S.circle=cirItems().filter(function(x){ return x.id!==Number(b.dataset.cirDel); }); save(); renderCircle();
    });
  });
  box.querySelectorAll('[data-cir-let]').forEach(function(b){
    b.addEventListener('click',function(){
      S.circle=cirItems().filter(function(x){ return x.id!==Number(b.dataset.cirLet); });
      markActiveToday(); save(); toast(t('cir.letgo')); renderCircle();
    });
  });
}

/* ================= the monthly nudge to back up =================
   Shown on Home once there are a few days worth keeping and the last backup
   is a month old (or there never was one). "Next week" puts it away for
   seven days. */
function bkState(){ try{ return JSON.parse(localStorage.getItem('proactive_bk')||'{}')||{}; }catch(e){ return {}; } }
function bkSet(o){ try{ localStorage.setItem('proactive_bk', JSON.stringify(o)); }catch(e){} }
function markBackedUp(){ var b=bkState(); b.last=dayKey(); b.later=null; bkSet(b); renderBackupAsk(); renderBackupLast(); }
function renderBackupLast(){
  var el=document.getElementById('bkLast'); if(!el) return;
  var b=bkState();
  el.textContent = b.last ? t('bk.last',{d:fmtDay(b.last)}) : t('bk.never');
}
function renderBackupAsk(){
  var box=document.getElementById('bkAsk'); if(!box) return;
  var b=bkState(), today=dayKey(), days=Object.keys(S.log||{}).length;
  var due = days>=5 && (!b.last || daysBetween(b.last,today)>=30) && !(b.later && b.later>today);
  box.hidden=!due; if(!due) return;
  box.innerHTML='<h2 class="boxh">'+ic('shield')+'<span>'+esc(t('bk.ask.t'))+'</span></h2>'+
    '<p class="psub">'+esc(t('bk.ask.s'))+'</p>'+
    '<div class="row-btns"><button class="btn btn-primary btn-sm" data-bk-go>'+ic('arrow')+'<span>'+esc(t('bk.ask.go'))+'</span></button>'+
    '<button class="btn btn-quiet btn-sm" data-bk-later>'+esc(t('bk.ask.later'))+'</button></div>';
  box.querySelector('[data-bk-go]').addEventListener('click',doExport);
  box.querySelector('[data-bk-later]').addEventListener('click',function(){
    var d=new Date(); d.setDate(d.getDate()+7); var s=bkState(); s.later=dayKey(d); bkSet(s); box.hidden=true;
  });
}

/* ================= finding materials on the internet =================
   From any row in My day, or a goal's materials: one query, editable, and
   four ways to look - videos, guides and articles, podcasts, or the whole
   web. A link found there can be pasted back: into the goal's materials,
   or kept beside a one-off thing. The app itself never fetches anything;
   the search opens in the browser. */
var srchFor=null;   // {gid} or {item: index in today's things}
function srchOpen(target){
  srchFor=target;
  var g=target.gid ? goalById(target.gid) : null;
  var it=(target.item!==undefined) ? today3().items[target.item] : null;
  var base=g ? g.title : (it ? it.t : '');
  var extra=g && g.area ? t('yt.q.'+g.area) : '';
  if(extra.indexOf('yt.q.')===0) extra='';
  var ways=[['vid','play',extra],['guide','book',t('srch.guide.q')],['pod','activity',t('srch.pod.q')],['web','globe','']];
  document.getElementById('srchBody').innerHTML=
    '<p class="psub">'+esc(t('srch.s'))+'</p>'+
    '<input type="text" id="srchQ" maxlength="100" value="'+esc(base)+'" aria-label="'+esc(t('srch.s'))+'">'+
    '<div class="srch-ways">'+ways.map(function(w){
      return '<button type="button" class="srch-way" data-srch="'+w[0]+'" data-extra="'+esc(w[2])+'">'+ic(w[1])+'<span>'+esc(t('srch.'+w[0]))+'</span></button>'; }).join('')+'</div>'+
    '<div class="field srch-save"><label for="srchUrl">'+esc(t('srch.save'))+'</label>'+
      '<div class="addrow"><input type="url" inputmode="url" id="srchUrl" placeholder="'+esc(t('res.url.ph'))+'">'+
      '<button class="btn btn-ghost" id="srchKeep">'+esc(t('c.save'))+'</button></div></div>'+
    (it && it.url ? '<p class="hint">'+ic('link')+'<span>'+esc(it.url)+'</span></p>' : '');
  var m=document.getElementById('srchModal'); m.classList.add('on');
  m.querySelectorAll('[data-srch]').forEach(function(b){
    b.addEventListener('click',function(){
      var q=document.getElementById('srchQ').value.trim(); if(!q) return;
      var full=(q+' '+(b.dataset.extra||'')).trim(), url;
      if(b.dataset.srch==='vid') url='https://www.youtube.com/results?search_query='+encodeURIComponent(full);
      else url='https://www.google.com/search?hl='+encodeURIComponent(cur||'he')+'&q='+encodeURIComponent(full);
      if(g) prefLearn(goalCat(g),0.5);
      window.open(url,'_blank','noopener');
    });
  });
  document.getElementById('srchKeep').addEventListener('click',srchKeep);
}
function srchKeep(){
  var inp=document.getElementById('srchUrl'), url=inp.value.trim();
  if(url && !/^https?:\/\//i.test(url) && /^[\w-]+(\.[\w-]+)+/.test(url)) url='https://'+url;
  if(!/^https?:\/\/\S+\.\S+/i.test(url)){ toast(t('res.bad')); inp.focus(); return; }
  var yt=ytId(url), name;
  try{ name = yt ? t('res.ytname') : new URL(url).hostname.replace(/^www\./,''); }catch(e){ name=url; }
  if(srchFor && srchFor.gid){
    var g=goalById(srchFor.gid); if(!g) return;
    if(!g.res) g.res=[];
    g.res.push({id:uid++, url:url, title:name, yt:yt});
    toast(t('srch.saved'));
  } else if(srchFor && srchFor.item!==undefined){
    var it=today3().items[srchFor.item]; if(!it) return;
    it.url=url; toast(t('srch.saved.i'));
  }
  save(); srchClose(); renderToday3(); if(typeof renderGoals==='function') renderGoals();
}
function srchClose(){ document.getElementById('srchModal').classList.remove('on'); srchFor=null; }
document.getElementById('srchClose').addEventListener('click',srchClose);
document.getElementById('srchModal').addEventListener('click',function(e){ if(e.target.id==='srchModal') srchClose(); });

/* ================= a link shared from another app =================
   With the app installed on Android it sits in the phone's Share menu.
   A video or page shared to it opens the app with the link in the address;
   the app asks which goal to keep it in (or today's list), saves it, and
   clears the address so a reload does not ask again. */
var shareSeen=false;
function sharedLink(){
  var q; try{ q=new URLSearchParams(location.search); }catch(e){ return null; }
  var raw=[q.get('url'),q.get('text'),q.get('title')].filter(Boolean).join(' ');
  var m=raw.match(/https?:\/\/[^\s"'<>]+/i); if(!m) return null;
  var url=m[0].replace(/[).,!?]+$/,''), title=(q.get('title')||'').trim();
  /* YouTube shares "title + link" as the text; what is left after the link is the name */
  if(!title){ var rest=(q.get('text')||'').replace(m[0],'').trim(); if(rest && rest.length<=80) title=rest; }
  return {url:url, title:title};
}
function sharedName(s){
  if(s.title) return s.title;
  if(ytId(s.url)) return t('res.ytname');
  try{ return new URL(s.url).hostname.replace(/^www\./,''); }catch(e){ return s.url; }
}
function handleShare(){
  if(shareSeen) return; shareSeen=true;
  var s=sharedLink(); if(!s) return;
  try{ history.replaceState(null,'',location.pathname); }catch(e){}
  splashDone=true;            /* straight to the question, no opening screen */
  openShare(s);
}
function openShare(s){
  var yt=ytId(s.url), name=sharedName(s), goals=liveGoals();
  function row(attr, icon, text){
    return '<button type="button" class="t3opt goal" '+attr+'><span class="t3opt-i">'+ic(icon)+'</span>'+
      '<span class="t3opt-t">'+esc(text)+'</span><span class="t3opt-a">'+ic('plus')+'</span></button>';
  }
  document.getElementById('shareBody').innerHTML=
    '<div class="share-prev">'+(yt ? '<img src="https://i.ytimg.com/vi/'+yt+'/mqdefault.jpg" alt="">' : ic('link'))+
      '<span>'+esc(name)+'</span></div>'+
    (goals.length ? '<div class="mg-lab">'+esc(t('t3.pick.goals'))+'</div><div class="t3list">'+
        goals.map(function(g){ return row('data-share-g="'+g.id+'"','target',g.title); }).join('')+'</div>'
      : '<p class="hint">'+esc(t('share.nogoal'))+'</p>')+
    '<div class="t3list share-today">'+row('data-share-day','sun',t('share.today'))+'</div>';
  var m=document.getElementById('shareModal'); m.classList.add('on');
  m.querySelectorAll('[data-share-g]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.shareG)); if(!g) return;
      if(!g.res) g.res=[];
      if(!g.res.some(function(r){ return r.url===s.url; })) g.res.push({id:uid++, url:s.url, title:name, yt:yt});
      prefLearn(goalCat(g),1); markActiveToday(); save();
      shareClose(); toast(t('share.saved',{g:g.title}));
      if(typeof renderGoals==='function') renderGoals();
      renderToday3();
    });
  });
  var d=m.querySelector('[data-share-day]');
  if(d) d.addEventListener('click',function(){
    if(addDayItem(name)){ var td=today3(); td.items[td.items.length-1].url=s.url; logDay(); save(); toast(t('cir.added')); }
    shareClose(); renderToday3();
  });
}
function shareClose(){ document.getElementById('shareModal').classList.remove('on'); }
document.getElementById('shareClose').addEventListener('click',shareClose);
document.getElementById('shareModal').addEventListener('click',function(e){ if(e.target.id==='shareModal') shareClose(); });

/* ================= the weekly sheet, on paper =================
   Days across the top, the week's goals down the side, a box for every
   day: printed and ticked by hand on the fridge. Photographed back in, the
   ticks are marked on the same grid on screen; every one is a step the
   avatar grows from (XP), a goal's ticks join My week, and the photo stays
   on the phone as the week's proof. Encouragement is guaranteed - even a
   sheet with no ticks is a start. */
var PS_MAX=8;
function psCfg(){
  if(!S.sheetCfg) S.sheetCfg={rows:[], next:false};
  if(!S.sheetCfg.rows.length){
    S.sheetCfg.rows=liveGoals().slice(0,PS_MAX).map(function(g){ return {t:g.title, gid:g.id}; });
  }
  return S.sheetCfg;
}
function psWeekStart(next){ var d=new Date(weekKey()+'T00:00:00'); if(next) d.setDate(d.getDate()+7); return d; }
function psDays(start){
  var out=[]; for(var i=0;i<7;i++){ var x=new Date(start); x.setDate(start.getDate()+i); out.push(x); } return out;
}
function psDayLabel(d){
  try{ return d.toLocaleDateString(cur,{weekday:'short'}); }catch(e){ return ''; }
}
function psRange(days){
  try{ return days[0].toLocaleDateString(cur,{day:'numeric',month:'short'})+' – '+days[6].toLocaleDateString(cur,{day:'numeric',month:'short'}); }catch(e){ return ''; }
}
function psSheetHtml(cfg){
  var days=psDays(psWeekStart(cfg.next)), vis=(P.vision||'').trim();
  var rows=cfg.rows.length ? cfg.rows : [{t:''},{t:''},{t:''}];
  while(rows.length<4) rows=rows.concat([{t:''}]);
  /* fewer goals, bigger boxes: the rows share the page's height */
  var rowH=Math.max(46, Math.min(84, Math.floor(400/rows.length)));
  return '<div class="sheet" id="sheetPrint">'+
    '<div class="sheet-top"><div><h3>'+esc(t('ps.sheet.t'))+'</h3><p>'+esc(psRange(days))+(P.name?' · '+esc(P.name):'')+'</p></div>'+
      '<div class="sheet-brand">Proacty</div></div>'+
    (vis ? '<p class="sheet-vis">'+esc(t('vis.lab'))+': <b>'+esc(vis)+'</b></p>' : '')+
    '<table class="sheet-grid"><thead><tr><th class="sg-goal">'+esc(t('ps.col.goal'))+'</th>'+
      days.map(function(d){ return '<th><span>'+esc(psDayLabel(d))+'</span><b>'+d.getDate()+'</b></th>'; }).join('')+
      '<th class="sg-sum">'+esc(t('ps.col.sum'))+'</th></tr></thead><tbody>'+
      rows.map(function(r){ return '<tr style="height:'+rowH+'px"><td class="sg-goal">'+esc(r.t)+'</td>'+days.map(function(){ return '<td class="sg-box"></td>'; }).join('')+'<td class="sg-sum"></td></tr>'; }).join('')+
    '</tbody></table>'+
    '<div class="sheet-lines"><p>'+esc(t('wr.q1'))+'</p><p>'+esc(t('wr.q2'))+'</p></div>'+
    '<div class="sheet-foot">'+esc(t('sp.line'))+'</div>'+
  '</div>';
}
function renderSheetPage(){
  var cfg=psCfg(), b=document.getElementById('psBuild'); if(!b) return;
  var have={}; cfg.rows.forEach(function(r){ have[normLine(r.t)]=1; });
  var cands=liveGoals().map(function(g){ return {t:g.title, gid:g.id}; })
    .concat((S.missions||[]).map(function(m){ return {t:label(m)}; }))
    .filter(function(c,i,a){ return !have[normLine(c.t)] && a.findIndex(function(x){ return normLine(x.t)===normLine(c.t); })===i; });
  b.innerHTML='<h3 class="boxh">'+ic('calendar')+'<span>'+esc(t('ps.build'))+'</span></h3>'+
    '<div class="t3seg ps-week">'+
      '<button type="button" data-psweek="0" class="'+(cfg.next?'':'on')+'">'+esc(t('wk.this'))+'</button>'+
      '<button type="button" data-psweek="1" class="'+(cfg.next?'on':'')+'">'+esc(t('wk.next'))+'</button></div>'+
    '<div class="mg-lab">'+esc(t('ps.rows'))+' <span class="numf">'+cfg.rows.length+'/'+PS_MAX+'</span></div>'+
    '<div class="ps-rows">'+cfg.rows.map(function(r,i){
      return '<div class="ps-row"><span class="numf">'+(i+1)+'</span><span class="ps-row-t">'+esc(r.t)+'</span>'+
        '<button class="icon-btn" data-psdel="'+i+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></div>'; }).join('')+'</div>'+
    (cfg.rows.length<PS_MAX ?
      (cands.length ? '<div class="mg-picks">'+cands.slice(0,8).map(function(c){
          return '<button type="button" class="t3idea" data-psadd="'+esc(c.t)+'"'+(c.gid?' data-gid="'+c.gid+'"':'')+'>'+ic('plus')+'<span>'+esc(c.t)+'</span></button>'; }).join('')+'</div>' : '')+
      '<div class="addrow"><input type="text" id="psOwn" maxlength="40" placeholder="'+esc(t('ps.own'))+'">'+
        '<button class="btn btn-ghost" id="psOwnAdd" aria-label="'+esc(t('c.add'))+'">'+ic('plus')+'</button></div>' : '')+
    '<div class="mg-lab ps-prevlab">'+esc(t('ps.preview'))+'</div>'+
    '<div class="sheet-wrap">'+psSheetHtml(cfg)+'</div>'+
    '<button class="btn btn-primary btn-block" id="psPrint">'+ic('share')+'<span>'+esc(t('ps.print'))+'</span></button>'+
    '<p class="hint">'+ic('sparkles')+'<span>'+esc(t('ps.print.h'))+'</span></p>';
  b.querySelectorAll('[data-psweek]').forEach(function(x){ x.addEventListener('click',function(){ cfg.next=x.dataset.psweek==='1'; save(); renderSheetPage(); }); });
  b.querySelectorAll('[data-psdel]').forEach(function(x){ x.addEventListener('click',function(){ cfg.rows.splice(Number(x.dataset.psdel),1); save(); renderSheetPage(); }); });
  b.querySelectorAll('[data-psadd]').forEach(function(x){ x.addEventListener('click',function(){
    cfg.rows.push({t:x.dataset.psadd, gid:x.dataset.gid?Number(x.dataset.gid):null}); save(); renderSheetPage(); }); });
  var own=b.querySelector('#psOwn');
  if(own){ var add=function(){ var v=own.value.trim(); if(!v){ own.focus(); return; } cfg.rows.push({t:v}); save(); renderSheetPage(); };
    b.querySelector('#psOwnAdd').addEventListener('click',add);
    own.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); add(); } }); }
  b.querySelector('#psPrint').addEventListener('click',function(){
    if(!cfg.rows.length){ toast(t('ps.need')); return; }
    /* the sheet is printed from its own copy at the top of the page, with
       everything else taken out of the layout, so it is one clean page */
    var root=document.getElementById('printRoot');
    if(!root){ root=document.createElement('div'); root.id='printRoot'; document.body.appendChild(root); }
    root.innerHTML=psSheetHtml(cfg).replace('id="sheetPrint"','');
    document.body.classList.add('printing-sheet'); markActiveToday();
    setTimeout(function(){ window.print(); },50);
  });
  renderSheetUpload();
}
window.addEventListener('afterprint',function(){
  document.body.classList.remove('printing-sheet');
  var root=document.getElementById('printRoot'); if(root) root.innerHTML='';
});

/* ---- the ticked sheet comes back ---- */
var psDraft=null;   // {week, rows, ticks, photo}
function psShrink(file, done){
  var fr=new FileReader();
  fr.onload=function(){
    var img=new Image();
    img.onload=function(){
      var w=img.width, h=img.height, k=Math.min(1, 900/Math.max(w,h));
      var c=document.createElement('canvas'); c.width=Math.round(w*k); c.height=Math.round(h*k);
      c.getContext('2d').drawImage(img,0,0,c.width,c.height);
      try{ done(c.toDataURL('image/jpeg',0.6)); }catch(e){ done(null); }
    };
    img.onerror=function(){ done(null); };
    img.src=fr.result;
  };
  fr.readAsDataURL(file);
}
function renderSheetUpload(){
  var u=document.getElementById('psUpload'); if(!u) return;
  var cfg=psCfg(), sheets=S.sheets||[];
  var head='<h3 class="boxh">'+ic('camera')+'<span>'+esc(t('ps.up.t'))+'</span></h3><p class="psub">'+esc(t('ps.up.s'))+'</p>';
  if(!psDraft){
    u.innerHTML=head+
      '<label class="btn btn-primary btn-block ps-cam">'+ic('camera')+'<span>'+esc(t('ps.up.btn'))+'</span>'+
        '<input type="file" accept="image/*" capture="environment" id="psFile" class="hidden-file"></label>'+
      (sheets.length ? '<div class="mg-lab">'+esc(t('ps.past'))+'</div><div class="ps-past">'+sheets.slice().reverse().slice(0,6).map(function(s){
          var n=0; s.ticks.forEach(function(r){ r.forEach(function(x){ if(x) n++; }); });
          return '<div class="ps-pastc">'+(s.photo?'<img src="'+s.photo+'" alt="">':ic('calendar'))+
            '<span>'+esc(fmtDay(s.week))+'</span><b class="numf">✓ '+n+'</b></div>'; }).join('')+'</div>' : '');
    u.querySelector('#psFile').addEventListener('change',function(e){
      var f=e.target.files&&e.target.files[0]; if(!f) return;
      psShrink(f,function(photo){
        var wk=dayKey(psWeekStart(cfg.next));
        var old=(S.sheets||[]).filter(function(s){ return s.week===wk; })[0];
        var rows=cfg.rows.length ? cfg.rows.slice() : [];
        psDraft={week:wk, rows:rows, photo:photo,
          ticks: old && old.rows.length===rows.length ? old.ticks.map(function(r){ return r.slice(); }) : rows.map(function(){ return [false,false,false,false,false,false,false]; })};
        renderSheetUpload();
      });
    });
    return;
  }
  var days=psDays(new Date(psDraft.week+'T00:00:00')), today=dayKey();
  u.innerHTML=head+
    (psDraft.photo ? '<img class="ps-photo" src="'+psDraft.photo+'" alt="">' : '')+
    '<div class="mg-lab">'+esc(t('ps.mark'))+'</div>'+
    '<div class="scroller"><table class="grid ps-mark"><thead><tr><th class="mcol">'+esc(t('ps.col.goal'))+'</th>'+
      days.map(function(d){ return '<th>'+esc(psDayLabel(d))+'</th>'; }).join('')+'</tr></thead><tbody>'+
      psDraft.rows.map(function(r,ri){ return '<tr><td class="mcol">'+esc(r.t)+'</td>'+days.map(function(d,di){
          var on=psDraft.ticks[ri][di], fut=dayKey(d)>today;
          return '<td class="dcell'+(on?' on':'')+(fut?' fut':'')+'" data-psr="'+ri+'" data-psd="'+di+'"><span class="mk">'+ic('check')+'</span></td>'; }).join('')+'</tr>'; }).join('')+
    '</tbody></table></div>'+
    '<div class="row-btns"><button class="btn btn-primary" id="psSave">'+ic('check')+'<span>'+esc(t('ps.save'))+'</span></button>'+
      '<button class="btn btn-quiet" id="psCancel">'+esc(t('c.cancel'))+'</button></div>'+
    '<div id="psReward"></div>';
  u.querySelectorAll('[data-psr]').forEach(function(c){
    c.addEventListener('click',function(){
      var r=Number(c.dataset.psr), d=Number(c.dataset.psd);
      psDraft.ticks[r][d]=!psDraft.ticks[r][d]; c.classList.toggle('on',psDraft.ticks[r][d]);
    });
  });
  u.querySelector('#psCancel').addEventListener('click',function(){ psDraft=null; renderSheetUpload(); });
  u.querySelector('#psSave').addEventListener('click',psSave);
}
function psSave(){
  var dr=psDraft; if(!dr) return;
  if(!S.sheets) S.sheets=[];
  var old=S.sheets.filter(function(s){ return s.week===dr.week; })[0];
  var n=0; dr.ticks.forEach(function(r){ r.forEach(function(x){ if(x) n++; }); });
  var paid=old ? (old.paid||0) : 0;
  /* every tick is 5 XP, and a sheet brought back is 20 more - once a week;
     a sheet brought back again pays only what was added */
  var due=n*5+20, gain=Math.max(0, due-paid);
  /* ticks on a goal's row count in My week, like a step done that day */
  var days=psDays(new Date(dr.week+'T00:00:00')), today=dayKey();
  dr.rows.forEach(function(r,ri){
    if(!r.gid || !goalById(r.gid)) return;
    days.forEach(function(d,di){
      var k=dayKey(d); if(k>today || !dr.ticks[ri][di]) return;
      if(!S.log) S.log={};
      if(!S.log[k]) S.log[k]={items:[],steps:[],st:{},note:'',feel:''};
      if(S.log[k].steps.indexOf(r.gid)<0) S.log[k].steps.push(r.gid);
    });
  });
  var rec={week:dr.week, rows:dr.rows, ticks:dr.ticks, photo:dr.photo||(old&&old.photo)||null, paid:Math.max(paid,due), at:today};
  S.sheets=S.sheets.filter(function(s){ return s.week!==dr.week; }).concat([rec]).sort(function(a,b){ return a.week<b.week?-1:1; });
  /* photos are kept for the last six sheets, so the phone's storage is not filled */
  S.sheets.forEach(function(s,i){ if(i<S.sheets.length-6) s.photo=null; });
  var before=levelInfo();
  if(gain) addPts(gain);
  markActiveToday(); save();
  var after=levelInfo();
  var msg = n===0 ? t('ps.r0') : n>=dr.rows.length*5 ? t('ps.r3',{n:n}) : n>=dr.rows.length*2 ? t('ps.r2',{n:n}) : t('ps.r1',{n:n});
  psDraft=null; renderSheetUpload();
  var box=document.getElementById('psReward') || document.getElementById('psUpload');
  var rw=document.createElement('div'); rw.className='ps-reward';
  rw.innerHTML='<div class="av-big t'+after.tier+'">'+avatarSvg(after.tier, avatarLabel(after))+'</div>'+
    '<div><p class="ps-rmsg">'+esc(msg)+'</p>'+
    (gain ? '<p class="ps-rxp">'+esc(t('ps.rxp',{n:gain}))+'</p>' : '')+
    '<div class="xp big"><i style="width:'+after.pct+'%"></i></div>'+
    '<p class="ps-rlvl">'+esc(after.level>before.level ? t('av.lvlup',{n:after.level}) : t('av.next',{n:after.need, l:after.level+1}))+'</p></div>';
  document.getElementById('psUpload').prepend(rw);
  rw.scrollIntoView({block:'center',behavior:'smooth'});
  celebrate();
}
"""