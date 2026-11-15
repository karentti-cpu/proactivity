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
      '<span><small>'+esc(t('vis.lab'))+'</small><b>'+esc(v)+'</b></span>'+ic('edit','vis-edit')+'</button>'+
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
/* what a done day is marked with - on screen, and faintly in each printed box */
var TRK_MARKS={check:'✓', heart:'❤️', star:'⭐', fire:'🔥', smile:'😊', flower:'🌸', sun:'☀️', dot:'●'};
function trkMark(){ return trkStyle().mark||'check'; }
function trkMarkHtml(){ var m=trkMark(); return m==='check' ? ic('check') : '<span class="trk-m">'+TRK_MARKS[m]+'</span>'; }
var TRK_EMO=['🌟','💪','📚','🌿','💧','🎯','🎨','😊','🏃','🧘','🍎','😴','🎵','💰','❤️','✏️'];
function trkStyle(){ var st=trkState(); if(!st.style) st.style={color:'green', look:'clean'}; return st.style; }
var TRK_CAT_EMO={body:'💪', study:'📚', people:'❤️', money:'💰', calm:'🌿', create:'🎨'};
function trkEmo(r,i){
  if(r.e) return r.e;
  var g=r.gid && goalById(r.gid), c=g && goalCat(g);
  return (c && TRK_CAT_EMO[c]) || TRK_EMO[i%TRK_EMO.length];
}
/* whose tables: mine, or one of my children's - each child has tables,
   a look and a prize of their own */
function trkKid(){ var w=S.trkWho||'me'; if(w==='me') return null; return (S.kids||[]).filter(function(k){ return k.id===w; })[0]||null; }
function trkState(){
  var k=trkKid();
  if(k){ if(!k.trk) k.trk={cfg:{}, list:[], style:{color:'orange', look:'fun', mark:'star'}}; return k.trk; }
  if(!S.trk) S.trk={cfg:{}, list:[]};
  return S.trk;
}
/* a child's age: asked as a number, and turned into the group the
   questions and the habit ideas are written for */
