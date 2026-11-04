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

/* ================= tracking tables: on paper or in the app =================
   Four kinds: a week (days across the top, goals down the side), a month
   of habits, a 30-day challenge for one goal, and a day's page. Each is
   built from the user's goals (or own words), prints as one clean page,
   and - except the day's page - is ticked here: straight on screen, or
   after photographing the ticked paper. Every tick is a step the avatar
   grows from; a goal's ticks join My week (today's also closes its step
   in My day); a streak of 3, 7, 14, 21 or 30 days is celebrated; and a
   photo of the paper is kept on the phone as the period's proof. */
var TRK_TYPES=[{id:'week',icon:'calendar',max:8},{id:'month',icon:'star',max:6},{id:'c30',icon:'flame',max:1},{id:'day',icon:'sun',max:0}];
var trkType='week', trkPhoto=null;
/* the sheet's look: a colour (or black and white, to save ink), a style,
   and for the fun style an emoji at the start of each row */
var TRK_COLORS={green:['#3D7B5E','#9fb3a6','#f1f6f2','#c9d6cd'], blue:['#2F6FB0','#9db5d0','#eef4fb','#c8d7e8'],
  purple:['#7A4FB0','#bba7d6','#f4effa','#d9cdea'], pink:['#C2477F','#e0a9c3','#fcf0f5','#efcfde'],
  orange:['#D9792B','#e8bf98','#fdf3ea','#f1d9c2'], ink:['#222222','#888888','#f2f2f2','#bbbbbb']};
var TRK_EMO=['🌟','💪','📚','🌿','💧','🎯','🎨','😊','🏃','🧘','🍎','😴','🎵','💰','❤️','✏️'];
function trkStyle(){ var st=trkState(); if(!st.style) st.style={color:'green', look:'clean'}; return st.style; }
var TRK_CAT_EMO={body:'💪', study:'📚', people:'❤️', money:'💰', calm:'🌿', create:'🎨'};
function trkEmo(r,i){
  if(r.e) return r.e;
  var g=r.gid && goalById(r.gid), c=g && goalCat(g);
  return (c && TRK_CAT_EMO[c]) || TRK_EMO[i%TRK_EMO.length];
}
function trkState(){
  if(!S.trk) S.trk={cfg:{}, list:[]};
  return S.trk;
}
function trkCfg(type){
  var st=trkState();
  if(!st.cfg[type]){
    var gs=liveGoals().map(function(g){ return {t:g.title, gid:g.id}; });
    var max=TRK_TYPES.filter(function(x){ return x.id===type; })[0].max;
    st.cfg[type]={rows:gs.slice(0,max), next:false, start:dayKey()};
  }
  return st.cfg[type];
}
function trkStart(type, cfg){
  if(type==='week'){ var d=new Date(weekKey()+'T00:00:00'); if(cfg.next) d.setDate(d.getDate()+7); return d; }
  if(type==='month'){ var n=new Date(); return new Date(n.getFullYear(), n.getMonth()+(cfg.next?1:0), 1); }
  if(type==='c30') return new Date((cfg.start||dayKey())+'T00:00:00');
  var t0=new Date(); t0.setHours(0,0,0,0); return t0;
}
function trkDays(type, cfg){
  var s=trkStart(type,cfg), n = type==='week'?7 : type==='c30'?30 : type==='month' ? new Date(s.getFullYear(), s.getMonth()+1, 0).getDate() : 1;
  var out=[]; for(var i=0;i<n;i++){ var x=new Date(s); x.setDate(s.getDate()+i); out.push(x); } return out;
}
function trkKey(type, cfg){ return type+':'+dayKey(trkStart(type,cfg)); }
function trkRec(type, cfg, make){
  var st=trkState(), k=trkKey(type,cfg), r=st.list.filter(function(x){ return x.key===k; })[0];
  if(!r && make){ r={key:k, type:type, ticks:{}, photo:null, bonus:false}; st.list.push(r); }
  return r;
}
function trkLoc(d,o){ try{ return d.toLocaleDateString(cur,o); }catch(e){ return ''; } }
function trkRange(days){ return trkLoc(days[0],{day:'numeric',month:'short'})+(days.length>1?' – '+trkLoc(days[days.length-1],{day:'numeric',month:'short'}):''); }
function trkTitle(type, days){
  if(type==='month') return trkLoc(days[0],{month:'long',year:'numeric'});
  if(type==='day') return trkLoc(days[0],{weekday:'long',day:'numeric',month:'long'});
  return trkRange(days);
}

