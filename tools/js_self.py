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
"""