function kidBandOf(n){ n=Number(n); return !n ? 'm' : n<=6 ? 's' : n<=9 ? 'm' : n<=12 ? 'l' : 't'; }
function kidSetAge(kid, n){ n=Math.max(2, Math.min(18, Math.round(Number(n)||0))); if(!n) return; kid.n=n; kid.age=kidBandOf(n); }
function kidAgeInput(id, val){
  return '<div class="kid-ageset"><button type="button" class="t3act" data-agestep="-1" aria-label="-">−</button>'+
    '<input type="number" id="'+id+'" min="2" max="18" inputmode="numeric" value="'+(val||'')+'" placeholder="?">'+
    '<button type="button" class="t3act" data-agestep="1" aria-label="+">+</button></div>';
}
function kidAgeRow(kid){
  return '<div class="kid-agerow"><label for="kidAgeIn">'+esc(t('kid.agefor',{n:kid.name}))+'</label>'+kidAgeInput('kidAgeIn', kid.n)+'</div>';
}
function kidAddForm(){
  return '<div class="trk-kidform"><input type="text" id="kidName" maxlength="20" placeholder="'+esc(t('kid.name'))+'">'+
    '<div class="kid-agerow plain"><label for="kidAgeNew">'+esc(t('kid.age'))+'</label>'+kidAgeInput('kidAgeNew','')+'</div>'+
    '<div class="row-btns"><button class="btn btn-primary btn-sm" id="kidSave">'+esc(t('kid.save'))+'</button></div></div>';
}
/* the − / + buttons next to an age field */
function kidStepBind(box){
  box.querySelectorAll('[data-agestep]').forEach(function(b){ b.addEventListener('click',function(){
    var inp=b.parentNode.querySelector('input'), v=Number(inp.value)||8; inp.value=Math.max(2,Math.min(18,v+Number(b.dataset.agestep)));
    inp.dispatchEvent(new Event('change')); }); });
}
function kidBind(box, kid, onDone){
  kidStepBind(box);
  var ai=box.querySelector('#kidAgeIn');
  if(ai && kid) ai.addEventListener('change',function(){ if(!ai.value) return; kidSetAge(kid, ai.value); save(); onDone(kid); });
  var sv=box.querySelector('#kidSave');
  if(sv) sv.addEventListener('click',function(){
    var inp=box.querySelector('#kidName'), nm=inp.value.trim(), ag=box.querySelector('#kidAgeNew');
    if(!nm){ inp.focus(); return; } if(!ag.value){ ag.focus(); return; }
    if(!S.kids) S.kids=[]; var k={id:uid++, name:nm}; kidSetAge(k, ag.value); S.kids.push(k); save(); onDone(k, true);
  });
}
var KID_HABITS={s:[1,2,3,4,5,6,12,13], m:[1,7,8,9,10,4,5,12,13,14], l:[15,16,10,11,13,14,5,12], t:[15,16,17,18,10,11,14,13]};
function trkCfg(type){
  var st=trkState();
  if(!st.cfg[type]){
    var gs=trkKid() ? [] : liveGoals().map(function(g){ return {t:g.title, gid:g.id}; });
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
  var mk=trkMark(), faint = mk==='check' ? '' : '<span class="sg-faint">'+TRK_MARKS[mk]+'</span>';
  var col=TRK_COLORS[sty.color]||TRK_COLORS.green;
  var kid=trkKid();
  var title=(cfg.title||'').trim() || (kid ? t('kid.title',{n:kid.name}) : t('trk.sheet.'+type));
  var who=kid ? kid.name : P.name;
  var head='<div class="sheet-top"><div><h3>'+esc(title)+'</h3><p>'+esc(trkTitle(type,days))+(who?' · '+esc(who):'')+'</p></div>'+
      '<div class="sheet-brand">Proacty</div></div>'+
    (vis && !kid ? '<p class="sheet-vis">'+esc(t('vis.lab'))+': <b>'+esc(vis)+'</b></p>' : '')+
    (kid ? '<p class="sheet-vis sheet-prize">'+esc(t('kid.prize'))+' <b>'+esc(cfg.prize||'')+'</b>'+(cfg.prize?'':' ______________')+'</p>' : '')+
    (type!=='day' ? '<p class="sheet-vis">'+esc(t('trk.markwith',{m:TRK_MARKS[mk]}))+'</p>' : '');
  var foot='<div class="sheet-foot">'+esc(t('sp.line'))+'</div>';
  var body='';
  if(type==='week' || type==='month'){
    var rows=cfg.rows.length ? cfg.rows.slice() : [];
    var minRows=type==='week'?4:3;
    while(rows.length<minRows) rows.push({t:''});
    var rowH = type==='week' ? Math.max(46, Math.min(84, Math.floor(400/rows.length))) : Math.max(40, Math.min(80, Math.floor(380/rows.length)));
    body='<table class="sheet-grid '+type+'"><thead><tr><th class="sg-goal">'+esc(t(kid?'kid.col':'ps.col.goal'))+'</th>'+
      days.map(function(d){ return '<th><span>'+esc(type==='week'?trkLoc(d,{weekday:'short'}):trkLoc(d,{weekday:'narrow'}))+'</span><b>'+d.getDate()+'</b></th>'; }).join('')+
      '<th class="sg-sum">'+esc(t('ps.col.sum'))+'</th></tr></thead><tbody>'+
      rows.map(function(r,i){ return '<tr style="height:'+rowH+'px"><td class="sg-goal">'+(r.t && (fun||r.e) ? '<span class="sg-emo">'+trkEmo(r,i)+'</span>' : '')+esc(r.t)+'</td>'+days.map(function(){ return '<td>'+(r.t?faint:'')+'</td>'; }).join('')+'<td class="sg-sum"></td></tr>'; }).join('')+
      '</tbody></table>'+
      '<div class="sheet-lines"><p>'+esc(t(kid ? (type==='month'?'kid.q1m':'kid.q1w') : (type==='month'?'trk.q1m':'wr.q1')))+'</p>'+
        '<p>'+esc(t(kid ? (type==='month'?'kid.q2m':'kid.q2w') : (type==='month'?'trk.q2m':'wr.q2')))+'</p></div>';
  } else if(type==='c30'){
    var g=cfg.rows[0];
    body='<p class="sheet-c30goal">'+(fun&&g ? '<span>'+trkEmo(g,0)+'</span>' : ic('flame'))+'<b>'+esc(g?g.t:'')+'</b></p>'+
      '<div class="sheet-c30">'+days.map(function(d,i){
        return '<div class="c30-box"><span class="c30-n">'+(i+1)+'</span><span class="c30-d">'+esc(trkLoc(d,{day:'numeric',month:'numeric'}))+'</span>'+faint+'</div>'; }).join('')+'</div>'+
      (kid ? '' : '<div class="sheet-lines"><p>'+esc(t('trk.prize'))+'</p></div>');
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
  var kid=trkKid();
  if(kid){
    /* a child's ticks are the child's: a cheer, and a party at a streak */
    if(on){ var ks=trkStreak(rec.ticks[key], di);
      if([3,7,14,21,30].indexOf(ks)>=0){ toast(t('trk.streak',{n:ks, g:row.t})); celebrate(); } else toast(t('kid.cheer',{n:kid.name})); }
    save(); renderTrackers(); return;
  }
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
  save(); renderTrackers(); if(typeof renderPath==='function') renderPath();
}

/* ---- the page ----
   Built around the table itself: whose (me or a child), which kind (small
   tabs), then the table - rows edited in place, ticked with a tap - and
   under it print, design and a photo of a ticked sheet. */
var trkDesignOpen=false, trkEditRow=-1, trkKidForm=false, trkKidEdit=false;
function trkCands(cfg){
  var have={}; cfg.rows.forEach(function(r){ have[normLine(r.t)]=1; });
  var kid=trkKid(), list;
  if(kid) list=(KID_HABITS[kid.age]||KID_HABITS.m).map(function(n){ return {t:t('kh.'+n)}; });
  else list=liveGoals().map(function(g){ return {t:g.title, gid:g.id}; }).concat((S.missions||[]).map(function(m){ return {t:label(m)}; }));
  return list.filter(function(c,i,a){ return !have[normLine(c.t)] && a.findIndex(function(x){ return normLine(x.t)===normLine(c.t); })===i; });
}
function renderTrackers(){
  var box=document.getElementById('trkBox'); if(!box) return;
  var kid=trkKid(); if(!kid && S.trkWho && S.trkWho!=='me') S.trkWho='me';
  if(kid && trkType==='day') trkType='week';
  var type=trkType, cfg=trkCfg(type), tdef=TRK_TYPES.filter(function(x){ return x.id===type; })[0];
  var days=trkDays(type,cfg), rec=trkRec(type,cfg,false), today=dayKey();
  /* whose */
  var who='<div class="trk-who"><span class="trk-who-l">'+esc(t('who.t'))+'</span>'+
    '<button type="button" class="trk-wb'+(!kid?' on':'')+'" data-who="me">'+ic('user')+'<span>'+esc(t('who.me'))+'</span></button>'+
    (S.kids||[]).map(function(k){ return '<button type="button" class="trk-wb kid'+(kid&&kid.id===k.id?' on':'')+'" data-who="'+k.id+'">⭐<span>'+esc(k.name)+'</span></button>'; }).join('')+
    '<button type="button" class="trk-wb add" data-kid-add>'+ic('plus')+'<span>'+esc(t('who.add'))+'</span></button>'+
    (kid ? '<button type="button" class="t3act" data-kid-edit aria-label="'+esc(t('kid.edit'))+'" title="'+esc(t('kid.edit'))+'">'+ic('edit')+'</button>' : '')+'</div>';
  var kf=trkKidForm ? kidAddForm() : (trkKidEdit && kid) ? '<div class="trk-kidform"><input type="text" id="kidName" maxlength="20" value="'+esc(kid.name)+'">'+
      '<div class="row-btns"><button class="btn btn-primary btn-sm" id="kidRename">'+esc(t('c.save'))+'</button>'+
      '<button class="btn btn-quiet btn-sm" id="kidDel">'+esc(t('kid.del',{n:kid.name}))+'</button></div></div>' : '';
  /* which kind */
  var tabs='<div class="t3seg trk-tabs'+(kid?' three':'')+'">'+TRK_TYPES.filter(function(x){ return !(kid && x.id==='day'); }).map(function(x){
    return '<button type="button" data-trk="'+x.id+'" class="'+(x.id===type?'on':'')+'">'+esc(t('trk.'+x.id))+'</button>'; }).join('')+'</div>';
  /* the table */
  var title=(cfg.title||'').trim() || (kid ? t('kid.title',{n:kid.name}) : t('trk.sheet.'+type));
  var period = type==='c30'
    ? '<div class="trk-period">'+esc(t('trk.c30.from',{d:fmtDay(cfg.start)}))+' <button class="btn btn-quiet btn-sm" data-trk-restart>'+ic('refresh')+'<span>'+esc(t('trk.c30.new'))+'</span></button></div>'
    : type==='day' ? '' : '<div class="t3seg ps-week"><button type="button" data-trk-next="0" class="'+(cfg.next?'':'on')+'">'+esc(t(type==='week'?'wk.this':'trk.thism'))+'</button>'+
        '<button type="button" data-trk-next="1" class="'+(cfg.next?'on':'')+'">'+esc(t(type==='week'?'wk.next':'trk.nextm'))+'</button></div>';
  var nameCell=function(r,i){
    return trkEditRow===i
      ? '<input type="text" class="trk-rin" data-trk-rin="'+i+'" maxlength="40" value="'+esc(r.t)+'">'
      : '<button type="button" class="trk-rname" data-trk-rname="'+i+'"><span class="trk-remo">'+trkEmo(r,i)+'</span><span>'+esc(r.t)+'</span></button>';
  };
  var cell=function(r,di,d){
    var arr=rec && rec.ticks[normLine(r.t)], on=!!(arr && arr[di]), fut=dayKey(d)>today, isT=dayKey(d)===today;
    return '<button type="button" class="trk-c'+(on?' on':'')+(fut?' fut':'')+(isT?' today':'')+'" data-trk-r="'+cfg.rows.indexOf(r)+'" data-trk-d="'+di+'"'+
      ' aria-pressed="'+on+'" aria-label="'+esc(r.t+' · '+trkLoc(d,{weekday:'long',day:'numeric',month:'numeric'}))+'">'+
      (type==='c30' ? '<span class="c30-n">'+(di+1)+'</span>' : '')+trkMarkHtml()+'</button>';
  };
  var grid='';
  if(type==='day') grid='<p class="hint">'+ic('sun')+'<span>'+esc(t('trk.day.h'))+'</span></p>';
  else if(!cfg.rows.length) grid='<p class="trk-emptymsg">'+esc(t('trk.empty'))+'</p>';
  else if(type==='c30'){
    var r0=cfg.rows[0], arr0=rec && rec.ticks[normLine(r0.t)], n0=arr0 ? arr0.filter(Boolean).length : 0;
    grid='<div class="trk-c30goal">'+nameCell(r0,0)+'<button class="icon-btn" data-trk-del="0" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></div>'+
      '<div class="trk-c30">'+days.map(function(d,di){ return cell(r0,di,d); }).join('')+'</div>'+
      (n0 ? '<p class="trk-count">'+esc(t('trk.c30.count',{n:n0}))+'</p>' : '');
  } else {
    grid='<div class="scroller"><table class="trk-grid '+type+'"><thead><tr><th class="mcol"></th>'+
      days.map(function(d){ return '<th class="'+(dayKey(d)===today?'today':'')+'"><span>'+esc(trkLoc(d,{weekday:'narrow'}))+'</span><b>'+d.getDate()+'</b></th>'; }).join('')+
      '</tr></thead><tbody>'+cfg.rows.map(function(r,i){
        var arr=rec && rec.ticks[normLine(r.t)], n=arr ? arr.filter(Boolean).length : 0;
        return '<tr><th class="mcol">'+nameCell(r,i)+(n?'<b class="numf">✓'+n+'</b>':'')+
          '<button class="trk-rdel" data-trk-del="'+i+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></th>'+
          days.map(function(d,di){ return '<td>'+cell(r,di,d)+'</td>'; }).join('')+'</tr>'; }).join('')+
      '</tbody></table></div><p class="trk-edith">'+esc(t('trk.edit.h'))+'</p>';
  }
  var cands=tdef.max ? trkCands(cfg) : [];
  var adder = (tdef.max && cfg.rows.length<tdef.max) ?
    '<div class="addrow trk-addrow"><input type="text" id="trkOwn" maxlength="40" placeholder="'+esc(kid?t('trk.addrow'):t('ps.own'))+'">'+
      '<button class="btn btn-ghost" id="trkOwnAdd">'+ic('plus')+'<span>'+esc(t('trk.addrow'))+'</span></button></div>'+
    (cands.length ? '<div class="mg-picks trk-ideas"><span class="trk-ideas-l">'+esc(t('trk.ideas'))+'</span>'+cands.slice(0,8).map(function(c){
        return '<button type="button" class="t3idea" data-trk-add="'+esc(c.t)+'"'+(c.gid?' data-gid="'+c.gid+'"':'')+'>'+ic('plus')+'<span>'+esc(c.t)+'</span></button>'; }).join('')+'</div>' : '') : '';
  var prize = kid && type!=='day' ? '<div class="field trk-prize"><label for="kidPrize">'+esc(t('kid.prize'))+'</label>'+
      '<input type="text" id="kidPrize" maxlength="60" value="'+esc(cfg.prize||'')+'" placeholder="'+esc(t('kid.prize.ph'))+'"></div>' : '';
  var sty=trkStyle();
  var main='<section class="trk-main'+(kid?' kid':'')+(trkMark()==='check'?'':' trk-emomark')+'" style="--sc:'+(TRK_COLORS[sty.color]||TRK_COLORS.green)[0]+'">'+
    '<div class="trk-head"><h3>'+esc(title)+'</h3><span>'+esc(trkTitle(type,days))+'</span></div>'+period+grid+adder+prize+
    (kid ? '<p class="trk-kidnote">'+esc(t('kid.note',{n:kid.name}))+'</p>' : '')+
    '<div class="trk-actions"><button class="btn btn-primary" id="trkPrint">'+ic('share')+'<span>'+esc(t('trk.printb'))+'</span></button>'+
      '<button class="btn btn-ghost'+(trkDesignOpen?' on':'')+'" id="trkDesign">'+ic('palette')+'<span>'+esc(t('trk.designb'))+'</span></button>'+
      (type!=='day' ? '<label class="btn btn-quiet trk-cam" title="'+esc(t('trk.photob'))+'">'+ic('camera')+'<input type="file" accept="image/*" capture="environment" id="trkFile" class="hidden-file"></label>' : '')+'</div>'+
    (rec&&rec.photo ? '<img class="ps-photo" src="'+rec.photo+'" alt="">' : '')+'<div id="trkReward"></div></section>';
  var design=trkDesignOpen ? '<section class="trk-sec trk-designp">'+
    '<div class="mg-lab">'+esc(t('trk.d.color'))+'</div><div class="trk-swatches">'+Object.keys(TRK_COLORS).map(function(k){
      return '<button type="button" class="trk-sw'+(k==='ink'?' ink':'')+(sty.color===k?' on':'')+'" data-trk-color="'+k+'"'+(k==='ink'?'':' style="background:'+TRK_COLORS[k][0]+'"')+
        ' aria-label="'+esc(t('trk.c.'+k))+'" title="'+esc(t('trk.c.'+k))+'"></button>'; }).join('')+'</div>'+
    '<div class="mg-lab">'+esc(t('trk.d.mark'))+'</div><div class="trk-marks">'+Object.keys(TRK_MARKS).map(function(k){
      return '<button type="button" class="trk-mk'+(trkMark()===k?' on':'')+'" data-trk-mark="'+k+'" aria-label="'+esc(t('trk.m.'+k))+'" title="'+esc(t('trk.m.'+k))+'">'+(k==='check'?ic('check'):TRK_MARKS[k])+'</button>'; }).join('')+'</div>'+
    '<div class="mg-lab">'+esc(t('trk.d.look'))+'</div><div class="t3seg trk-looks" style="grid-template-columns:repeat(3,1fr)">'+['clean','fun','mini'].map(function(k){
      return '<button type="button" data-trk-look="'+k+'" class="'+(sty.look===k?'on':'')+'">'+esc(t('trk.l.'+k))+'</button>'; }).join('')+'</div>'+
    '<div class="field"><label for="trkTitle">'+esc(t('trk.d.title'))+'</label><input type="text" id="trkTitle" maxlength="40" value="'+esc(cfg.title||'')+'" placeholder="'+esc(kid?t('kid.title',{n:kid.name}):t('trk.sheet.'+type))+'"></div>'+
    '<div class="mg-lab">'+esc(t('trk.paper'))+'</div><div class="sheet-wrap">'+trkSheetHtml(type,cfg)+'</div>'+
    '<p class="hint">'+ic('sparkles')+'<span>'+esc(t('ps.print.h'))+'</span></p></section>' : '';
  var past=trkState().list.filter(function(x){ return x.key!==trkKey(type,cfg) && x.type===type; }).slice(-6).reverse();
  var pastSec=past.length ? '<div class="trk-sec"><div class="mg-lab">'+esc(t('trk.past'))+'</div><div class="ps-past">'+past.map(function(x){
      var n=0; Object.keys(x.ticks).forEach(function(k){ x.ticks[k].forEach(function(v){ if(v) n++; }); });
      return '<div class="ps-pastc">'+(x.photo?'<img src="'+x.photo+'" alt="">':ic('calendar'))+'<span>'+esc(fmtDay(x.key.split(':')[1]))+'</span><b class="numf">✓ '+n+'</b></div>'; }).join('')+'</div></div>' : '';
  box.innerHTML=who+kf+(kid && !trkKidEdit ? kidAgeRow(kid) : '')+tabs+main+design+pastSec;
  if(kid && !trkKidEdit && !trkKidForm) kidBind(box, kid, function(){ renderTrackers(); });

  /* whose */
  box.querySelectorAll('[data-who]').forEach(function(b){ b.addEventListener('click',function(){
    S.trkWho=b.dataset.who==='me'?'me':Number(b.dataset.who); trkKidForm=false; trkKidEdit=false; trkEditRow=-1; save(); renderTrackers(); }); });
  box.querySelector('[data-kid-add]').addEventListener('click',function(){ trkKidForm=!trkKidForm; trkKidEdit=false; renderTrackers();
    var n=document.getElementById('kidName'); if(n) n.focus(); });
  var ke=box.querySelector('[data-kid-edit]'); if(ke) ke.addEventListener('click',function(){ trkKidEdit=!trkKidEdit; trkKidForm=false; renderTrackers(); });
  if(trkKidForm) kidBind(box, null, function(k){ S.trkWho=k.id; trkKidForm=false; save(); renderTrackers(); });
  var kr=box.querySelector('#kidRename');
  if(kr) kr.addEventListener('click',function(){ var nm=document.getElementById('kidName').value.trim(); if(!nm) return; kid.name=nm; trkKidEdit=false; save(); renderTrackers(); });
  var kd=box.querySelector('#kidDel');
  if(kd) kd.addEventListener('click',function(){
    if(!confirm(t('kid.del',{n:kid.name})+'?')) return;
    S.kids=S.kids.filter(function(k){ return k!==kid; }); S.trkWho='me'; trkKidEdit=false; save(); renderTrackers(); });
  /* the table */
  box.querySelectorAll('[data-trk]').forEach(function(b){ b.addEventListener('click',function(){ trkType=b.dataset.trk; trkEditRow=-1; renderTrackers(); }); });
  box.querySelectorAll('[data-trk-next]').forEach(function(b){ b.addEventListener('click',function(){ cfg.next=b.dataset.trkNext==='1'; save(); renderTrackers(); }); });
  box.querySelectorAll('[data-trk-del]').forEach(function(b){ b.addEventListener('click',function(){ cfg.rows.splice(Number(b.dataset.trkDel),1); trkEditRow=-1; save(); renderTrackers(); }); });
  box.querySelectorAll('[data-trk-add]').forEach(function(b){ b.addEventListener('click',function(){
    cfg.rows.push({t:b.dataset.trkAdd, gid:b.dataset.gid?Number(b.dataset.gid):null}); save(); renderTrackers(); }); });
  box.querySelectorAll('[data-trk-rname]').forEach(function(b){ b.addEventListener('click',function(){
    trkEditRow=Number(b.dataset.trkRname); renderTrackers(); var inp=box.querySelector('[data-trk-rin]'); if(inp){ inp.focus(); inp.select(); } }); });
  box.querySelectorAll('[data-trk-rin]').forEach(function(inp){
    var done=function(){
      var i=Number(inp.dataset.trkRin), r=cfg.rows[i], v=inp.value.trim(); trkEditRow=-1;
      if(r && v && v!==r.t){
        /* the ticks follow the row to its new name */
        trkState().list.forEach(function(x){ var o=normLine(r.t); if(x.ticks[o]){ x.ticks[normLine(v)]=x.ticks[o]; delete x.ticks[o]; } });
        r.t=v; save();
      }
      renderTrackers();
    };
    inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); done(); } if(e.key==='Escape'){ trkEditRow=-1; renderTrackers(); } });
    inp.addEventListener('blur',done);
  });
  var pz2=box.querySelector('#kidPrize');
  if(pz2) pz2.addEventListener('change',function(){ cfg.prize=pz2.value.trim(); save(); });
  var rs=box.querySelector('[data-trk-restart]');
  if(rs) rs.addEventListener('click',function(){ cfg.start=dayKey(); save(); renderTrackers(); });
  var own=box.querySelector('#trkOwn');
  if(own){ var add=function(){ var v=own.value.trim(); if(!v){ own.focus(); return; } cfg.rows.push({t:v}); save(); renderTrackers();
      var o2=document.getElementById('trkOwn'); if(o2) o2.focus(); };
    box.querySelector('#trkOwnAdd').addEventListener('click',add);
    own.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); add(); } }); }
  box.querySelectorAll('[data-trk-r]').forEach(function(b){
    b.addEventListener('click',function(){ trkTick(type,cfg,cfg.rows[Number(b.dataset.trkR)],Number(b.dataset.trkD)); });
  });
  /* design, print, photo */
  box.querySelector('#trkDesign').addEventListener('click',function(){ trkDesignOpen=!trkDesignOpen; renderTrackers();
    if(trkDesignOpen){ var d=box.querySelector('.trk-designp'); if(d) d.scrollIntoView({behavior:'smooth',block:'start'}); } });
  box.querySelectorAll('[data-trk-color]').forEach(function(b){ b.addEventListener('click',function(){ trkStyle().color=b.dataset.trkColor; save(); renderTrackers(); }); });
  box.querySelectorAll('[data-trk-mark]').forEach(function(b){ b.addEventListener('click',function(){ trkStyle().mark=b.dataset.trkMark; save(); renderTrackers(); }); });
  box.querySelectorAll('[data-trk-look]').forEach(function(b){ b.addEventListener('click',function(){ trkStyle().look=b.dataset.trkLook; save(); renderTrackers(); }); });
  var ti=box.querySelector('#trkTitle');
  if(ti) ti.addEventListener('change',function(){ cfg.title=ti.value.trim(); save(); renderTrackers(); });
  box.querySelector('#trkPrint').addEventListener('click',function(){
    if(tdef.max && !cfg.rows.length){ toast(t('ps.need')); return; }
    var root=document.getElementById('printRoot');
    if(!root){ root=document.createElement('div'); root.id='printRoot'; document.body.appendChild(root); }
    root.innerHTML=trkSheetHtml(type,cfg);
    document.body.classList.add('printing-sheet'); document.body.classList.toggle('print-portrait',type==='day');
    if(!kid) markActiveToday();
    setTimeout(function(){ window.print(); },50);
  });
  var f=box.querySelector('#trkFile');
  if(f) f.addEventListener('change',function(e){
    var file=e.target.files&&e.target.files[0]; if(!file) return;
    psShrink(file,function(photo){
      var r=trkRec(type,cfg,true); r.photo=photo;
      var first=!r.bonus; r.bonus=true;
      var before=levelInfo(); if(first && !kid) addPts(20);
      if(!kid) markActiveToday(); save();
      var withPhoto=trkState().list.filter(function(x){ return x.photo; });
      withPhoto.slice(0,Math.max(0,withPhoto.length-6)).forEach(function(x){ x.photo=null; });
      save(); renderTrackers(); trkReward(first&&!kid?20:0, before);
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


/* ================= games: a minute that builds proactive thinking =================
   Five short games, one tap a card, kind feedback right away and never a
   "wrong": in my hands or not; flip a reactive sentence; a moment before
   reacting; the first step; a speed round. Cards are chosen for the age
   (up to 17 / 18 and up).
   The games learn the player: each card remembers how it went, so new
   cards and the ones that were hard come first and the easy ones rest; the
   level rises after two right answers in a row and eases after a miss;
   Today's game leans to the game that needs practice; and the end of a
   round says what the games have learned. */
/* each card: [number, level]; circle and speed cards also carry their
   answer. Level 3-4 bring the subtle ones: in my hands only in part, and a
   fourth answer that sounds reasonable but still lets others decide. */
var GAME_CIRCLE={k:[[1,1,'in'],[2,1,'out'],[3,1,'in'],[4,1,'out'],[5,2,'in'],[6,2,'out'],[7,2,'in'],[8,2,'out'],[9,3,'part'],[10,3,'part'],[11,3,'part'],[12,4,'in']],
                 t:[[1,1,'in'],[2,1,'out'],[3,1,'in'],[4,1,'out'],[5,2,'in'],[6,2,'out'],[7,2,'in'],[8,2,'out'],[9,3,'part'],[10,3,'part'],[11,3,'part'],[12,3,'part'],[13,4,'part'],[14,4,'in'],[15,4,'out']],
                 a:[[1,1,'in'],[2,1,'out'],[3,1,'in'],[4,1,'out'],[5,2,'in'],[6,2,'out'],[7,2,'in'],[8,2,'out'],[9,3,'part'],[10,3,'part'],[11,3,'part'],[12,3,'part'],[13,4,'in'],[14,4,'out'],[15,4,'part']]};
var GAME_FLIP=[[1,1],[2,1],[4,1],[5,1],[9,1],[3,2],[6,2],[7,2],[8,2],[10,2],[11,3],[12,3],[13,3],[14,3],[15,3],[16,4],[17,4],[18,4]];
var GAME_REACT={k:[[1,1],[2,1],[3,2],[4,2],[5,3],[6,3]], t:[[1,1],[3,1],[6,1],[2,2],[4,2],[5,2],[7,3],[8,3],[9,3],[10,4],[11,4]], a:[[4,1],[5,1],[6,1],[1,2],[2,2],[3,2],[7,3],[8,3],[9,3],[10,4],[11,4]]};
var GAME_STEP=[[1,1],[2,1],[3,1],[4,2],[5,2],[6,3],[7,3],[8,4],[9,4],[10,4]];
var GAME_SPEED=[[1,1,'c'],[2,1,'r'],[3,1,'c'],[4,1,'r'],[5,1,'c'],[6,1,'r'],[7,1,'c'],[8,1,'r'],[9,2,'c'],[10,2,'r'],[11,2,'c'],[12,2,'r'],
                [13,2,'c'],[14,2,'r'],[15,2,'c'],[16,2,'r'],[17,3,'r'],[18,3,'c'],[19,3,'r'],[20,3,'c'],[21,3,'r'],[22,3,'c'],[23,3,'r'],[24,3,'c']];
/* calm: [number, level, the feeling the situation brings] */
var GAME_CALM=[[1,1,'angry'],[2,1,'stress'],[3,1,'tired'],[4,2,'hurt'],[5,2,'frust'],[6,3,'disap'],[7,3,'fear'],[8,4,'angry'],[9,4,'stress'],[10,4,'sad']];
/* the twenty feelings, and the feeling game: [number, level, answer, the feelings close to it] */
var FEELINGS=[{k:'joy',e:'😄'},{k:'pride',e:'🏆'},{k:'relief',e:'😮‍💨'},{k:'grat',e:'🙏'},{k:'excite',e:'🤩'},{k:'curious',e:'🧐'},{k:'calm',e:'😌'},
  {k:'anger',e:'😠'},{k:'frust',e:'😤'},{k:'hurt',e:'😔'},{k:'jeal',e:'😒'},{k:'shame',e:'🙈'},{k:'embar',e:'😳'},{k:'guilt',e:'😣'},
  {k:'fear',e:'😨'},{k:'worry',e:'😟'},{k:'sad',e:'😢'},{k:'disap',e:'😞'},{k:'lonely',e:'🥺'},{k:'bored',e:'🥱'}];
var GAME_FEEL=[[1,1,'joy',['excite']],[2,1,'fear',['worry']],[3,1,'anger',['frust']],[4,1,'sad',['lonely']],[5,1,'excite',['joy']],[6,1,'bored',['calm']],
  [7,2,'relief',['joy']],[8,2,'pride',['joy']],[9,2,'grat',['joy']],[10,2,'disap',['sad']],[11,2,'worry',['fear']],[12,2,'lonely',['sad']],[13,2,'curious',['excite']],[14,2,'calm',['relief']],
  [15,3,'guilt',['shame','fear']],[16,3,'embar',['shame','hurt']],[17,3,'jeal',['disap','anger']],[18,3,'frust',['anger','disap']],[19,3,'hurt',['anger','shame']],[20,3,'disap',['sad','frust']],
  [21,4,'shame',['embar','guilt']],[22,4,'worry',['fear','shame']],[23,4,'relief',['calm','joy']],[24,4,'lonely',['sad','bored']]];
function feelOf(k){ return FEELINGS.filter(function(x){ return x.k===k; })[0]; }
function feelDict(){
  return '<details class="fl-dict"><summary>'+ic('book')+'<span><b>'+esc(t('gm.dict'))+'</b><small>'+esc(t('gm.dict.s'))+'</small></span>'+ic('chevron','fl-c')+'</summary>'+
    '<div class="fl-grid">'+FEELINGS.map(function(f){
      return '<div class="fl-item"><span class="fl-e">'+f.e+'</span><span><b>'+esc(t('fe.'+f.k))+'</b><small>'+esc(t('fe.'+f.k+'.m'))+'</small></span></div>'; }).join('')+'</div></details>';
}
var GAME_IDS=[{id:'circle',icon:'compass'},{id:'flip',icon:'refresh'},{id:'react',icon:'shield'},{id:'calm',icon:'wind'},{id:'feel',icon:'face'},{id:'step',icon:'flag'},{id:'speed',icon:'zap'}];
/* positive psychology games: the good glasses and talking to yourself like a
   friend work like calm; which strength is it works like the feeling game */
var GAME_OPT=[[1,1],[2,1],[3,2],[4,2],[5,3],[6,3],[7,4],[8,4]];
var GAME_KIND=[[1,1],[2,1],[3,2],[4,2],[5,3],[6,3],[7,4],[8,4]];
var GAME_STR=[[1,1,'curious',['learn']],[2,1,'brave',['fair','lead']],[3,1,'kind',['grat']],[4,1,'humor',['create']],
  [5,2,'persist',['hope','brave']],[6,2,'create',['humor','curious']],[7,2,'grat',['hope','kind']],
  [8,3,'fair',['lead','kind']],[9,3,'hope',['persist','grat']],[10,3,'learn',['curious','persist']],
  [11,4,'lead',['fair','brave']],[12,4,'self',['brave','persist']]];
GAME_IDS=GAME_IDS.concat([{id:'opt',icon:'sun'},{id:'kind',icon:'seedling'},{id:'str',icon:'gem'}]);
/* games whose answers are a set of words: feelings, strengths */
var GM_WORDS={feel:{keys:function(){ return FEELINGS.map(function(f){ return f.k; }); }, lab:function(k){ return t('fe.'+k); }, emo:function(k){ var f=feelOf(k); return f?f.e:''; }},
              str:{keys:function(){ return VS_KEYS; }, lab:function(k){ return t('vs.'+k); }, emo:function(){ return ''; }}};
var GAME_NEW=['step','speed','calm','feel','opt','kind','str'], GAME_LEN=6, GAME_SECS=45;
var gmRun=null, gmTick=null;
/* who is playing: me, one of my children, or someone else (an age group,
   nothing saved). The cards follow the player's age: k up to 12, t up to
   17, a for adults. A child's progress is kept with the child, and only my
   own rounds give XP and count for Today's game and the daily path. */
var gmPlayer={k:'me'}, gmGuest=null, gmKidForm=false;
function gmKidP(){ return gmPlayer.k==='kid' ? (S.kids||[]).filter(function(k){ return k.id===gmPlayer.id; })[0]||null : null; }
function gmIsMe(){ return gmPlayer.k==='me' || (gmPlayer.k==='kid' && !gmKidP()); }
function gmAge(){
  if(gmPlayer.k==='guest') return gmPlayer.band||'a';
  var kd=gmKidP(); if(kd) return kd.age==='t' ? 't' : 'k';
  var n=Number(P.age);
  if(n && n<=12) return 'k';
  return (!P.age || ageBand(P.age)==='a13') ? 't' : 'a';
}
/* cards that do not suit children are left out of their rounds */
var GM_NOKIDS={feel:[7,11,12], step:[9], calm:[8]};
function gmShuffle(a){ a=a.slice(); for(var i=a.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)); var x=a[i]; a[i]=a[j]; a[j]=x; } return a; }
function gmNorm(o){ ['lvl','mem','acc','played'].forEach(function(k){ if(!o[k]) o[k]={}; }); return o; }
function gmMine(){ if(!S.games) S.games={played:{}, daily:null}; return gmNorm(S.games); }
function gmState(){
  var kd=gmKidP();
  if(kd){ if(!kd.games) kd.games={played:{}}; return gmNorm(kd.games); }
  if(gmPlayer.k==='guest'){ if(!gmGuest) gmGuest={played:{}}; return gmNorm(gmGuest); }
  return gmMine();
}
/* Today's game: one a day, never the same as yesterday, leaning to a game
   not tried yet, then to the one with the fewest right answers */
function gmDaily(){
  var st=gmMine(), today=dayKey();
  if(st.dpick && st.dpick.day===today) return st.dpick.id;
  var prev=st.dpick && st.dpick.id, d=new Date(), n=Math.floor((d-new Date(d.getFullYear(),0,0))/864e5), best=null, bs=99;
  GAME_IDS.forEach(function(g,i){
    if(g.id===prev) return;
    var a=st.acc[g.id], s=!st.played[g.id] ? -1 : (a && a[0] ? a[1]/a[0] : .5);
    if(g.id==='react' && hasProfile() && weakDim()==='choice') s-=.15;
    s+=((i+n)%GAME_IDS.length)*.01;
    if(s<bs){ bs=s; best=g.id; }
  });
  st.dpick={day:today, id:best};
  return best;
}
function gmPool(id){
  var pool=gmPoolAll(id), no=gmAge()==='k' && GM_NOKIDS[id];
  if(no) pool=pool.filter(function(c){ var n=Number((c.key.match(/(\d+)$/)||[])[1]); return no.indexOf(n)<0; });
  return pool;
}
function gmPoolAll(id){
  var age=gmAge(), pool=[];
  if(id==='circle') GAME_CIRCLE[age].forEach(function(c){ pool.push({key:'gm.circle.'+age+c[0], lv:c[1], ans:c[2]}); });
  else if(id==='feel') GAME_FEEL.forEach(function(c){ pool.push({key:'gm.fl.'+c[0], lv:c[1], ans:c[2], near:c[3]}); });
  else if(id==='str') GAME_STR.forEach(function(c){ pool.push({key:'gm.str.'+c[0], lv:c[1], ans:c[2], near:c[3]}); });
  else if(id==='speed') GAME_SPEED.forEach(function(c){ pool.push({key:'gm.sp.'+c[0], lv:c[1], ans:c[2]}); });
  else ({flip:GAME_FLIP, step:GAME_STEP, calm:GAME_CALM, opt:GAME_OPT, kind:GAME_KIND}[id] || GAME_REACT[age]).forEach(function(c){
    pool.push({key:({flip:'gm.flip.', step:'gm.step.', calm:'gm.calm.', opt:'gm.opt.', kind:'gm.kind.'}[id] || 'gm.react.'+age)+c[0], lv:c[1], multi:true, feel:c[2]});
  });
  return pool;
}
/* the next card: at the level the round has reached; among those, a card
   that was hard last time, then a new one, then the less sure ones; a card
   already seen today rests */
function gmPick(R){
  var st=gmState(), today=dayKey(), used={}, best=null, bs=-1e9;
  R.cards.forEach(function(c){ used[c.key]=1; });
  function score(c){ var m=st.mem[c.key]; if(!m) return 3; if(m[2]===today) return .2; if(!m[3]) return 4; return 1+(1-m[1]/m[0]); }
  gmShuffle(R.pool).forEach(function(c){
    if(used[c.key]) return;
    var sc=score(c)-Math.abs(c.lv-R.lv)*10;
    if(sc>bs){ bs=sc; best=c; }
  });
  if(!best) return null;
  var m=st.mem[best.key], k=best.key, card={key:k, lv:best.lv, ans:best.ans, near:best.near, feel:best.feel, back:!!(m && !m[3] && m[2]!==today)};
  if(best.multi){
    var ks=best.lv>=3 ? ['a','b','c','d'] : (['step','calm','opt','kind'].indexOf(R.id)>=0) ? ['a'].concat(gmShuffle(['b','c','d']).slice(0,2)) : ['a','b','c'];
    card.q=t(k+'.q'); card.best=t(k+'.a'); card.ans='a';
    card.opts=gmShuffle(ks.map(function(x){ return {t:t(k+'.'+x), k:x}; }));
  } else card.q=t(k);
  if(GM_WORDS[R.id]){
    /* the answer, the close ones once the level allows, and the rest at random */
    var n=best.lv>=3 ? 4 : 3, picks=[best.ans].concat(best.lv>=2 ? best.near.slice(0,n-1) : []);
    gmShuffle(GM_WORDS[R.id].keys()).forEach(function(k){ if(picks.length<n && picks.indexOf(k)<0 && best.near.indexOf(k)<0) picks.push(k); });
    card.fopts=gmShuffle(picks);
  }
  R.cards.push(card);
  return card;
}
/* remember how a card went, and move the round's level: up after two right
   in a row (three in the speed round), down a step after a miss */
function gmRecord(R,c,ok){
  var st=gmState(), m=st.mem[c.key]||[0,0,'',0], a=st.acc[R.id]||[0,0];
  st.mem[c.key]=[m[0]+1, m[1]+(ok?1:0), dayKey(), ok?1:0];
  st.acc[R.id]=[a[0]+1, a[1]+(ok?1:0)];
  R.n++;
  if(ok){ R.right++; R.pts+=R.id==='speed' ? (c.lv>=3?2:1) : (c.lv>=3?3:2); }
  var prev=R.lv;
  if(ok){ R.streak++; if(R.streak>=(R.id==='speed'?3:2) && R.lv<R.maxLv){ R.lv++; R.streak=0; } }
  else { R.streak=0; if(R.lv>1) R.lv--; }
  R.shift = R.lv>prev ? 'up' : R.lv<prev ? 'down' : null;
}
function gmStop(){ if(gmTick){ clearInterval(gmTick); gmTick=null; } }
function gmStart(id){
  gmStop();
  var pool=gmPool(id), maxLv=Math.max.apply(null,pool.map(function(c){ return c.lv; })), L=gmState().lvl[id]||0;
  gmRun={id:id, pool:pool, maxLv:maxLv, lv:Math.min(maxLv,Math.max(1,L)), streak:0, cards:[], i:0, n:0, right:0, pts:0, answered:null};
  renderGames();
  var b=document.getElementById('gmBox'); if(b) b.scrollIntoView({block:'start'});
}
function renderGameRow(){
  var b=document.getElementById('gameRow'); if(!b) return;
  var id=gmDaily(), g=GAME_IDS.filter(function(x){ return x.id===id; })[0], done=gmMine().daily===dayKey();
  b.hidden=false;
  b.className='home-game'+(done?' done':'');
  b.innerHTML='<span class="hg-ic">'+ic(g.icon)+'</span>'+
    '<span class="hg-t"><small>'+esc(t('gm.daily'))+'</small><b>'+esc(t('gm.'+id))+'</b>'+
      '<em>'+esc(done ? t('gm.daily.done') : t('gm.daily.xp'))+'</em></span>'+
    '<span class="hg-go">'+esc(t(done?'gm.again':'gm.play'))+'</span>';
  if(!b.dataset.bound){ b.dataset.bound='1'; b.addEventListener('click',function(){ gmPlayer={k:'me'}; goPage('games'); gmStart(gmDaily()); }); }
}
function gmFeel(k){ var f=pzF(k); return (f?f.e+' ':'')+esc(pzLabel(k)); }
function gmLvLabel(id){ var L=Math.max(1,gmState().lvl[id]||0); return '<span class="gm-lv l'+L+'">'+esc(t('gm.lv'+L))+'</span>'; }
function renderGames(){
  var box=document.getElementById('gmBox'); if(!box) return;
  var st=gmState(), daily=gmDaily();
  if(!gmRun){
    gmStop();
    var kp=gmKidP(); if(gmPlayer.k==='kid' && !kp) gmPlayer={k:'me'};
    var who='<div class="trk-who gm-who"><span class="trk-who-l">'+esc(t('gm.who'))+'</span>'+
      '<button type="button" class="trk-wb'+(gmPlayer.k==='me'?' on':'')+'" data-gwho="me">'+ic('user')+'<span>'+esc(t('gm.me'))+'</span></button>'+
      (S.kids||[]).map(function(k){ return '<button type="button" class="trk-wb kid'+(kp&&kp.id===k.id?' on':'')+'" data-gwho="'+k.id+'">⭐<span>'+esc(k.name)+'</span></button>'; }).join('')+
      '<button type="button" class="trk-wb add'+(gmKidForm?' on':'')+'" data-gwho="add">'+ic('plus')+'<span>'+esc(t('who.add'))+'</span></button>'+
      '<button type="button" class="trk-wb'+(gmPlayer.k==='guest'?' on':'')+'" data-gwho="guest">'+ic('users')+'<span>'+esc(t('gm.other'))+'</span></button></div>'+
      (gmKidForm ? kidAddForm() : kp ? kidAgeRow(kp) : '')+
      (gmPlayer.k==='guest' ? '<div class="t3seg gm-bands">'+['k','t','a'].map(function(b){
        return '<button type="button" data-gband="'+b+'" class="'+((gmPlayer.band||'a')===b?'on':'')+'">'+esc(t('gm.b.'+b))+'</button>'; }).join('')+'</div>'+
        '<p class="gm-forp">'+esc(t('gm.for.g'))+'</p>' : kp ? '<p class="gm-forp">'+esc(t('gm.for',{n:kp.name}))+'</p>' : '');
    box.innerHTML=who+'<div class="gm-list">'+GAME_IDS.map(function(g){
      var isD=g.id===daily, n=st.played[g.id]||0, isNew=!n && GAME_NEW.indexOf(g.id)>=0;
      return '<button type="button" class="gm-card'+(isD?' daily':'')+'" data-gm="'+g.id+'"><span class="gm-ic">'+ic(g.icon)+'</span>'+
        '<span class="gm-txt"><b>'+esc(t('gm.'+g.id))+(isNew ? ' <span class="gm-newb">'+esc(t('gm.new'))+'</span>' : n ? ' '+gmLvLabel(g.id) : '')+'</b>'+
        '<small>'+esc(t('gm.'+g.id+'.s'))+'</small>'+
        (isD ? '<em>'+esc(st.daily===dayKey() ? t('gm.daily.done') : t('gm.daily'))+'</em>' : '')+'</span>'+
        (n ? '<span class="gm-n numf">✓'+n+'</span>' : '')+'</button>'; }).join('')+'</div>'+feelDict();
    box.querySelectorAll('[data-gm]').forEach(function(b){ b.addEventListener('click',function(){ gmStart(b.dataset.gm); }); });
    kidBind(box, kp, function(k, added){ gmKidForm=false; if(added) gmPlayer={k:'kid', id:k.id}; renderGames(); });
    box.querySelectorAll('[data-gwho]').forEach(function(b){ b.addEventListener('click',function(){
      var w=b.dataset.gwho;
      if(w==='add'){ gmKidForm=!gmKidForm; renderGames(); var n=document.getElementById('kidName'); if(n) n.focus(); return; }
      gmKidForm=false;
      gmPlayer = w==='me' ? {k:'me'} : w==='guest' ? {k:'guest', band:gmPlayer.band||'a'} : {k:'kid', id:Number(w)};
      if(w==='guest') gmGuest=null; renderGames(); }); });
    box.querySelectorAll('[data-gband]').forEach(function(b){ b.addEventListener('click',function(){ gmPlayer.band=b.dataset.gband; gmGuest=null; renderGames(); }); });
    return;
  }
  var R=gmRun;
  if(R.id==='speed'){ gmSpeed(box); return; }
  if(R.i>=GAME_LEN || (R.i>=R.cards.length && !gmPick(R))){ gmFinish(box); return; }
  var c=R.cards[R.i];
  var dots='<div class="gm-dots">'+Array.apply(null,Array(GAME_LEN)).map(function(_,k){ return '<i class="'+(k<R.i?'on':k===R.i?'cur':'')+'"></i>'; }).join('')+'</div>';
  var W=GM_WORDS[R.id];
  var opts = W
    ? '<div class="gm-opts fl-opts">'+c.fopts.map(function(k){ var e=W.emo(k); return '<button type="button" class="gm-opt" data-ans="'+k+'">'+(e?'<span class="fl-e">'+e+'</span>':'')+'<span>'+esc(W.lab(k))+'</span></button>'; }).join('')+'</div>'
    : R.id==='circle'
    ? '<div class="gm-opts '+(c.lv>=3?'three':'two')+'"><button type="button" class="gm-opt" data-ans="in">'+ic('check')+'<span>'+esc(t('gm.in'))+'</span></button>'+
        (c.lv>=3 ? '<button type="button" class="gm-opt" data-ans="part">'+ic('compass')+'<span>'+esc(t('gm.part'))+'</span></button>' : '')+
        '<button type="button" class="gm-opt" data-ans="out">'+ic('seedling')+'<span>'+esc(t('gm.out'))+'</span></button></div>'
    : '<div class="gm-opts">'+c.opts.map(function(o){ return '<button type="button" class="gm-opt" data-ans="'+o.k+'">'+esc(o.t)+'</button>'; }).join('')+'</div>';
  var fb='';
  if(R.answered){
    var a=R.answered, good=a===c.ans, msg, show='';
    if(R.id==='str') msg=t(good ? 'gm.sv.ok' : (c.near||[]).indexOf(a)>=0 ? 'gm.sv.x' : 'gm.sv.x2',{p:t('vs.'+a), s:t('vs.'+c.ans)});
    else if(R.id==='feel') msg=good ? t('gm.fe.ok',{f:t('fe.'+c.ans), m:t('fe.'+c.ans+'.m')}) : t((c.near||[]).indexOf(a)>=0 ? 'gm.fe.x' : 'gm.fe.x2',{p:t('fe.'+a), f:t('fe.'+c.ans), m:t('fe.'+c.ans+'.m')});
    else if(R.id==='circle') msg=t(good ? 'gm.c.'+c.ans : 'gm.c.'+c.ans+'.x');
    else if(R.id==='flip') msg=t(good?'gm.f.ok':'gm.f.x');
    else msg=t(({step:'gm.s.', calm:'gm.k.', opt:'gm.o.', kind:'gm.y.'}[R.id]||'gm.r.')+a);
    if(!good && c.best) show=c.best;
    fb='<div class="gm-fb '+(good?'good':'soft')+'"><p>'+(good?'🎉 ':'💡 ')+esc(msg)+'</p>'+(show?'<p class="gm-best">'+esc(show)+'</p>':'')+
      '<button class="btn btn-primary btn-block" id="gmNext">'+esc(t('gm.next'))+'</button></div>';
  }
  var note='';
  if(!R.answered){
    if(R.shiftAt===R.i) note='<p class="gm-up'+(R.shiftDir==='down'?' down':'')+'">'+esc(t(R.shiftDir==='down'?'gm.down':'gm.up'))+'</p>';
    else if(c.back) note='<p class="gm-back">'+esc(t('gm.again.q'))+'</p>';
  }
  var forWho=gmKidP() ? '<p class="gm-forwho">'+esc(t('gm.playing',{n:gmKidP().name}))+'</p>' : gmPlayer.k==='guest' ? '<p class="gm-forwho">'+esc(t('gm.playing',{n:t('gm.b.'+(gmPlayer.band||'a'))}))+'</p>' : '';
  box.innerHTML='<div class="gm-play">'+forWho+'<div class="gm-head"><b>'+esc(t('gm.'+R.id))+' <span class="gm-lv l'+c.lv+'">'+esc(t('gm.lv'+c.lv))+'</span></b>'+dots+'</div>'+note+
    (c.feel ? '<p class="gm-feel">'+gmFeel(c.feel)+'</p>' : '')+
    '<p class="gm-q">'+esc(c.q)+'</p><p class="gm-ask">'+esc(t('gm.q.'+R.id))+'</p>'+opts+fb+
    '<button class="btn btn-quiet btn-sm gm-quit" id="gmQuit">'+esc(t('gm.done'))+'</button>'+(R.id==='feel'?feelDict():'')+'</div>';
  box.querySelectorAll('[data-ans]').forEach(function(b){
    if(R.answered){ b.disabled=true; if(b.dataset.ans===R.answered) b.classList.add('picked'); if(b.dataset.ans===c.ans) b.classList.add('best'); return; }
    b.addEventListener('click',function(){
      R.answered=b.dataset.ans;
      gmRecord(R,c,R.answered===c.ans);
      if(R.shift){ R.shiftAt=R.i+1; R.shiftDir=R.shift; }
      renderGames();
    });
  });
  var nx=box.querySelector('#gmNext'); if(nx) nx.addEventListener('click',function(){ R.i++; R.answered=null; renderGames(); });
  box.querySelector('#gmQuit').addEventListener('click',function(){ gmRun=null; renderGames(); });
}
/* the speed round: as many sentences as fit in 45 seconds, a tap each,
   a short flash of feedback and straight on */
function gmSpeed(box){
  var R=gmRun;
  var quit='<button class="btn btn-quiet btn-sm gm-quit" id="gmQuit">'+esc(t('gm.done'))+'</button>';
  function bindQuit(){ box.querySelector('#gmQuit').addEventListener('click',function(){ gmStop(); gmRun=null; renderGames(); }); }
  if(!R.started){
    box.innerHTML='<div class="gm-play"><div class="gm-head"><b>'+esc(t('gm.speed'))+'</b></div>'+
      '<div class="gm-sp-intro">'+ic('zap')+'<p>'+esc(t('gm.sp.go'))+'</p></div>'+
      '<button class="btn btn-primary btn-block" id="gmGo">'+esc(t('gm.sp.start'))+'</button>'+quit+'</div>';
    box.querySelector('#gmGo').addEventListener('click',function(){
      R.started=true; R.end=Date.now()+GAME_SECS*1000; renderGames();
      gmTick=setInterval(function(){
        if(gmRun!==R){ gmStop(); return; }
        var left=Math.max(0,(R.end-Date.now())/1000), el=document.getElementById('gmLeft'), bar=document.getElementById('gmBar');
        if(el) el.textContent=t('gm.sp.left',{n:Math.ceil(left)});
        if(bar) bar.style.width=(left/GAME_SECS*100)+'%';
        if(left<=0 && !R.flash) renderGames();
      },250);
    });
    bindQuit(); return;
  }
  var left=(R.end-Date.now())/1000;
  if(R.over || left<=0 || (R.i>=R.cards.length && !gmPick(R))){ R.over=true; gmStop(); gmFinish(box); return; }
  var c=R.cards[R.i], f=R.flash;
  box.innerHTML='<div class="gm-play gm-sp"><div class="gm-head"><b>'+esc(t('gm.speed'))+' <span class="gm-lv l'+c.lv+'">'+esc(t('gm.lv'+c.lv))+'</span></b>'+
      '<span class="gm-sp-score numf">✓ '+R.right+'</span><span class="gm-timer numf" id="gmLeft">'+esc(t('gm.sp.left',{n:Math.ceil(left)}))+'</span></div>'+
    '<div class="gm-tbar"><i id="gmBar" style="width:'+(left/GAME_SECS*100)+'%"></i></div>'+
    '<p class="gm-q">'+esc(c.q)+'</p><p class="gm-ask">'+esc(t('gm.q.speed'))+'</p>'+
    '<div class="gm-opts two"><button type="button" class="gm-opt" data-sp="c">'+ic('check')+'<span>'+esc(t('gm.sp.c'))+'</span></button>'+
      '<button type="button" class="gm-opt" data-sp="r">'+ic('refresh')+'<span>'+esc(t('gm.sp.r'))+'</span></button></div>'+
    (f ? '<p class="gm-flash '+(f.ok?'good':'soft')+'">'+esc(f.ok ? t('gm.sp.ok') : t('gm.sp.x',{c:t('gm.sp.'+c.ans)}))+'</p>' : '<p class="gm-flash"></p>')+
    quit+'</div>';
  box.querySelectorAll('[data-sp]').forEach(function(b){
    if(f){ b.disabled=true; if(b.dataset.sp===c.ans) b.classList.add('best'); else if(!f.ok) b.classList.add('picked'); return; }
    b.addEventListener('click',function(){
      var ok=b.dataset.sp===c.ans;
      gmRecord(R,c,ok); R.flash={ok:ok}; renderGames();
      setTimeout(function(){ if(gmRun!==R) return; R.flash=null; R.i++; renderGames(); }, ok?450:1300);
    });
  });
  bindQuit();
}
/* what the games have learned: the game that goes best, and the one worth
   more practice (after a few answers in each) */
function gmInsight(){
  var st=gmState(), rows=GAME_IDS.map(function(g){ var a=st.acc[g.id]; return a && a[0]>=4 ? {id:g.id, r:a[1]/a[0]} : null; }).filter(Boolean);
  if(!rows.length) return '';
  rows.sort(function(x,y){ return y.r-x.r; });
  var s=rows[0], g=rows[rows.length-1], txt;
  if(rows.length>1 && s.r-g.r>=.1) txt=t('gm.learn',{s:t('gm.'+s.id), g:t('gm.'+g.id)});
  else if(s.r>=.7) txt=t('gm.learn1',{s:t('gm.'+s.id)});
  else return '';
  return '<p class="gm-learn">'+ic('sparkles')+'<span>'+esc(txt)+'</span></p>';
}
function gmFinish(box){
  var R=gmRun, st=gmState(), today=dayKey(), total=R.n;
  if(!R.paid){
    R.paid=true;
    var before=levelInfo(), gain=10+R.pts, bonus=0;
    st.played[R.id]=(st.played[R.id]||0)+1; st.lastDay=today;
    /* a strong round: the next one starts harder; a hard one: a little easier */
    var L=st.lvl[R.id]||0, up, down;
    if(R.id==='speed'){ up=total>=8 && R.right/total>=.85; down=total>=4 && R.right/total<.5; }
    else { up=total>=GAME_LEN-1 && R.right>=total-1; down=R.right<=2; }
    if(up && L<3){ st.lvl[R.id]=L+1; R.harder=true; }
    else if(down && L>0) st.lvl[R.id]=L-1;
    R.mine=gmIsMe();
    if(R.mine){
      if(R.id===gmDaily() && st.daily!==today){ st.daily=today; bonus=15; }
      addPts(gain+bonus); markActiveToday();
    }
    save();
    R.gain=gain; R.bonus=bonus; R.before=before;
    celebrate(); renderGameRow(); renderPath();
  }
  var after=levelInfo(), hi=total>0 && R.right>=total-1;
  if(!R.mine){
    /* someone else's round: a cheer, no XP of mine */
    var kp=gmKidP();
    box.innerHTML='<div class="gm-end"><div class="pz-end"><div class="sc-heart">🎉</div><p class="ps-rmsg">'+esc(t('gm.end.o',{n:R.right, t:total}))+'</p>'+
      (kp ? '<p>'+esc(t('kid.cheer',{n:kp.name}))+'</p>' : '<p>'+esc(t(hi?'gm.end.hi':'gm.end.lo'))+'</p>')+
      (R.harder?'<p class="gm-harder">'+esc(t('gm.harder'))+'</p>':'')+'</div>'+
      '<div class="row-btns"><button class="btn btn-primary" id="gmAgain">'+ic('refresh')+'<span>'+esc(t('gm.again'))+'</span></button>'+
      '<button class="btn btn-ghost" id="gmBack">'+esc(t('gm.done'))+'</button></div></div>';
    box.querySelector('#gmAgain').addEventListener('click',function(){ gmStart(R.id); });
    box.querySelector('#gmBack').addEventListener('click',function(){ gmRun=null; renderGames(); });
    return;
  }
  box.innerHTML='<div class="gm-end"><div class="ps-reward"><div class="av-big t'+after.tier+'">'+avatarSvg(after.tier, avatarLabel(after))+'</div>'+
    '<div><p class="ps-rmsg">'+esc(t('gm.end',{n:R.right, t:total}))+'</p><p>'+esc(t(hi?'gm.end.hi':'gm.end.lo'))+'</p>'+
    '<p class="ps-rxp">'+esc(t('ps.rxp',{n:R.gain}))+'</p>'+(R.bonus?'<p class="ps-rxp">'+esc(t('gm.bonus',{n:R.bonus}))+'</p>':'')+
    (R.harder?'<p class="gm-harder">'+esc(t('gm.harder'))+'</p>':'')+
    '<div class="xp big"><i style="width:'+after.pct+'%"></i></div>'+
    '<p class="ps-rlvl">'+esc(after.level>R.before.level ? t('av.lvlup',{n:after.level}) : t('av.next',{n:after.need, l:after.level+1}))+'</p></div></div>'+
    gmInsight()+
    '<div class="row-btns"><button class="btn btn-primary" id="gmAgain">'+ic('refresh')+'<span>'+esc(t('gm.again'))+'</span></button>'+
    '<button class="btn btn-ghost" id="gmBack">'+esc(t('gm.done'))+'</button></div></div>';
  box.querySelector('#gmAgain').addEventListener('click',function(){ gmStart(R.id); });
  box.querySelector('#gmBack').addEventListener('click',function(){ gmRun=null; renderGames(); });
}

/* ================= a moment to pause, and how I feel =================
   Two daily moments of self-regulation. At the top of the day, "A moment
   to pause": three slow breaths - in through the nose, hold, and out very
   slowly through the mouth - before the day begins. After the tasks, "How do
   I feel right now?": name the feeling; a pleasant one is noticed and kept,
   a hard one gets a choice of response, with three breaths first if wanted.
   Every check-in is kept in the day's log, so My week shows what was felt
   and how the player chose. */
var PZ_FEELS=[{k:'joy',e:'😄',l:'fe.joy',pos:1},{k:'calm',e:'😌',l:'fe.calm',pos:1},{k:'pride',e:'🏆',l:'fe.pride',pos:1},
              {k:'excite',e:'🤩',l:'fe.excite',pos:1},{k:'grat',e:'🙏',l:'fe.grat',pos:1},
              {k:'tired',e:'😴',l:'pz.f.tired'},{k:'stress',e:'😰',l:'pz.f.stress'},{k:'angry',e:'😠',l:'pz.f.angry'},
              {k:'frust',e:'😤',l:'pz.f.frust'},{k:'worry',e:'😟',l:'fe.worry'},{k:'hurt',e:'😔',l:'pz.f.hurt'},
              {k:'sad',e:'😢',l:'pz.f.sad'},{k:'disap',e:'😞',l:'pz.f.disap'},{k:'fear',e:'😟',l:'pz.f.fear'}];
var PZ_SHOWN=['joy','calm','pride','excite','grat','tired','stress','angry','frust','worry','hurt','sad'];
function pzF(k){ return PZ_FEELS.filter(function(x){ return x.k===k; })[0]; }
function pzLabel(k){ var f=pzF(k); return f ? t(f.l) : k; }
/* kinds of breath, four rounds each: slow (4 in, 4 held, 7 out), the calming
   4-7-8, box breathing, and affectionate breathing with a hand on the heart
   (Neff and Germer), whose phases carry a gentle phrase */
var PZ_TYPES={slow:[['in',4],['hold',4],['out',7]], '478':[['in',4],['hold',7],['out',8]],
              box:[['in',4],['hold',4],['out',4],['hold2',4]], comp:[['cin',5],['cout',7]]};
var PZ_ROUNDS=4;
var PZ_PH=PZ_TYPES.slow;
function pzType(){ var k=(S.pref&&S.pref.breath)||'slow'; return PZ_TYPES[k] ? k : 'slow'; }
function pzPhLabel(ph){ return t(ph==='cin'?'pz.c.in':ph==='cout'?'pz.c.out':ph==='hold2'?'pz.hold':'pz.'+ph); }
function pzCircleCls(ph){ return ph==='cin'?'in':ph==='cout'?'out':ph; }
var pz=null, pzTimer=null;
function pzStop(){ if(pzTimer){ clearTimeout(pzTimer); pzTimer=null; } }
function pzOpen(mode){
  pzStop();
  pz = mode==='feel' ? {mode:'feel', step:'feel'} : mode==='sc' ? {mode:'sc', step:'sc0'} :
       ['intent','init','ahead'].indexOf(mode)>=0 ? {mode:mode, step:mode} : {mode:'day', step:'intro'};
  document.getElementById('pzTitle').querySelector('span').textContent=t({feel:'pz.ck.t', sc:'sc.t', intent:'in.t', init:'it.t', ahead:'ah.t'}[mode]||'pz.btn');
  pzRender(); document.getElementById('pauseModal').classList.add('on');
}
function pzClose(){ pzStop(); pz=null; document.getElementById('pauseModal').classList.remove('on'); renderPauseBtn(); renderPath(); }
function pzLog(){ if(!S.log || !S.log[dayKey()]) logDay(); var L=S.log[dayKey()]; if(!L.pauses) L.pauses=[]; if(!L.inits) L.inits=[]; return L; }
function pzWeekCount(){
  var log=S.log||{}, n=0;
  weekOf(0).forEach(function(d){ ((log[d]||{}).pauses||[]).forEach(function(z){ if(z.a) n++; }); });
  return n;
}
function renderPauseBtn(){
  var b=document.getElementById('pauseBtn'); if(!b) return;
  var L=(S.log||{})[dayKey()], done=!!(L && L.breath);
  b.classList.toggle('done',done);
  b.innerHTML='<span class="pz-ic">'+ic(done?'check':'wind')+'</span><span><b>'+esc(t('pz.btn'))+'</b><small>'+esc(t(done?'pz.d.done':'pz.d.s'))+'</small></span>'+ic('chevron');
}
function pzBreathHtml(){
  var ph=PZ_PH[pz.ph][0];
  return '<p class="pz-sub pz-how">'+esc(t(pzType()==='comp'?'br.comp.how':'pz.how'))+'</p>'+
    '<div class="pz-breath"><div class="pz-circle '+pzCircleCls(ph)+'" style="transition-duration:'+PZ_PH[pz.ph][1]+'s"></div><div class="pz-in"><b id="pzPhase">'+esc(pzPhLabel(ph))+'</b><span class="numf" id="pzSec">'+pz.sec+'</span></div></div>'+
    '<p class="pz-sub" id="pzN">'+esc(t('pz.n',{n:Math.min(PZ_ROUNDS,pz.br+1), t:PZ_ROUNDS}))+'</p>'+
    '<button class="btn btn-ghost btn-block" id="pzNext">'+esc(t('pz.next'))+'</button>';
}
function pzStartBreath(after){ PZ_PH=PZ_TYPES[pzType()]; pz.after=after; pz.step='breath'; pz.br=0; pz.ph=0; pz.sec=PZ_PH[0][1]; pzRender(); pzTick(); }
function pzRender(){
  var box=document.getElementById('pzBody'); if(!box||!pz) return;
  if(pz.step==='intro'){
    var cur=pzType();
    box.innerHTML='<p class="pz-big">'+esc(t('pz.d.1'))+'</p><p class="pz-sub">'+esc(t('pz.1.s'))+'</p>'+
      '<div class="mg-lab">'+esc(t('br.type'))+'</div><div class="pz-types">'+['slow','478','box','comp'].map(function(k){
        return '<button type="button" class="pz-type'+(k===cur?' on':'')+'" data-brt="'+k+'"><b>'+esc(t('br.'+k))+'</b><small>'+esc(t('br.'+k+'.s'))+'</small></button>'; }).join('')+'</div>'+
      '<button class="btn btn-primary btn-block" id="pzGo">'+ic('wind')+'<span>'+esc(t('pz.go'))+'</span></button>';
    box.querySelectorAll('[data-brt]').forEach(function(b){ b.addEventListener('click',function(){
      if(!S.pref) S.pref={}; S.pref.breath=b.dataset.brt; save(); pzRender(); }); });
    box.querySelector('#pzGo').addEventListener('click',function(){ pzStartBreath('dayend'); });
  } else if(pz.step==='intent'){
    var Li=pzLog();
    box.innerHTML=(P.vision ? '<p class="pz-felt">'+esc(t('in.vis',{v:P.vision}))+'</p>' : '')+
      '<p class="pz-big">'+esc(t('in.q'))+'</p>'+
      '<div class="mg-picks pz-chips">'+['patience','courage','calm','generous','persist','listen','joy','resp','curious'].map(function(k){
        return '<button type="button" class="t3idea t3chip'+(Li.intent===t('q.'+k)?' on':'')+'" data-inq="'+k+'"><span>'+esc(t('q.'+k))+'</span></button>'; }).join('')+'</div>'+
      '<div class="addrow pz-ownrow"><input type="text" id="pzOwn" maxlength="60" placeholder="'+esc(t('in.own'))+'">'+
      '<button class="btn btn-primary" id="pzOk">'+esc(t('in.ok'))+'</button></div>';
    var setI=function(x){ if(!x) return; var L=pzLog(), first=!L.intent; L.intent=x; if(first){ addPts(5); markActiveToday(); } save(); toast(t('in.saved',{x:x})); pzClose(); };
    box.querySelectorAll('[data-inq]').forEach(function(b){ b.addEventListener('click',function(){ setI(t('q.'+b.dataset.inq)); }); });
    var oi=box.querySelector('#pzOwn');
    box.querySelector('#pzOk').addEventListener('click',function(){ var v=oi.value.trim(); if(v) setI(v); else oi.focus(); });
    oi.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); setI(oi.value.trim()); } });
  } else if(pz.step==='init'){
    /* pick several ideas, put each in your own words, add your own; in the
       day the main action is to plan them into My day, in the evening to
       record what was already done */
    if(!pz.sel) pz.sel=[];
    var eve=new Date().getHours()>=17;
    var trows=trkTodayRows().filter(function(r){ return !r.done; });
    var picked=function(n){ return pz.sel.some(function(x){ return x.n===n; }); };
    /* in the day, no more than My day has room for; in the evening it is a record, so no limit */
    var room=eve ? 99 : Math.max(0, T3_MAX-today3().items.length), atMax=pz.sel.length>=room;
    box.innerHTML='<p class="pz-big">'+esc(t(eve?'it.q':'it.q.m'))+'</p><p class="pz-sub">'+esc(t('it.s'))+'</p>'+
      (trows.length ? '<p class="pz-sub pz-rt">'+esc(t('it.trk'))+'</p><div class="pz-acts">'+trows.map(function(r,i){
        return '<div class="it-row"><span>'+esc(r.row.t)+'</span><button type="button" class="btn btn-ghost btn-sm" data-ittrk="'+i+'">'+esc(t('it.did'))+'</button></div>'; }).join('')+'</div>' : '')+
      '<p class="pz-sub pz-rt">'+esc(t('it.pick'))+(eve ? '' : ' <b class="it-room">'+esc(room ? t('it.room',{n:room-pz.sel.length}) : t('it.full'))+'</b>')+'</p>'+
      '<div class="mg-picks pz-chips">'+[1,2,3,4,5,6,7,8].map(function(n){
        return '<button type="button" class="t3idea t3chip'+(picked(n)?' on':'')+'" data-itpick="'+n+'"'+(!picked(n)&&atMax?' disabled':'')+'>'+ic(picked(n)?'check':'plus')+'<span>'+esc(t('it.'+n))+'</span></button>'; }).join('')+'</div>'+
      '<div class="addrow pz-ownrow"><input type="text" id="pzOwn" maxlength="100" placeholder="'+esc(t('it.own'))+'"'+(atMax?' disabled':'')+'>'+
      '<button class="btn btn-ghost" id="pzAddOwn"'+(atMax?' disabled':'')+'>'+ic('plus')+'<span>'+esc(t('it.add'))+'</span></button></div>'+
      (pz.sel.length ? '<p class="pz-sub pz-rt">'+esc(t('it.words'))+'</p><div class="it-sel">'+pz.sel.map(function(x,i){
        return '<div class="it-selrow">'+ic('rocket')+'<input type="text" maxlength="100" data-itsel="'+i+'" value="'+esc(x.t)+'">'+
          '<button type="button" class="t3act" data-itdel="'+i+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></div>'; }).join('')+'</div>' : '')+
      (pz.sel.length ? '<div class="row-btns it-btns">'+
        '<button class="btn '+(eve?'btn-ghost':'btn-primary')+'" id="itPlan">'+esc(t('it.planN',{n:pz.sel.length}))+'</button>'+
        '<button class="btn '+(eve?'btn-primary':'btn-quiet')+'" id="itDid">'+esc(t('it.didN'))+'</button></div>' : '');
    var keepEdits=function(){ box.querySelectorAll('[data-itsel]').forEach(function(inp){ var x=pz.sel[+inp.dataset.itsel]; if(x) x.t=inp.value; }); };
    box.querySelectorAll('[data-itpick]').forEach(function(b){ b.addEventListener('click',function(){
      keepEdits(); var n=+b.dataset.itpick, ix=-1; pz.sel.forEach(function(x,i){ if(x.n===n) ix=i; });
      if(ix>=0) pz.sel.splice(ix,1); else if(!atMax) pz.sel.push({n:n, t:t('it.'+n)}); pzRender(); }); });
    var own=box.querySelector('#pzOwn');
    var addOwn=function(){ var v=own.value.trim(); if(atMax) return; if(!v){ own.focus(); return; } keepEdits(); pz.sel.push({n:0, t:v}); pzRender(); };
    box.querySelector('#pzAddOwn').addEventListener('click',addOwn);
    own.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); addOwn(); } });
    box.querySelectorAll('[data-itdel]').forEach(function(b){ b.addEventListener('click',function(){ keepEdits(); pz.sel.splice(+b.dataset.itdel,1); pzRender(); }); });
    box.querySelectorAll('[data-ittrk]').forEach(function(b){ b.addEventListener('click',function(){
      var r=trows[+b.dataset.ittrk]; trkTick(r.type, r.cfg, r.row, r.di); celebrate(); toast(t('it.done')); pzClose(); }); });
    var chosen=function(){ keepEdits(); return pz.sel.map(function(x){ return x.t.trim(); }).filter(Boolean); };
    var pb=box.querySelector('#itPlan');
    if(pb) pb.addEventListener('click',function(){
      var list=chosen(); if(!list.length) return; var td=today3();
      list.forEach(function(x){ if(addDayItem(x)){ var it=td.items.filter(function(y){ return normLine(y.t)===normLine(x); })[0]; if(it) it.init=true; } });
      logDay(); save(); toast(t('it.planned.n')); pzClose(); renderToday3();
    });
    var db=box.querySelector('#itDid');
    if(db) db.addEventListener('click',function(){
      var list=chosen(); if(!list.length) return; var L=pzLog();
      list.forEach(function(x){ L.inits.push({t:x, h:new Date().getHours()}); });
      addPts(15*list.length); markActiveToday(); save(); celebrate(); toast(t('it.done')); pzClose();
    });
  } else if(pz.step==='ahead'){
    var La=pzLog(), td3=today3(), mine=(La.inits||[]).map(function(x){ return x.t; }).concat(td3.items.filter(function(x){ return x.init&&x.done; }).map(function(x){ return x.t; }));
    var undone=td3.items.filter(function(x){ return !x.done; }), carry=S.carry||[];
    var obs=['tired','time','mood','dist','people'];
    box.innerHTML=(mine.length ? '<p class="pz-felt">'+esc(t('ah.good'))+' '+esc(mine.join(' · '))+'</p>' : '')+
      '<p class="pz-big">'+esc(t('ah.q1'))+'</p>'+
      '<div class="mg-picks pz-chips">'+obs.map(function(k){ return '<button type="button" class="t3idea t3chip" data-ob="'+k+'"><span>'+esc(t('ob.'+k))+'</span></button>'; }).join('')+'</div>'+
      '<input type="text" id="ahO" class="pz-in1" maxlength="60" placeholder="'+esc(t('ah.obs.ph'))+'">'+
      '<p class="pz-big pz-q2">'+esc(t('ah.q2'))+'</p>'+
      '<input type="text" id="ahT" class="pz-in1" maxlength="80" placeholder="'+esc(t('ah.then.ph'))+'">'+
      (undone.length ? '<p class="pz-sub pz-rt">'+esc(t('ah.retry'))+'</p><div class="pz-acts">'+undone.map(function(x){
        var c=carry.indexOf(x.t)>=0;
        return '<div class="it-row"><span>'+esc(x.t)+'</span><button type="button" class="btn btn-ghost btn-sm" data-carry="'+esc(x.t)+'"'+(c?' disabled':'')+'>'+esc(c?t('ah.retry.ok'):t('ah.retry.btn'))+'</button></div>'; }).join('')+'</div>' : '')+
      '<button class="btn btn-primary btn-block" id="ahSave">'+esc(t('ah.save'))+'</button>';
    box.querySelectorAll('[data-ob]').forEach(function(b){ b.addEventListener('click',function(){
      box.querySelectorAll('[data-ob]').forEach(function(x){ x.classList.toggle('on',x===b); });
      box.querySelector('#ahO').value=t('ob.'+b.dataset.ob); var tt=box.querySelector('#ahT'); if(!tt.value) tt.value=t('th.'+b.dataset.ob); }); });
    box.querySelectorAll('[data-carry]').forEach(function(b){ b.addEventListener('click',function(){
      if(!S.carry) S.carry=[]; if(S.carry.indexOf(b.dataset.carry)<0) S.carry.push(b.dataset.carry); save(); b.disabled=true; b.textContent=t('ah.retry.ok'); }); });
    box.querySelector('#ahSave').addEventListener('click',function(){
      var o=box.querySelector('#ahO').value.trim(), th=box.querySelector('#ahT').value.trim();
      if(!o && !th){ box.querySelector('#ahO').focus(); return; }
      var L=pzLog(), first=!L.ahead; L.ahead={o:o, t:th}; if(first){ addPts(10); markActiveToday(); } save(); toast(t('ah.saved')); pzClose();
    });
  } else if(/^sc[0-3]$/.test(pz.step)){
    var n=+pz.step.slice(2);
    box.innerHTML='<div class="sc-step"><div class="pz-dots">'+[0,1,2,3].map(function(k){ return '<i class="'+(k<n?'on':k===n?'cur':'')+'"></i>'; }).join('')+'</div>'+
      (n===0 ? '<div class="sc-heart">💛</div><p class="pz-big">'+esc(t('sc.0'))+'</p>'
             : '<p class="sc-say">'+esc(t('sc.'+n))+'</p><p class="pz-sub">'+esc(t('sc.'+n+'.s'))+'</p>')+'</div>'+
      '<button class="btn btn-primary btn-block" id="scNext">'+esc(t(n===0?'sc.go':'sc.next'))+'</button>';
    box.querySelector('#scNext').addEventListener('click',function(){
      if(n<3){ pz.step='sc'+(n+1); pzRender(); return; }
      var L=pzLog(); L.sc=(L.sc||0)+1; if(L.sc===1) addPts(5); markActiveToday(); save(); pz.step='scend'; pzRender();
    });
  } else if(pz.step==='scend'){
    box.innerHTML='<div class="pz-end"><div class="sc-heart">💛</div><p class="pz-big">'+esc(t('sc.end'))+'</p></div>'+
      '<div class="row-btns"><button class="btn btn-primary" id="pzEnd">'+esc(t('pz.close'))+'</button></div>';
    box.querySelector('#pzEnd').addEventListener('click',pzClose);
  } else if(pz.step==='breath'){
    box.innerHTML=pzBreathHtml();
    box.querySelector('#pzNext').addEventListener('click',function(){ pzStop(); pzAfterBreath(); });
  } else if(pz.step==='dayend'){
    box.innerHTML='<div class="pz-end"><div class="pz-endic">'+ic('check')+'</div><p class="pz-big">'+esc(t('pz.d.end'))+'</p>'+
      (pz.paid ? '<p class="ps-rxp">'+esc(t('ps.rxp',{n:5}))+'</p>' : '')+'</div>'+
      '<div class="row-btns"><button class="btn btn-primary" id="pzEnd">'+esc(t('pz.close'))+'</button></div>';
    box.querySelector('#pzEnd').addEventListener('click',pzClose);
  } else if(pz.step==='feel'){
    box.innerHTML='<p class="pz-sub">'+esc(t('pz.2.s'))+'</p>'+
      '<div class="pz-feels">'+PZ_SHOWN.map(function(k){ var f=pzF(k);
        return '<button type="button" class="pz-feel'+(f.pos?' pos':'')+'" data-pzf="'+k+'"><span>'+f.e+'</span>'+esc(t(f.l))+'</button>'; }).join('')+'</div>';
    box.querySelectorAll('[data-pzf]').forEach(function(b){ b.addEventListener('click',function(){
      pz.f=b.dataset.pzf; pz.step=pzF(pz.f).pos ? 'pos' : 'choose'; pzRender(); }); });
  } else if(pz.step==='pos'){
    var fp=pzF(pz.f);
    box.innerHTML='<p class="pz-felt">'+fp.e+' '+esc(t(fp.l))+'</p><p class="pz-big">'+esc(t('pz.pos'))+'</p>'+
      '<div class="addrow pz-ownrow"><input type="text" id="pzOwn" maxlength="120" placeholder="'+esc(t('pz.pos.ph'))+'">'+
      '<button class="btn btn-primary" id="pzOk">'+esc(t('pz.pos.ok'))+'</button></div>';
    var keep=function(){ var L=pzLog(); L.pauses.push({f:pz.f, note:box.querySelector('#pzOwn').value.trim(), h:new Date().getHours()});
      addPts(5); markActiveToday(); save(); toast(t('pz.pos.done')); pzClose(); };
    box.querySelector('#pzOk').addEventListener('click',keep);
    box.querySelector('#pzOwn').addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); keep(); } });
  } else if(pz.step==='choose'){
    var f=pzF(pz.f);
    box.innerHTML='<p class="pz-felt">'+f.e+' '+esc(t(f.l))+'</p>'+
      (pz.breathed ? '' : '<button class="btn btn-ghost btn-sm pz-first" id="pzFirst">'+ic('wind')+'<span>'+esc(t('pz.first'))+'</span></button>')+
      '<p class="pz-big">'+esc(t('pz.3'))+'</p><p class="pz-sub">'+esc(t('pz.3.s'))+'</p>'+
      '<div class="pz-acts">'+[1,2,3,4,5].map(function(n){
        return '<button type="button" class="pz-act" data-pza="'+n+'">'+esc(t('pz.a'+n))+'</button>'; }).join('')+'</div>'+
      '<div class="addrow pz-ownrow"><input type="text" id="pzOwn" maxlength="120" placeholder="'+esc(t('pz.own'))+'">'+
      '<button class="btn btn-primary" id="pzOk">'+esc(t('pz.ok'))+'</button></div>';
    var fb=box.querySelector('#pzFirst'); if(fb) fb.addEventListener('click',function(){ pzStartBreath('choose'); });
    function choose(txt){
      if(!txt) return;
      var L=pzLog(); L.pauses.push({f:pz.f, a:txt, h:new Date().getHours()});
      pz.a=txt; pz.step='end'; addPts(10); markActiveToday(); save(); celebrate(); pzRender();
    }
    box.querySelectorAll('[data-pza]').forEach(function(b){ b.addEventListener('click',function(){ choose(t('pz.a'+b.dataset.pza)); }); });
    var own=box.querySelector('#pzOwn');
    box.querySelector('#pzOk').addEventListener('click',function(){ var v=own.value.trim(); if(v) choose(v); else own.focus(); });
    own.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); var v=own.value.trim(); if(v) choose(v); } });
  } else {
    var n=pzWeekCount();
    box.innerHTML='<div class="pz-end"><div class="pz-endic">'+ic('check')+'</div>'+
      '<p class="pz-big">'+esc(t('pz.done'))+'</p><p class="pz-chosen">„'+esc(pz.a)+'”</p>'+
      '<p class="ps-rxp">'+esc(t('ps.rxp',{n:10}))+'</p>'+
      '<p class="pz-sub">'+esc(n>1 ? t('pz.week',{n:n}) : t('pz.week1'))+'</p></div>'+
      '<div class="row-btns">'+(pz.addedDay ? '' : '<button class="btn btn-ghost" id="pzAdd">'+ic('plus')+'<span>'+esc(t('pz.add'))+'</span></button>')+
      '<button class="btn btn-primary" id="pzEnd">'+esc(t('pz.close'))+'</button></div>';
    var ad=box.querySelector('#pzAdd');
    if(ad) ad.addEventListener('click',function(){
      if(addDayItem(pz.a)){ markActiveToday(); save(); }
      pz.addedDay=true; toast(t('pz.added')); pzRender(); renderToday3();
    });
    box.querySelector('#pzEnd').addEventListener('click',function(){ pzClose(); renderDash(); });
  }
}
function pzAfterBreath(){
  if(pz.after==='dayend'){
    var L=pzLog();
    if(!L.breath){ L.breath=true; addPts(5); markActiveToday(); pz.paid=true; }
    save(); pz.step='dayend';
  } else { pz.breathed=true; pz.step='choose'; }
  pzRender();
}
/* one second at a time, so the count inside the circle runs down */
function pzTick(){
  pzStop();
  pzTimer=setTimeout(function(){
    if(!pz || pz.step!=='breath') return;
    pz.sec--;
    if(pz.sec<=0){
      pz.ph++;
      if(pz.ph>=PZ_PH.length){ pz.ph=0; pz.br++; }
      if(pz.br>=PZ_ROUNDS){ pzAfterBreath(); return; }
      pz.sec=PZ_PH[pz.ph][1];
      var ph=PZ_PH[pz.ph][0], c=document.querySelector('.pz-circle'), el=document.getElementById('pzPhase'), nn=document.getElementById('pzN');
      if(c){ c.style.transitionDuration=PZ_PH[pz.ph][1]+'s'; c.className='pz-circle '+pzCircleCls(ph); }
      if(el) el.textContent=pzPhLabel(ph);
      if(nn) nn.textContent=t('pz.n',{n:Math.min(PZ_ROUNDS,pz.br+1), t:PZ_ROUNDS});
    }
    var sc=document.getElementById('pzSec'); if(sc) sc.textContent=pz.sec;
    pzTick();
  },1000);
}
document.getElementById('pauseBtn').addEventListener('click',function(){ pzOpen('day'); });
document.getElementById('feelBtn').addEventListener('click',function(){ pzOpen('feel'); });
document.getElementById('pzX').addEventListener('click',pzClose);
document.getElementById('pauseModal').addEventListener('click',function(e){ if(e.target.id==='pauseModal') pzClose(); });