/* ---- the printed page ---- */
function trkSheetHtml(type, cfg){
  var days=trkDays(type,cfg), vis=(P.vision||'').trim(), sty=trkStyle(), fun=sty.look==='fun';
  var col=TRK_COLORS[sty.color]||TRK_COLORS.green;
  var title=(cfg.title||'').trim() || t('trk.sheet.'+type);
  var head='<div class="sheet-top"><div><h3>'+esc(title)+'</h3><p>'+esc(trkTitle(type,days))+(P.name?' · '+esc(P.name):'')+'</p></div>'+
      '<div class="sheet-brand">Proacty</div></div>'+
    (vis ? '<p class="sheet-vis">'+esc(t('vis.lab'))+': <b>'+esc(vis)+'</b></p>' : '');
  var foot='<div class="sheet-foot">'+esc(t('sp.line'))+'</div>';
  var body='';
  if(type==='week' || type==='month'){
    var rows=cfg.rows.length ? cfg.rows.slice() : [];
    var minRows=type==='week'?4:3;
    while(rows.length<minRows) rows.push({t:''});
    var rowH = type==='week' ? Math.max(46, Math.min(84, Math.floor(400/rows.length))) : Math.max(40, Math.min(80, Math.floor(380/rows.length)));
    body='<table class="sheet-grid '+type+'"><thead><tr><th class="sg-goal">'+esc(t('ps.col.goal'))+'</th>'+
      days.map(function(d){ return '<th><span>'+esc(type==='week'?trkLoc(d,{weekday:'short'}):trkLoc(d,{weekday:'narrow'}))+'</span><b>'+d.getDate()+'</b></th>'; }).join('')+
      '<th class="sg-sum">'+esc(t('ps.col.sum'))+'</th></tr></thead><tbody>'+
      rows.map(function(r,i){ return '<tr style="height:'+rowH+'px"><td class="sg-goal">'+(r.t && (fun||r.e) ? '<span class="sg-emo">'+trkEmo(r,i)+'</span>' : '')+esc(r.t)+'</td>'+days.map(function(){ return '<td></td>'; }).join('')+'<td class="sg-sum"></td></tr>'; }).join('')+
      '</tbody></table>'+
      '<div class="sheet-lines"><p>'+esc(t(type==='month'?'trk.q1m':'wr.q1'))+'</p><p>'+esc(t(type==='month'?'trk.q2m':'wr.q2'))+'</p></div>';
  } else if(type==='c30'){
    var g=cfg.rows[0];
    body='<p class="sheet-c30goal">'+(fun&&g ? '<span>'+trkEmo(g,0)+'</span>' : ic('flame'))+'<b>'+esc(g?g.t:'')+'</b></p>'+
      '<div class="sheet-c30">'+days.map(function(d,i){
        return '<div class="c30-box"><span class="c30-n">'+(i+1)+'</span><span class="c30-d">'+esc(trkLoc(d,{day:'numeric',month:'numeric'}))+'</span></div>'; }).join('')+'</div>'+
      '<div class="sheet-lines"><p>'+esc(t('trk.prize'))+'</p></div>';
  } else {
    var td=today3(), lines=[];
    pickedGoals().forEach(function(g){ lines.push(g.title+(dayStep(g)?' — '+dayStep(g):'')); });
    td.items.forEach(function(x){ lines.push(x.t); });
    while(lines.length<12) lines.push('');
    body='<div class="sheet-daycols"><div><h4>'+esc(t('t3.tab.today'))+'</h4><ul class="sheet-todo">'+
        lines.map(function(l){ return '<li><span class="todo-box"></span><span>'+esc(l)+'</span></li>'; }).join('')+'</ul></div>'+
      '<div><h4>'+esc(t('ev.t'))+'</h4><p class="sheet-feels">⚡ 🌿 🌟 🌙</p>'+
        '<div class="sheet-lines"><p>'+esc(t('ev.q'))+'</p><p>'+esc(t('ev.ch.q'))+'</p></div></div></div>';
  }
  return '<div class="sheet'+(type==='day'?' portrait':'')+'" data-look="'+esc(sty.look)+'" style="--sc:'+col[0]+';--sl:'+col[1]+';--sb:'+col[2]+';--sl2:'+col[3]+'">'+head+body+foot+'</div>';
}