/* ================= a tool for you, and what I have learned =================
   The app reads what the player already did - pauses and their feelings,
   evening feelings, how much of the list gets done, goals left without a
   step, the games, the check-in - and offers one tool a day, saying why.
   "Not now" is remembered: a tool turned down three times is not offered
   again. Nothing leaves the device. */
function tlDays(n){ var out=[], d=new Date(); for(var i=0;i<n;i++){ out.push(dayKey(d)); d.setDate(d.getDate()-1); } return out; }
function tlState(){ if(!S.tools) S.tools={dis:{}, used:{}}; if(!S.tools.dis) S.tools.dis={}; if(!S.tools.used) S.tools.used={}; return S.tools; }
var DIM_GAME={choice:'react', init:'step', goal:'step', time:'speed', solve:'flip', plan:'step'};
function gmName(id){ return t('gm.'+id); }
function tlCandidates(){
  var log=S.log||{}, wk=tlDays(7), out=[], st=gmMine();
  var active=wk.filter(function(d){ return log[d]; }).length;
  function go(id){ return function(){ gmPlayer={k:'me'}; goPage('games'); gmStart(id); }; }
  /* pauses with a hard feeling */
  var pz=0, pf={};
  wk.forEach(function(d){ ((log[d]||{}).pauses||[]).forEach(function(z){ pz++; pf[z.f]=(pf[z.f]||0)+1; }); });
  var topf=Object.keys(pf).sort(function(a,b){ return pf[b]-pf[a]; })[0];
  if(pz>=2 && ['angry','stress','frust','hurt','fear'].indexOf(topf)>=0)
    out.push({id:'calm', s:9, t:t('tl.calm.t'), w:t('tl.calm.w',{n:pz, f:pzLabel(topf)}), icon:'wind', act:go('calm')});
  /* a long list, little of it done */
  var tot=0, done=0, days=0;
  wk.slice(1).forEach(function(d){ var L=log[d]; if(!L||!L.items.length) return; days++; tot+=L.items.length; L.items.forEach(function(x){ if(x.done) done++; }); });
  if(days>=3 && tot>=6 && done/tot<.5)
    out.push({id:'less', s:8, t:t('tl.less.t'), w:t('tl.less.w'), icon:'check', act:function(){ goPage('home'); toast(t('tl.less.ok')); var b=document.getElementById('todayBox'); if(b) b.scrollIntoView({block:'start'}); }});
  /* a goal with no step for four days or more */
  var today=dayKey();
  liveGoals().some(function(g){
    if(!g.startedAt || daysBetween(g.startedAt,today)<4) return false;
    var last=null;
    Object.keys(log).sort().forEach(function(d){ if((log[d].steps||[]).indexOf(g.id)>=0 || (log[d].rest||[]).indexOf(g.id)>=0) last=d; });
    var n=daysBetween(last||g.startedAt, today);
    if(n<4 || g.doneDay===today) return false;
    out.push({id:'stuck', s:8.5, t:t('tl.stuck.t',{g:g.title}), w:t('tl.stuck.w',{n:n}), icon:'target', act:function(){
      var td=today3(); if(td.picked.indexOf(g.id)<0) td.picked.push(g.id); save(); goPage('home'); toast(t('tl.stuck.ok'));
      var b=document.getElementById('todayBox'); if(b) b.scrollIntoView({block:'start'}); }});
    return true;
  });
  /* tired evenings */
  var tired=wk.slice(0,5).filter(function(d){ return (log[d]||{}).feel==='tired'; }).length;
  if(tired>=2) out.push({id:'tired', s:7.5, t:t('tl.tired.t'), w:t('tl.tired.w'), icon:'wind', act:function(){ pzOpen('day'); }});
  /* feelings that get mixed up */
  var fa=st.acc.feel;
  if(fa && fa[0]>=5 && fa[1]/fa[0]<.7) out.push({id:'dict', s:6, t:t('tl.dict.t'), w:t('tl.dict.w'), icon:'book', act:function(){
    goPage('games'); var d=document.querySelector('#gmBox .fl-dict'); if(d){ d.open=true; d.scrollIntoView({block:'start'}); } }});
  /* the game with the most room to grow, and the one ready for more */
  var rows=GAME_IDS.map(function(g){ var a=st.acc[g.id]; return a && a[0]>=6 ? {id:g.id, r:a[1]/a[0]} : null; }).filter(Boolean)
                   .sort(function(x,y){ return x.r-y.r; });
  if(rows.length && rows[0].r<.6) out.push({id:'game_'+rows[0].id, s:5.5, t:t('tl.game.t',{g:gmName(rows[0].id)}), w:t('tl.game.w'), icon:'star', act:go(rows[0].id)});
  var top=rows[rows.length-1];
  if(top && top.r>=.9 && (st.lvl[top.id]||0)<3) out.push({id:'up_'+top.id, s:5, t:t('tl.up.t',{g:gmName(top.id)}), w:t('tl.up.w'), icon:'trending',
    act:function(){ st.lvl[top.id]=Math.min(3,(st.lvl[top.id]||0)+1); save(); gmPlayer={k:'me'}; goPage('games'); gmStart(top.id); }});
  /* hard, hurting feelings this week: a self-compassion break */
  var hurtF=null; wk.forEach(function(d){ ((log[d]||{}).pauses||[]).forEach(function(z){ if(['hurt','sad','disap','shame','lonely'].indexOf(z.f)>=0) hurtF=z.f; }); });
  if(hurtF) out.push({id:'sc', s:7, t:t('tl.sc.t'), w:t('tl.sc.w',{f:pzLabel(hurtF)}), icon:'face', act:function(){ pzOpen('sc'); }});
  /* no gratitude written in the last three days, in the evening */
  var gr=S.grat||{}, recent=tlDays(3).some(function(d){ return gr[d]; });
  if(!recent && new Date().getHours()>=17 && active>=1) out.push({id:'grat', s:6.5, t:t('tl.grat.t'), w:t('tl.grat.w'), icon:'book', act:function(){ goPage('well'); }});
  /* the pause, never tried */
  var anyPause=Object.keys(log).some(function(d){ return (log[d].pauses||[]).length || log[d].breath; });
  if(!anyPause && active>=2) out.push({id:'pause', s:4.5, t:t('tl.pause.t'), w:t('tl.pause.w'), icon:'wind', act:function(){ pzOpen('day'); }});
  /* the check-in's area to grow */
  if(hasProfile()){
    var d=weakDim(), gid=DIM_GAME[d]||'react';
    out.push({id:'dim', s:3, t:t('tl.dim.t',{d:t('dim.'+d)}), w:t('tl.dim.w',{d:t('dim.'+d), g:gmName(gid)}), icon:'gauge', act:go(gid)});
  }
  /* a new game not played yet */
  var fresh=GAME_NEW.filter(function(id){ return !st.played[id]; })[0];
  if(fresh) out.push({id:'new_'+fresh, s:2, t:t('tl.new.t',{g:gmName(fresh)}), w:t('tl.new.w'), icon:'sparkles', act:go(fresh)});
  return out;
}
/* one tool a day: the strongest reason, less each time it was turned down */
function tlToday(){
  var ts=tlState(), today=dayKey();
  if(ts.hid===today) return null;
  var c=tlCandidates().filter(function(x){ return (ts.dis[x.id]||0)<3; });
  c.forEach(function(x){ x.r=x.s-2*(ts.dis[x.id]||0)-((ts.used[x.id]||{}).day===today ? 20 : 0); });
  c.sort(function(a,b){ return b.r-a.r; });
  var best=c.filter(function(x){ return x.r>0; })[0]||null;
  /* the day's tool stays the same, unless a clearly stronger reason has appeared since */
  if(ts.pick && ts.pick.day===today){ var keep=c.filter(function(x){ return x.id===ts.pick.id; })[0]; if(keep && !(best && best.r>keep.r+1)) return keep; }
  ts.pick=best ? {day:today, id:best.id} : null;
  return best;
}
function renderTool(){
  var box=document.getElementById('toolBox'); if(!box) return;
  var x=tlToday();
  if(!x){ box.hidden=true; box.innerHTML=''; return; }
  box.hidden=false;
  box.innerHTML='<div class="tl-head">'+ic('sparkles')+'<span>'+esc(t('tl.t'))+'</span></div>'+
    '<div class="tl-main"><span class="tl-ic">'+ic(x.icon)+'</span><b>'+esc(x.t)+'</b></div>'+
    '<p class="tl-why"><span>'+esc(t('tl.why'))+'</span> '+esc(x.w)+'</p>'+
    '<div class="row-btns"><button class="btn btn-primary btn-sm" id="tlTry">'+esc(t('tl.try'))+'</button>'+
    '<button class="btn btn-quiet btn-sm" id="tlNot">'+esc(t('tl.not'))+'</button></div>';
  box.querySelector('#tlTry').addEventListener('click',function(){
    var ts=tlState(); ts.used[x.id]={day:dayKey(), n:((ts.used[x.id]||{}).n||0)+1}; ts.hid=dayKey(); save();
    box.hidden=true; x.act();
  });
  box.querySelector('#tlNot').addEventListener('click',function(){
    var ts=tlState(); ts.dis[x.id]=(ts.dis[x.id]||0)+1; ts.hid=dayKey(); save(); box.hidden=true;
  });
}
function renderLearned(){
  var box=document.getElementById('learnBox'); if(!box) return;
  var log=S.log||{}, two=tlDays(14), lines=[], st=gmMine();
  var h=S.hours||{}, ht=(h.m||0)+(h.n||0)+(h.e||0);
  if(ht>=8){ var w=['m','n','e'].sort(function(a,b){ return (h[b]||0)-(h[a]||0); })[0]; lines.push(['clock', t('ln.time',{w:t('ln.time.'+w)})]); }
  var tot=0, done=0; two.forEach(function(d){ ((log[d]||{}).items||[]).forEach(function(x){ tot++; if(x.done) done++; }); });
  /* the share only when it is encouraging; otherwise the things done, which always are */
  if(tot>=6 && done/tot>=.4) lines.push(['check', t('ln.done',{p:Math.round(done/tot*100)})]);
  else if(done>=2) lines.push(['check', t('ln.done.n',{n:done})]);
  var pf={}; Object.keys(log).forEach(function(d){ (log[d].pauses||[]).forEach(function(z){ pf[z.f]=(pf[z.f]||0)+1; }); });
  var topf=Object.keys(pf).sort(function(a,b){ return pf[b]-pf[a]; })[0];
  if(topf && pf[topf]>=2){ var fe=pzF(topf); lines.push(['wind', t('ln.feel',{f:(fe?fe.e+' ':'')+pzLabel(topf)})]); }
  var rows=GAME_IDS.map(function(g){ var a=st.acc[g.id]; return a && a[0]>=6 ? {id:g.id, r:a[1]/a[0]} : null; }).filter(Boolean).sort(function(x,y){ return y.r-x.r; });
  if(rows.length) lines.push(['star', t('ln.game',{g:gmName(rows[0].id)})]);
  var ini=two.reduce(function(n,d){ return n+initCount(log[d],d); },0); if(ini>=2) lines.unshift(['rocket', t('ln.init',{n:ini})]);
  if(hasProfile()) lines.push(['gauge', t('ln.dim',{d:t('dim.'+strongDim())})]);
  var act=two.filter(function(d){ return log[d]; }).length;
  if(act>=3) lines.push(['calendar', t('ln.days',{n:act})]);
  box.innerHTML='<h3 class="boxh">'+ic('sparkles')+'<span>'+esc(t('ln.t'))+'</span></h3><p class="psub">'+esc(t('ln.s'))+'</p>'+
    (lines.length ? '<ul class="ln-list">'+lines.slice(0,5).map(function(l){ return '<li>'+ic(l[0])+'<span>'+esc(l[1])+'</span></li>'; }).join('')+'</ul>'
                  : '<p class="hint">'+esc(t('ln.none'))+'</p>');
}