/* ---- ticking ---- */
function trkStreak(arr, i){ var n=0; while(i>=0 && arr[i]){ n++; i--; } return n; }
function trkTick(type, cfg, row, di){
  var days=trkDays(type,cfg), d=days[di], k=dayKey(d), today=dayKey();
  if(k>today){ toast(t('trk.future')); return; }
  var rec=trkRec(type,cfg,true), key=normLine(row.t);
  if(!rec.ticks[key]) rec.ticks[key]=days.map(function(){ return false; });
  var on=!rec.ticks[key][di]; rec.ticks[key][di]=on;
  var g=row.gid ? goalById(row.gid) : null;
  if(g){
    if(!S.log) S.log={};
    if(!S.log[k]) S.log[k]={items:[],steps:[],st:{},note:'',feel:''};
    var L=S.log[k], ix=L.steps.indexOf(g.id);
    if(on && ix<0) L.steps.push(g.id);
    if(!on && ix>=0) L.steps.splice(ix,1);
    if(k===today){
      if(on){ g.doneDay=today; if(g.paidDay!==today){ g.paidDay=today; addPts(25); } }
      else if(g.doneDay===today) g.doneDay=null;
    } else addPts(on?5:-5);
    prefLearn(goalCat(g), on?1:0);
  } else addPts(on?5:-5);
  if(on){
    markActiveToday();
    var s=trkStreak(rec.ticks[key], di);
    if([3,7,14,21,30].indexOf(s)>=0){ toast(t('trk.streak',{n:s, g:row.t})); celebrate(); }
    else toast(praise());
  }
  save(); renderTrackers();
}

/* ---- the page ---- */
var trkDesignOpen=false;
function renderTrackers(){
  var box=document.getElementById('trkBox'); if(!box) return;
  var type=trkType, cfg=trkCfg(type), tdef=TRK_TYPES.filter(function(x){ return x.id===type; })[0];
  var days=trkDays(type,cfg), rec=trkRec(type,cfg,false), today=dayKey();
  var tabs='<div class="trk-types">'+TRK_TYPES.map(function(x){
    return '<button type="button" class="trk-type'+(x.id===type?' on':'')+'" data-trk="'+x.id+'">'+ic(x.icon)+'<b>'+esc(t('trk.'+x.id))+'</b><small>'+esc(t('trk.'+x.id+'.s'))+'</small></button>'; }).join('')+'</div>';
  /* what goes in it */
  var build='';
  if(tdef.max){
    var have={}; cfg.rows.forEach(function(r){ have[normLine(r.t)]=1; });
    var cands=liveGoals().map(function(g){ return {t:g.title, gid:g.id}; })
      .concat((S.missions||[]).map(function(m){ return {t:label(m)}; }))
      .filter(function(c,i,a){ return !have[normLine(c.t)] && a.findIndex(function(x){ return normLine(x.t)===normLine(c.t); })===i; });
    var period = type==='c30'
      ? '<div class="trk-period">'+esc(t('trk.c30.from',{d:fmtDay(cfg.start)}))+' <button class="btn btn-quiet btn-sm" data-trk-restart>'+ic('refresh')+'<span>'+esc(t('trk.c30.new'))+'</span></button></div>'
      : '<div class="t3seg ps-week"><button type="button" data-trk-next="0" class="'+(cfg.next?'':'on')+'">'+esc(t(type==='week'?'wk.this':'trk.thism'))+'</button>'+
          '<button type="button" data-trk-next="1" class="'+(cfg.next?'on':'')+'">'+esc(t(type==='week'?'wk.next':'trk.nextm'))+'</button></div>';
    build='<div class="mg-lab">'+esc(t(type==='c30'?'trk.c30.goal':type==='month'?'trk.rows.m':'ps.rows'))+(tdef.max>1?' <span class="numf">'+cfg.rows.length+'/'+tdef.max+'</span>':'')+'</div>'+
      '<div class="ps-rows">'+cfg.rows.map(function(r,i){
        return '<div class="ps-row"><button type="button" class="trk-emo" data-trk-emo="'+i+'" aria-label="'+esc(t('trk.emo'))+'" title="'+esc(t('trk.emo'))+'">'+trkEmo(r,i)+'</button><span class="ps-row-t">'+esc(r.t)+'</span>'+
          '<button class="icon-btn" data-trk-del="'+i+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></div>'; }).join('')+'</div>'+
      (cfg.rows.length<tdef.max ?
        (cands.length ? '<div class="mg-picks">'+cands.slice(0,8).map(function(c){
            return '<button type="button" class="t3idea" data-trk-add="'+esc(c.t)+'"'+(c.gid?' data-gid="'+c.gid+'"':'')+'>'+ic('plus')+'<span>'+esc(c.t)+'</span></button>'; }).join('')+'</div>' : '')+
        '<div class="addrow"><input type="text" id="trkOwn" maxlength="40" placeholder="'+esc(t('ps.own'))+'">'+
          '<button class="btn btn-ghost" id="trkOwnAdd" aria-label="'+esc(t('c.add'))+'">'+ic('plus')+'</button></div>' : '')+
      period;
  } else build='<p class="hint">'+ic('sun')+'<span>'+esc(t('trk.day.h'))+'</span></p>';
  /* ticking on screen */
  var digital='';
  if(type!=='day' && cfg.rows.length){
    var cell=function(r,di,d){
      var arr=rec && rec.ticks[normLine(r.t)], on=!!(arr && arr[di]), fut=dayKey(d)>today, isT=dayKey(d)===today;
      return '<button type="button" class="trk-c'+(on?' on':'')+(fut?' fut':'')+(isT?' today':'')+'" data-trk-r="'+cfg.rows.indexOf(r)+'" data-trk-d="'+di+'"'+
        ' aria-pressed="'+on+'" aria-label="'+esc(r.t+' · '+trkLoc(d,{weekday:'long',day:'numeric',month:'numeric'}))+'">'+
        (type==='c30' ? '<span class="c30-n">'+(di+1)+'</span>' : '')+ic('check')+'</button>';
    };
    if(type==='c30'){
      var r0=cfg.rows[0], arr0=rec && rec.ticks[normLine(r0.t)], n0=arr0 ? arr0.filter(Boolean).length : 0;
      digital='<div class="trk-c30">'+days.map(function(d,di){ return cell(r0,di,d); }).join('')+'</div>'+
        (n0 ? '<p class="trk-count">'+esc(t('trk.c30.count',{n:n0}))+'</p>' : '');
    } else {
      digital='<div class="scroller"><table class="trk-grid '+type+'"><thead><tr><th class="mcol"></th>'+
        days.map(function(d){ return '<th class="'+(dayKey(d)===today?'today':'')+'"><span>'+esc(trkLoc(d,{weekday:'narrow'}))+'</span><b>'+d.getDate()+'</b></th>'; }).join('')+
        '</tr></thead><tbody>'+cfg.rows.map(function(r){
          var arr=rec && rec.ticks[normLine(r.t)], n=arr ? arr.filter(Boolean).length : 0;
          return '<tr><th class="mcol"><span>'+esc(r.t)+'</span>'+(n?'<b class="numf">✓'+n+'</b>':'')+'</th>'+
            days.map(function(d,di){ return '<td>'+cell(r,di,d)+'</td>'; }).join('')+'</tr>'; }).join('')+
        '</tbody></table></div>';
    }
    digital='<div class="trk-sec"><h3 class="boxh">'+ic('check')+'<span>'+esc(t('trk.dig'))+'</span></h3><p class="psub">'+esc(t('trk.dig.s'))+'</p>'+digital+
      '<label class="btn btn-ghost btn-block ps-cam">'+ic('camera')+'<span>'+esc(t(rec&&rec.photo?'trk.photo.again':'trk.photo'))+'</span>'+
        '<input type="file" accept="image/*" capture="environment" id="trkFile" class="hidden-file"></label>'+
      (rec&&rec.photo ? '<img class="ps-photo" src="'+rec.photo+'" alt="">' : '')+
      '<div id="trkReward"></div></div>';
  }
  var sty=trkStyle();
  var design='<details class="trk-design"'+(trkDesignOpen?' open':'')+'><summary>'+ic('palette')+'<span>'+esc(t('trk.design'))+'</span></summary>'+
    '<div class="mg-lab">'+esc(t('trk.d.color'))+'</div><div class="trk-swatches">'+Object.keys(TRK_COLORS).map(function(k){
      return '<button type="button" class="trk-sw'+(k==='ink'?' ink':'')+(sty.color===k?' on':'')+'" data-trk-color="'+k+'"'+(k==='ink'?'':' style="background:'+TRK_COLORS[k][0]+'"')+
        ' aria-label="'+esc(t('trk.c.'+k))+'" title="'+esc(t('trk.c.'+k))+'"></button>'; }).join('')+'</div>'+
    '<div class="mg-lab">'+esc(t('trk.d.look'))+'</div><div class="t3seg trk-looks" style="grid-template-columns:repeat(3,1fr)">'+['clean','fun','mini'].map(function(k){
      return '<button type="button" data-trk-look="'+k+'" class="'+(sty.look===k?'on':'')+'">'+esc(t('trk.l.'+k))+'</button>'; }).join('')+'</div>'+
    '<div class="field"><label for="trkTitle">'+esc(t('trk.d.title'))+'</label><input type="text" id="trkTitle" maxlength="40" value="'+esc(cfg.title||'')+'" placeholder="'+esc(t('trk.sheet.'+type))+'"></div>'+
    '</details>';
  var printSec='<div class="trk-sec"><h3 class="boxh">'+ic('share')+'<span>'+esc(t('trk.paper'))+'</span></h3>'+design+
    '<div class="sheet-wrap">'+trkSheetHtml(type,cfg)+'</div>'+
    '<button class="btn btn-primary btn-block" id="trkPrint">'+ic('share')+'<span>'+esc(t('ps.print'))+'</span></button>'+
    '<p class="hint">'+ic('sparkles')+'<span>'+esc(t('ps.print.h'))+'</span></p></div>';
  /* earlier tables, with their photos */
  var past=trkState().list.filter(function(x){ return x.key!==trkKey(type,cfg) && x.type===type; }).slice(-6).reverse();
  var pastSec=past.length ? '<div class="trk-sec"><div class="mg-lab">'+esc(t('trk.past'))+'</div><div class="ps-past">'+past.map(function(x){
      var n=0; Object.keys(x.ticks).forEach(function(k){ x.ticks[k].forEach(function(v){ if(v) n++; }); });
      return '<div class="ps-pastc">'+(x.photo?'<img src="'+x.photo+'" alt="">':ic('calendar'))+'<span>'+esc(fmtDay(x.key.split(':')[1]))+'</span><b class="numf">✓ '+n+'</b></div>'; }).join('')+'</div></div>' : '';
  box.innerHTML=tabs+'<div class="trk-sec">'+build+'</div>'+digital+printSec+pastSec;

  box.querySelectorAll('[data-trk]').forEach(function(b){ b.addEventListener('click',function(){ trkType=b.dataset.trk; renderTrackers(); }); });
  box.querySelectorAll('[data-trk-next]').forEach(function(b){ b.addEventListener('click',function(){ cfg.next=b.dataset.trkNext==='1'; save(); renderTrackers(); }); });
  box.querySelectorAll('[data-trk-del]').forEach(function(b){ b.addEventListener('click',function(){ cfg.rows.splice(Number(b.dataset.trkDel),1); save(); renderTrackers(); }); });
  box.querySelectorAll('[data-trk-add]').forEach(function(b){ b.addEventListener('click',function(){
    cfg.rows.push({t:b.dataset.trkAdd, gid:b.dataset.gid?Number(b.dataset.gid):null}); save(); renderTrackers(); }); });
  var dz=box.querySelector('.trk-design');
  if(dz) dz.addEventListener('toggle',function(){ trkDesignOpen=dz.open; });
  box.querySelectorAll('[data-trk-color]').forEach(function(b){ b.addEventListener('click',function(){ trkStyle().color=b.dataset.trkColor; save(); renderTrackers(); }); });
  box.querySelectorAll('[data-trk-look]').forEach(function(b){ b.addEventListener('click',function(){ trkStyle().look=b.dataset.trkLook; save(); renderTrackers(); }); });
  var ti=box.querySelector('#trkTitle');
  if(ti) ti.addEventListener('change',function(){ cfg.title=ti.value.trim(); save(); renderTrackers(); });
  box.querySelectorAll('[data-trk-emo]').forEach(function(b){
    b.addEventListener('click',function(){
      var i=Number(b.dataset.trkEmo), r=cfg.rows[i], k=TRK_EMO.indexOf(trkEmo(r,i));
      r.e=TRK_EMO[(k+1)%TRK_EMO.length]; save(); renderTrackers();
    });
  });
  var rs=box.querySelector('[data-trk-restart]');
  if(rs) rs.addEventListener('click',function(){ cfg.start=dayKey(); save(); renderTrackers(); });
  var own=box.querySelector('#trkOwn');
  if(own){ var add=function(){ var v=own.value.trim(); if(!v){ own.focus(); return; } cfg.rows.push({t:v}); save(); renderTrackers(); };
    box.querySelector('#trkOwnAdd').addEventListener('click',add);
    own.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); add(); } }); }
  box.querySelectorAll('[data-trk-r]').forEach(function(b){
    b.addEventListener('click',function(){ trkTick(type,cfg,cfg.rows[Number(b.dataset.trkR)],Number(b.dataset.trkD)); });
  });
  box.querySelector('#trkPrint').addEventListener('click',function(){
    if(tdef.max && !cfg.rows.length){ toast(t('ps.need')); return; }
    var root=document.getElementById('printRoot');
    if(!root){ root=document.createElement('div'); root.id='printRoot'; document.body.appendChild(root); }
    root.innerHTML=trkSheetHtml(type,cfg);
    document.body.classList.add('printing-sheet'); document.body.classList.toggle('print-portrait',type==='day');
    markActiveToday();
    setTimeout(function(){ window.print(); },50);
  });
  var f=box.querySelector('#trkFile');
  if(f) f.addEventListener('change',function(e){
    var file=e.target.files&&e.target.files[0]; if(!file) return;
    psShrink(file,function(photo){
      var r=trkRec(type,cfg,true); r.photo=photo;
      var first=!r.bonus; r.bonus=true;
      var before=levelInfo(); if(first) addPts(20);
      markActiveToday(); save();
      /* keep photos for the last six tables only */
      var withPhoto=trkState().list.filter(function(x){ return x.photo; });
      withPhoto.slice(0,Math.max(0,withPhoto.length-6)).forEach(function(x){ x.photo=null; });
      save(); renderTrackers(); trkReward(first?20:0, before);
    });
  });
}
function trkReward(gain, before){
  var after=levelInfo(), box=document.getElementById('trkReward'); if(!box) return;
  box.innerHTML='<div class="ps-reward"><div class="av-big t'+after.tier+'">'+avatarSvg(after.tier, avatarLabel(after))+'</div>'+
    '<div><p class="ps-rmsg">'+esc(t('trk.photo.ok'))+'</p>'+
    (gain ? '<p class="ps-rxp">'+esc(t('ps.rxp',{n:gain}))+'</p>' : '')+
    '<div class="xp big"><i style="width:'+after.pct+'%"></i></div>'+
    '<p class="ps-rlvl">'+esc(after.level>before.level ? t('av.lvlup',{n:after.level}) : t('av.next',{n:after.need, l:after.level+1}))+'</p></div></div>';
  box.scrollIntoView({block:'center',behavior:'smooth'});
  celebrate();
}
window.addEventListener('afterprint',function(){
  document.body.classList.remove('printing-sheet','print-portrait');
  var root=document.getElementById('printRoot'); if(root) root.innerHTML='';
});
/* a photo, shrunk on the phone so its storage is not filled */
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
"""