/* ================= positive psychology =================
   A gratitude journal (three good things and why they happened), a
   self-compassion break, a strength to use in a new way this week, and a
   kind act a day. */
var VS_KEYS=['curious','brave','kind','humor','persist','create','grat','fair','hope','learn','lead','self'];
var KD_N=10, wlKd=null, wlStrPick=false;
function renderWell(){
  var box=document.getElementById('wellBox'); if(!box) return;
  if(!S.grat) S.grat={};
  var today=dayKey(), g=S.grat[today]||[], days=Object.keys(S.grat).filter(function(d){ return d!==today && S.grat[d].length; }).sort().reverse();
  var rows=[0,1,2].map(function(i){ var x=g[i]||{};
    return '<div class="gr-row"><span class="gr-n numf">'+(i+1)+'</span><div class="gr-in">'+
      '<input type="text" maxlength="140" data-gr="'+i+'" value="'+esc(x.t||'')+'" placeholder="'+esc(t('gr.ph'))+'">'+
      '<input type="text" class="gr-why" maxlength="140" data-grw="'+i+'" value="'+esc(x.w||'')+'" placeholder="'+esc(t('gr.why'))+'"></div></div>'; }).join('');
  var hist=days.length ? '<details class="gr-hist"><summary>'+ic('book')+'<span>'+esc(t('gr.hist',{n:days.length}))+'</span></summary>'+
    days.slice(0,30).map(function(d){ return '<div class="gr-day"><b>'+esc(fmtDay(d))+'</b><ul>'+S.grat[d].map(function(x){
      return '<li>'+esc(x.t)+(x.w?' <small>· '+esc(x.w)+'</small>':'')+'</li>'; }).join('')+'</ul></div>'; }).join('')+'</details>' : '';
  /* strength of the week */
  var wk=weekKey(), sw=(S.well&&S.well.str&&S.well.str.week===wk) ? S.well.str.k : null;
  var str = (sw && !wlStrPick)
    ? '<p class="wl-pick">'+esc(t('st.week',{s:t('vs.'+sw)}))+'</p><p class="wl-idea"><b>'+esc(t('st.idea'))+'</b> '+esc(t('vs.'+sw+'.i'))+'</p>'+
      '<div class="row-btns"><button class="btn btn-ghost btn-sm" data-wladd="'+esc(t('vs.'+sw+'.i'))+'">'+ic('plus')+'<span>'+esc(t('wl.add'))+'</span></button>'+
      '<button class="btn btn-quiet btn-sm" id="stChange">'+esc(t('st.change'))+'</button></div>'
    : '<div class="mg-picks">'+VS_KEYS.map(function(k){ return '<button type="button" class="t3idea t3chip" data-vs="'+k+'"><span>'+esc(t('vs.'+k))+'</span></button>'; }).join('')+'</div>';
  if(wlKd===null){ var n=Math.floor((new Date()-new Date(new Date().getFullYear(),0,0))/864e5); wlKd=n%KD_N+1; }
  box.innerHTML=
    '<section class="dash-box wl-card"><h3 class="boxh">'+ic('book')+'<span>'+esc(t('gr.t'))+'</span></h3><p class="psub">'+esc(t('gr.s'))+'</p>'+
      rows+'<div class="row-btns"><button class="btn btn-primary btn-sm" id="grSave">'+esc(t('gr.save'))+'</button>'+
      (g.length?'<span class="wl-done">'+esc(t('gr.done'))+'</span>':'')+'</div>'+hist+'</section>'+
    '<section class="dash-box wl-card"><h3 class="boxh">💛<span>'+esc(t('sc.t'))+'</span></h3><p class="psub">'+esc(t('sc.s'))+'</p>'+
      '<button class="btn btn-primary btn-sm" id="scOpen">'+esc(t('sc.go'))+'</button></section>'+
    '<section class="dash-box wl-card"><h3 class="boxh">'+ic('gem')+'<span>'+esc(t('st.t'))+'</span></h3><p class="psub">'+esc(t('st.s'))+'</p>'+str+'</section>'+
    '<section class="dash-box wl-card"><h3 class="boxh">'+ic('gift')+'<span>'+esc(t('kd.t'))+'</span></h3><p class="psub">'+esc(t('kd.s'))+'</p>'+
      '<p class="wl-pick">'+esc(t('kd.'+wlKd))+'</p><div class="row-btns">'+
      '<button class="btn btn-ghost btn-sm" data-wladd="'+esc(t('kd.'+wlKd))+'">'+ic('plus')+'<span>'+esc(t('wl.add'))+'</span></button>'+
      '<button class="btn btn-quiet btn-sm" id="kdMore">'+esc(t('kd.more'))+'</button></div></section>'+
    '<section class="dash-box wl-card"><h3 class="boxh">'+ic('star')+'<span>'+esc(t('wl.games'))+'</span></h3><div class="gm-list">'+
      ['opt','kind','str'].map(function(id){ var g=GAME_IDS.filter(function(x){ return x.id===id; })[0];
        return '<button type="button" class="gm-card" data-wlgame="'+id+'"><span class="gm-ic">'+ic(g.icon)+'</span><span class="gm-txt"><b>'+esc(t('gm.'+id))+'</b><small>'+esc(t('gm.'+id+'.s'))+'</small></span></button>'; }).join('')+
    '</div></section>';
  box.querySelector('#grSave').addEventListener('click',function(){
    var list=[0,1,2].map(function(i){ return {t:box.querySelector('[data-gr="'+i+'"]').value.trim(), w:box.querySelector('[data-grw="'+i+'"]').value.trim()}; })
                    .filter(function(x){ return x.t; });
    if(!list.length){ box.querySelector('[data-gr="0"]').focus(); return; }
    var first=!(S.grat[today]||[]).length;
    S.grat[today]=list; if(first){ addPts(10); markActiveToday(); }
    save(); toast(t('gr.saved')); if(first) celebrate(); renderWell();
  });
  box.querySelector('#scOpen').addEventListener('click',function(){ pzOpen('sc'); });
  box.querySelectorAll('[data-vs]').forEach(function(b){ b.addEventListener('click',function(){
    if(!S.well) S.well={}; S.well.str={week:wk, k:b.dataset.vs}; wlStrPick=false; save(); renderWell(); }); });
  var sc=box.querySelector('#stChange'); if(sc) sc.addEventListener('click',function(){ wlStrPick=true; renderWell(); });
  box.querySelector('#kdMore').addEventListener('click',function(){ wlKd=wlKd%KD_N+1; renderWell(); });
  box.querySelectorAll('[data-wlgame]').forEach(function(b){ b.addEventListener('click',function(){ gmPlayer={k:'me'}; goPage('games'); gmStart(b.dataset.wlgame); }); });
  box.querySelectorAll('[data-wladd]').forEach(function(b){ b.addEventListener('click',function(){
    if(addDayItem(b.dataset.wladd)){ markActiveToday(); save(); toast(t('pz.added')); } }); });
}

/* ================= the daily path =================
   Four small steps a day, in the order of the home page: pause, do, feel,
   play. Each one is ticked as it happens; all four make a full day - a
   bonus, a celebration, and a streak of full days. A tap on a step takes
   you straight to it. */
/* The path is proactivity itself: pause (the space before responding),
   choose (an intention, tied to who I want to be), initiate (one thing on my
   own initiative), and look ahead (what might get in the way tomorrow, and
   an if-then plan). Feeling and playing stay as tools and a bonus. */
var PATH_STEPS=[{k:'pause',icon:'wind'},{k:'choose',icon:'compass'},{k:'init',icon:'rocket'},{k:'ahead',icon:'flag'}];
/* rows ticked in the tracking tables on a given day: the habits one chose
   to track are initiative too */
function trkTicksOn(d){
  var n=0, st=S.trk; if(!st || !st.list) return 0;
  st.list.forEach(function(r){
    var m=/^(week|month|c30):(\d{4}-\d{2}-\d{2})$/.exec(r.key||''); if(!m) return;
    var i=daysBetween(m[2], d); if(i<0) return;
    Object.keys(r.ticks||{}).forEach(function(k){ if(r.ticks[k][i]) n++; });
  });
  return n;
}
/* today's rows in the tables, with where to tick them */
function trkTodayRows(){
  var keep=S.trkWho; S.trkWho='me';
  try{ return trkTodayRowsMine(); } finally { S.trkWho=keep; }
}
function trkTodayRowsMine(){
  var out=[], today=dayKey();
  ['week','month','c30'].forEach(function(type){
    var st=trkState(); if(!st.cfg[type]) return;
    var cfg=st.cfg[type]; if(cfg.next) return;
    var days=trkDays(type,cfg), di=-1;
    days.forEach(function(x,i){ if(dayKey(x)===today) di=i; });
    if(di<0) return;
    var rec=trkRec(type,cfg,false);
    cfg.rows.forEach(function(r){ if(!r.t) return; var tk=rec && rec.ticks[normLine(r.t)];
      out.push({type:type, cfg:cfg, row:r, di:di, done:!!(tk && tk[di])}); });
  });
  return out;
}
function initCount(L,d){ return (L ? (L.inits||[]).length + (L.items||[]).filter(function(x){ return x.init && x.done; }).length : 0) + (d ? trkTicksOn(d) : 0); }
function pathDone(){
  var today=dayKey(), L=(S.log||{})[today]||{}, td=today3();
  return {
    pause: !!L.breath,
    choose: !!L.intent,
    init: (L.inits||[]).length>0 || td.items.some(function(x){ return x.init && x.done; }) || trkTicksOn(today)>0,
    ahead: !!L.ahead,
    feel: (L.pauses||[]).length>0,
    game: gmMine().lastDay===today || gmMine().daily===today
  };
}
function fullStreak(){
  var n=0, d=new Date(), f=S.full||{};
  if(!f[dayKey(d)]) d.setDate(d.getDate()-1);
  while(f[dayKey(d)]){ n++; d.setDate(d.getDate()-1); }
  return n;
}
function renderPath(){
  var box=document.getElementById('pathBox'); if(!box) return;
  var done=pathDone(), n=PATH_STEPS.filter(function(s){ return done[s.k]; }).length, today=dayKey();
  if(!S.full) S.full={};
  var fresh=false;
  if(n===4 && !S.full[today]){ S.full[today]=1; fresh=true; addPts(20); save(); setTimeout(celebrate,300); toast(t('path.fullxp')); }
  var next=PATH_STEPS.filter(function(s){ return !done[s.k]; })[0], streak=fullStreak();
  var Ltoday=(S.log||{})[today]||{}, yd=new Date(); yd.setDate(yd.getDate()-1);
  var ya=((S.log||{})[dayKey(yd)]||{}).ahead, yPlan=(ya && ya.o && ya.t && new Date().getHours()<17) ? ya : null;
  box.className='path-box'+(n===4?' full':'');
  box.innerHTML='<div class="path-top"><b>'+esc(t('path.t'))+'</b><span>'+esc(t('path.n',{n:n}))+'</span></div>'+
    '<div class="path-steps">'+PATH_STEPS.map(function(s,i){
      return (i?'<i class="path-line'+(done[PATH_STEPS[i-1].k]?' on':'')+'"></i>':'')+
        '<button type="button" class="path-step'+(done[s.k]?' on':'')+(next&&next.k===s.k?' is-next':'')+'" data-path="'+s.k+'">'+
        '<span class="path-dot">'+ic(done[s.k]?'check':s.icon)+'</span><small>'+esc(t('path.'+s.k))+'</small></button>'; }).join('')+'</div>'+
    '<p class="path-msg">'+esc(n===4 ? t('path.full') : n===0 ? t('path.go') : t('path.next',{s:t('path.'+next.k)}))+
      (streak>=2 ? ' <span class="path-streak">'+esc(t('path.streak',{n:streak}))+'</span>' : '')+'</p>'+
    (Ltoday.intent ? '<p class="path-note">'+ic('compass')+'<span>'+esc(t('in.line',{x:Ltoday.intent}))+'</span></p>' : '')+
    (yPlan ? '<p class="path-note pn-plan">'+ic('flag')+'<span>'+esc(t('ah.plan',{o:yPlan.o, t:yPlan.t}))+'</span></p>' : '')+
    '<div class="path-bonus"><span>'+esc(t('path.bonus'))+'</span>'+
      '<button type="button" class="pb'+(done.feel?' on':'')+'" data-path="feel">'+ic(done.feel?'check':'face')+'<span>'+esc(t('path.feel'))+'</span></button>'+
      '<button type="button" class="pb'+(done.game?' on':'')+'" data-path="game">'+ic(done.game?'check':'star')+'<span>'+esc(t('path.game'))+'</span></button></div>';
  if(fresh) box.classList.add('pop');
  box.querySelectorAll('[data-path]').forEach(function(b){ b.addEventListener('click',function(){
    var k=b.dataset.path;
    if(k==='pause') pzOpen('day');
    else if(k==='feel') pzOpen('feel');
    else if(k==='choose') pzOpen('intent');
    else if(k==='init') pzOpen('init');
    else if(k==='ahead') pzOpen('ahead');
    else if(k==='game'){ gmPlayer={k:'me'}; goPage('games'); gmStart(gmDaily()); }
    else { var tb=document.getElementById('todayBox'); if(tb){ tb.scrollIntoView({behavior:'smooth',block:'start'}); var inp=tb.querySelector('[data-t3new]'); if(inp) setTimeout(function(){ inp.focus(); },400); } }
  }); });
}
"""