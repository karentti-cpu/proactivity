# -*- coding: utf-8 -*-
JS_APP = r"""
/* ================= state ================= */
var P={name:'',age:'',email:'',goals:['study','sport','sleep','food'],customCats:[],
       diff:'mid',workout:'general',fitLevel:'beginner',time:'30',actPref:'mix',
       easy:[],hard:[],dream:'',skinType:'normal',userGoals:[],
       plan:null, trialStart:null, founder:false, remind:'17:00',
       chainGoal:null, planAfter:null,
       gender:'', accent:'sage', theme:'light'};
/* The first screen is deliberately white with a soft green, rather than
   following the device - most phones are set to dark, so "follow the device"
   meant almost nobody ever saw the calm version. One tap on the sun/moon
   changes it and the choice is remembered for good. */
/* S.streak is the count of ticks ever made and is kept only so old saves keep
   their number; the streak the user is shown is S.day, a real run of calendar
   days built with the same bumpStreak/liveStreak helpers the mini-apps use. */
/* streak and chDone are dead fields kept so an old save round-trips through
   JSON unchanged; the live value is S.day. S.next, the old daily suggestion, is
   kept the same way. */
var S={points:0,streak:0,chDone:false,tasks:[],missions:[],plan:{},goals:[],
       quiz:null, lessons:{}, ach:{}, next:null, tips:{}, hist:[], ref:null,
       day:{streak:0,lastDay:null},
       stats:{tasksDone:0,challenges:0,comebacks:0,bestStreak:0}};
var CATS=[], uid=1;

/* ================= theme ================= */
var ACCENTS=['sage','flame','bloom','mint'];

function activeTheme(){ return P.theme==='dark' ? 'dark' : 'light'; }

function applyTheme(){
  var d=document.documentElement;
  d.setAttribute('data-theme', activeTheme());
  d.setAttribute('data-accent', ACCENTS.indexOf(P.accent)>=0 ? P.accent : 'sage');
  document.querySelectorAll('[data-set-accent]').forEach(function(b){
    b.classList.toggle('on', b.dataset.setAccent===P.accent);
  });
  var mb=document.getElementById('modeBtn');
  if(mb) mb.classList.toggle('is-light', activeTheme()==='light');
  var meta=document.querySelector('meta[name="theme-color"]');
  if(meta) meta.setAttribute('content', activeTheme()==='light' ? '#FBF9F5' : '#14161C');
}
/* Appearance is stored under its own keys, not inside the profile: the profile
   is only written once onboarding completes, and a colour picked on the landing
   page must still survive a refresh. */
function saveLook(){
  try{
    localStorage.setItem('proactive_accent', P.accent||'mint');
    localStorage.setItem('proactive_theme', P.theme||'');
  }catch(e){}
}
function loadLook(){
  try{
    var a=localStorage.getItem('proactive_accent');
    if(ACCENTS.indexOf(a)>=0) P.accent=a;
    var th=localStorage.getItem('proactive_theme');
    if(th==='light'||th==='dark') P.theme=th;
  }catch(e){}
}
/* Gender is picked during onboarding, before save() is allowed to write a
   profile, so like the accent it lives under its own key and that key wins.
   An older save can still hold the boy/girl/na values from the question this
   replaced, so those map across rather than being dropped. */
var LEGACY_GENDER={boy:'m', girl:'f', na:'n'};
function loadGender(){
  try{
    var g=localStorage.getItem('proactive_gender');
    if(GENDERS.indexOf(g)>=0){ gnd=g; P.gender=g; return; }
  }catch(e){}
  var fromProfile=LEGACY_GENDER[P.gender] || (GENDERS.indexOf(P.gender)>=0 ? P.gender : '');
  gnd=fromProfile; P.gender=fromProfile;
  if(fromProfile){ try{ localStorage.setItem('proactive_gender', fromProfile); }catch(e){} }
}
function setAccent(a){
  if(ACCENTS.indexOf(a)<0) return;
  P.accent=a; saveLook(); applyTheme(); redrawColoured();
}
function setTheme(mode){ P.theme=mode; saveLook(); applyTheme(); redrawColoured(); }

/* the progress ring paints with real colour values, so it has to be redrawn
   whenever the palette changes */
function redrawColoured(){
  if(document.getElementById('app').style.display==='block'){ renderRing(); renderMini(); }
}
function cssVar(name){
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

document.addEventListener('click',function(e){
  var a=e.target.closest('[data-set-accent]');
  if(a){ setAccent(a.dataset.setAccent); return; }
  var m=e.target.closest('#modeBtn');
  if(m){ setTheme(activeTheme()==='light' ? 'dark' : 'light'); }
});

/* Local calendar day, not UTC - with UTC the day would roll over at the wrong
   hour and break every streak for anyone not on GMT. */
function dayKey(d){
  d = d || new Date();
  return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
}
function daysBetween(a,b){
  return Math.round((new Date(b+'T00:00:00') - new Date(a+'T00:00:00'))/86400000);
}
/* Shared by the sport and skincare mini-apps: same day is a no-op, yesterday
   extends the run. One missed day is forgiven once per run - a month of work
   should not be wiped out by a single bad Tuesday, which is the moment most
   people stop opening the app for good. A second miss does reset it: a streak
   that can never break is not a streak. */
function bumpStreak(o,day){
  day = day || dayKey();
  if(o.lastDay === day) return o.streak;
  var gap = o.lastDay ? daysBetween(o.lastDay, day) : 0;
  if(!o.lastDay){ o.streak=1; o.grace=0; }
  else if(gap === 1){ o.streak=(o.streak||0)+1; }
  else if(gap === 2 && !o.grace){ o.streak=(o.streak||0)+1; o.grace=1; }
  else { o.streak=1; o.grace=0; }
  o.lastDay = day;
  return o.streak;
}
/* A run that was broken before today should read as 0, not as its stale value.
   A run with one day missed and the grace still unspent is not broken yet: act
   today and it carries on, so it keeps showing. */
function liveStreak(o){
  if(!o || !o.lastDay) return 0;
  var gap = daysBetween(o.lastDay, dayKey());
  if(gap === 0 || gap === 1) return o.streak||0;
  if(gap === 2 && !o.grace) return o.streak||0;
  return 0;
}
/* True while one missed day can still be rescued by acting today. */
function streakRescuable(o){
  if(!o || !o.lastDay || o.grace) return false;
  return daysBetween(o.lastDay, dayKey()) === 2;
}

function emptyMini(){
  return {
    view:'hub',
    sport: {sessions:[], streak:0, lastDay:null},
    skin:  {setup:null, routine:null, log:{}, streak:0, lastDay:null},
    fridge:{pantry:[], favs:[], history:[], photo:null}
  };
}

var STORE_V=4;
/* The profile is written only once setup finishes. Anything that fires during
   onboarding - an achievement unlocking off the check-in, a tip - must not
   persist a half-built profile, or a refresh drops the user into the app with
   steps still unfinished. The look, the answers and the chain each have their
   own key and are unaffected. */
function save(){ try{
  if(onbActive) return;
  saveLook();
  if(GENDERS.indexOf(P.gender)>=0) localStorage.setItem('proactive_gender', P.gender);
  localStorage.setItem('proactive_v',STORE_V);
  localStorage.setItem('proactive_p',JSON.stringify(P));
  localStorage.setItem('proactive_s',JSON.stringify(S));
  localStorage.setItem('proactive_uid',uid);
}catch(e){ if(typeof warnQuota==='function') warnQuota(); } }

/* ids must never collide with ids already sitting in storage, whatever their
   origin - a stale counter silently makes one checkbox toggle another row. */
function reseedUid(){
  var max=0;
  function seen(n){ n=Number(n); if(n>max) max=n; }
  (S.tasks||[]).forEach(function(x){ seen(x.id); });
  (S.missions||[]).forEach(function(x){ seen(x.id); });
  (S.goals||[]).forEach(function(g){ seen(g.id); (g.actions||[]).forEach(function(a){ seen(a.id); }); });
  (P.customCats||[]).forEach(function(c){ var m=/^custom_(\d+)$/.exec(c.id||''); if(m) seen(m[1]); });
  var stored=Number(localStorage.getItem('proactive_uid'))||1;
  uid=Math.max(stored,max+1,1);
}

/* v1 stored every task, mission and category label as a hardcoded Hebrew
   string and category icons as emoji, so carrying that straight into the new
   build leaves Hebrew text in the other four languages and icon references
   that resolve to nothing. Keep the progress, rebuild the labelled parts. */
function migrateV1(){
  P.customCats=(P.customCats||[]).map(function(c){
    return {id:c.id, name:c.name, icon:'star', custom:true, sg:['sg.generic']};
  });
  P.easy=[]; P.hard=[];                 // v1 stored these as Hebrew literals
  S.tasks=[]; S.missions=[]; S.plan={}; // re-seeded below from the new schema
  S.goals=(S.goals||[]).map(function(g){
    return {id:g.id, title:g.title,     // the user typed these, so they stay
            actions:guessSteps(g.title).map(function(k){
              return {id:0,key:k,text:'',done:false};
            })};
  });
  if(!P.trialStart) P.trialStart=Date.now();
}

/* v2 predates the mini-apps. Additive only: nothing stored by v2 is touched. */
function migrateV2(){
  if(!S.mini) S.mini=emptyMini();
}

/* Fields the v4 schema adds. Object.assign in load() merges a stored save over
   the defaults, so a v3 save arrives with these already present (as defaults);
   this only backfills a save that was hand-edited or partially written. */
/* Goals made by the chain used to be named "<what> · <how often>". The how
   often is on the goal already, so the suffix comes off - in whichever
   language the goal was made - and the weekly mission follows the name. */
function tidyGoalTitles(){
  (S.goals||[]).forEach(function(g){
    if(!g.freq || !g.title) return;
    Object.keys(I18N).forEach(function(l){
      var f=I18N[l]['gf.'+g.freq], suf=' · '+f;
      if(f && g.title.length>suf.length && g.title.slice(-suf.length)===suf){
        var old=g.title; g.title=g.title.slice(0,-suf.length);
        (S.missions||[]).forEach(function(m){ if(m.goalId===g.id && m.title===old) m.title=g.title; });
      }
    });
  });
}
function ensureV4Fields(){
  if(!S.quiz) S.quiz=emptyQuiz();
  if(!S.lessons) S.lessons={};
  if(!S.ach) S.ach={};
  if(!S.tips) S.tips={};
  if(!S.hist) S.hist=[];
  if(S.quiz){ if(!S.quiz.areas) S.quiz.areas=[]; if(!S.quiz.blocks) S.quiz.blocks=[]; }
  if(S.mini && S.mini.skin && typeof migrateRoutine==='function') migrateRoutine(S.mini.skin);
  if(!S.day) S.day={streak:0,lastDay:null};
  if(!S.ref) S.ref=emptyRef();          /* the referral code and what it earned */
  if(!S.stats) S.stats={tasksDone:0, challenges:0, comebacks:0, bestStreak:0};
  /* Goals made before the start gate existed were tracked from the day they
     were written, so they count as started - anything else would silently
     stop a streak someone already has. */
  (S.goals||[]).forEach(function(g){ if(g.started===undefined){ g.started=true; g.startedAt=g.startedAt||null; } });
}

/* v3 predates the check-in, the lessons, the achievements and the real day
   streak. Additive only: nothing stored by v3 is touched. The old S.streak
   counted ticks rather than days, so it seeds stats.tasksDone - which is what
   it actually measured - and the day streak starts fresh instead of inheriting
   a number that never meant days. */
function migrateV3(){
  ensureV4Fields();
  S.stats.tasksDone = Number(S.streak)||0;
}

/* Every real action routes through here: it is the single place that decides
   the day streak, so nothing can bump it twice in one day and a missed day
   simply starts a new run instead of "failing". */
function markActiveToday(){
  if(!S.day) S.day={streak:0,lastDay:null};
  var day=dayKey();
  if(S.day.lastDay===day) return;
  var gap = S.day.lastDay ? daysBetween(S.day.lastDay,day) : 0;
  var broke = S.day.lastDay && (gap>2 || (gap===2 && S.day.grace));
  bumpStreak(S.day,day);
  if(broke) S.stats.comebacks=(S.stats.comebacks||0)+1;
  S.stats.bestStreak=Math.max(S.stats.bestStreak||0, S.day.streak||0);
  save();
  if((S.day.streak||0)>=3 && typeof tip==='function') tip('streak');
}
function shownStreak(){ return liveStreak(S.day); }
function streakLine(){
  var n=shownStreak();
  if(streakRescuable(S.day)) return t('d.sk.rescue',{n:n});
  if(n<=0 && S.day && S.day.lastDay) return t('d.sk.miss');
  return n<=0 ? t('d.sk.0') : n===1 ? t('d.sk.1') : t('d.sk.n',{n:n});
}

function load(){ try{
  var p=localStorage.getItem('proactive_p'), s=localStorage.getItem('proactive_s');
  if(!p||!s) return false;
  var pp=JSON.parse(p);
  /* A profile written before Pro existed has no `founder` field at all. Those
     people were promised a free app and got one, so they keep every feature for
     good - checked before the merge, because the default would mask it. */
  var grandfather = !('founder' in pp);
  P=Object.assign(P,pp); S=Object.assign(S,JSON.parse(s));
  if(grandfather) P.founder=true;
  reseedUid();                          // before anything hands out a new id
  var v=Number(localStorage.getItem('proactive_v'))||1;
  if(v<2){
    migrateV1();
    buildCats();
    seedTasks(); seedMissions();        // rebuilt in the new shape; goals kept
    S.goals.forEach(function(g){
      g.id=uid++; g.actions.forEach(function(a){ a.id=uid++; });
    });
  }
  if(v<3) migrateV2();                  // chains, so a v1 save lands on v4
  if(v<4) migrateV3();
  if(!S.mini) S.mini=emptyMini();       // belt and braces for a hand-edited save
  ensureV4Fields();
  tidyGoalTitles();
  loadQuiz();                           // answers saved before onboarding ended
  if(v<STORE_V) save();
  return true;
}catch(e){ return false; } }

function buildCats(){
  CATS = ALL_CATS.filter(function(c){ return P.goals.indexOf(c.id)>=0; });
  P.customCats.forEach(function(cc){ if(!CATS.some(function(c){return c.id===cc.id;})) CATS.push(cc); });
  if(!CATS.length) CATS = ALL_CATS.slice();
}
function catById(id){
  var all=ALL_CATS.concat(P.customCats);
  for(var i=0;i<all.length;i++) if(all[i].id===id) return all[i];
  return null;
}
function catName(c){ return c ? (c.custom ? c.name : t(c.k)) : ''; }
function pick(a){ return a[Math.floor(Math.random()*a.length)]; }

var toastT;
function toast(msg){
  var el=document.getElementById('toast');
  el.textContent=msg; el.classList.add('on');
  clearTimeout(toastT); toastT=setTimeout(function(){ el.classList.remove('on'); },2400);
}
/* S.points is the XP total. A level or a rank gained here is announced a beat
   after the praise toast most awards fire right behind this call, so the two
   do not overwrite each other. */
function addPts(n){
  /* when in the day the steps happen, for "what I have learned about you" */
  if(n>0){ var h=new Date().getHours(), b=h<12?'m':h<17?'n':'e'; if(!S.hours) S.hours={m:0,n:0,e:0}; S.hours[b]=(S.hours[b]||0)+1; }
  var before=levelInfo();
  S.points=Math.max(0,S.points+n); save();
  var after=levelInfo();
  if(n>0 && after.level>before.level){
    var msg = after.tier>before.tier ? t('av.rankup',{x:t(after.rank.k)}) : t('av.lvlup',{n:after.level});
    setTimeout(function(){ toast(msg); celebrate(); }, 1400);
    if(typeof renderStats==='function' && document.getElementById('app').style.display==='block') renderStats();
  }
}
function praise(){ return t(pick(PRAISE)); }

/* A short burst of confetti and a light buzz for the moments that matter:
   all three things done, a goal's step done, a level up, the week written
   up. Nothing for every tick - a celebration that happens all the time
   stops being one. Skipped when the device asks for reduced motion. */
function celebrate(){
  try{ if(navigator.vibrate) navigator.vibrate(35); }catch(e){}
  if(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var host=document.createElement('div'); host.className='confetti'; host.setAttribute('aria-hidden','true');
  var cols=['#3D7B5E','#8DB86E','#D99A26','#FF7FB0','#3DDCA8'];
  for(var i=0;i<36;i++){
    var p=document.createElement('i');
    p.style.left=(Math.random()*100)+'%';
    p.style.background=cols[i%cols.length];
    p.style.animationDelay=(Math.random()*.25)+'s';
    p.style.setProperty('--dx',(Math.random()*120-60)+'px');
    p.style.setProperty('--r',(Math.random()*720-360)+'deg');
    host.appendChild(p);
  }
  document.body.appendChild(host);
  setTimeout(function(){ host.remove(); },1900);
}

/* ================= pricing ================= */
var PRICES={
  he:{sym:'₪', m:19,  y:13,  ytot:149},
  en:{sym:'$', m:4.99,y:3.49,ytot:39},
  fr:{sym:'€', m:4.99,y:3.49,ytot:39},
  ru:{sym:'₽', m:399, y:249, ytot:2990},
  ar:{sym:'$', m:4.99,y:3.49,ytot:39}
};
function money(n){
  var p=PRICES[cur]||PRICES.en;
  var s=(n%1===0)? String(n) : n.toFixed(2);
  return cur==='ru' ? (s+' '+p.sym) : (p.sym+s);
}
function renderPrices(){
  var p=PRICES[cur]||PRICES.en;
  document.querySelectorAll('[data-price]').forEach(function(el){
    el.textContent = money(el.dataset.price==='annual' ? p.y : p.m);
  });
  document.querySelectorAll('[data-bill]').forEach(function(el){
    el.textContent = el.dataset.bill==='annual'
      ? money(p.ytot)+' · '+t('l.pr.billedy')
      : t('l.pr.billedm');
  });
}

/* ================= trial strip ================= */
var TRIAL_DAYS=14;
function trialDaysLeft(){
  if(!P.trialStart) return TRIAL_DAYS;
  var used=Math.floor((Date.now()-P.trialStart)/86400000);
  return Math.max(0, TRIAL_DAYS-used);
}
/* The strip tells the truth about the account and nothing else. With no
   checkout configured there is no trial to count down, so it stays away rather
   than inventing a deadline nobody can act on. */
function renderTrial(){
  var bar=document.getElementById('trialBar');
  var st=(typeof proState==='function') ? proState() : 'open';
  if(st==='open'||st==='founder'||st==='pro'){ bar.classList.remove('on'); return; }
  bar.classList.add('on');
  var n=trialDaysLeft();
  document.getElementById('trialTxt').textContent =
    st==='free' ? t('trial.over')
    : n>1 ? t('trial.left',{n:n}) : t('trial.last');
}
document.getElementById('trialCta').addEventListener('click',function(){
  document.getElementById('app').style.display='none';
  document.getElementById('onboarding').style.display='block';
  showStep(8);
});

/* ================= landing ================= */
function goOnboarding(){
  onbActive=true;
  document.getElementById('landing').style.display='none';
  document.body.classList.remove('has-sticky');
  document.getElementById('stickyCta').style.display='none';
  document.getElementById('onboarding').style.display='block';
  window.scrollTo(0,0);
  showStep(1);
}
['ctaTop','ctaBottom','ctaSticky'].forEach(function(id){
  document.getElementById(id).addEventListener('click',goOnboarding);
});
document.body.classList.add('has-sticky');
/* The sticky button only once the hero's own button has scrolled away -
   two "start" buttons on one screen read as two different things. */
if('IntersectionObserver' in window){
  new IntersectionObserver(function(es){
    document.body.classList.toggle('past-hero', !es[0].isIntersecting);
  }).observe(document.getElementById('ctaTop'));
} else document.body.classList.add('past-hero');

/* ================= onboarding ================= */
/* The way in is three screens: 1 welcome · 2 about you · 6 first goal, and
   then the app. The check-in (4, with its result on 5) is offered inside the
   app instead of standing between a new user and the first screen; 3 and 7
   are no longer on the path. Step 8 is the plans screen: deliberately not
   part of the count, reached only from the trial strip. */
var ONB_FLOW=[1,2,6];
var os=1, ONB_TOTAL=ONB_FLOW.length;
/* True only while the user is walking the setup flow. The plans screen reuses
   the same overlay from inside the app, and without this flag paying from
   there used to re-run seedState() and wipe every task, mission and goal. */
var onbActive=false;

function showStep(n){
  os=n;
  document.querySelectorAll('.step').forEach(function(s){ s.classList.remove('on'); });
  var el=document.querySelector('.step[data-step="'+n+'"]');
  if(el) el.classList.add('on');
  var bar=document.getElementById('onbBar');
  var count=document.getElementById('stepCount');
  if(n===4){
    renderQuiz();                       // owns the bar and the counter itself
  } else {
    var at=ONB_FLOW.indexOf(n)+1;
    if(bar) bar.style.width=Math.round((at||ONB_TOTAL)/ONB_TOTAL*100)+'%';
    if(count) count.textContent = at ? t('o.step',{n:at,t:ONB_TOTAL}) : '';
  }
  if(n===5) renderProfile('rsBody');
  if(n===6) renderChain('onbChain');
  if(n===8) renderBuilt();
  var h=el && el.querySelector('h2');
  if(h) h.setAttribute('tabindex','-1');
  window.scrollTo(0,0);
}

function renderGoalOpts(){
  var box=document.getElementById('oGoals'); box.innerHTML='';
  ALL_CATS.concat(P.customCats).forEach(function(c){
    var on=P.goals.indexOf(c.id)>=0;
    var d=document.createElement('button');
    d.type='button';
    d.className='opt'+(on?' on':'');
    d.setAttribute('aria-pressed', on?'true':'false');
    d.innerHTML=ic(c.icon)+'<span>'+esc(catName(c))+'</span>';
    d.onclick=function(){
      var i=P.goals.indexOf(c.id);
      if(i>=0) P.goals.splice(i,1); else P.goals.push(c.id);
      var now=P.goals.indexOf(c.id)>=0;
      d.classList.toggle('on', now);
      d.setAttribute('aria-pressed', now?'true':'false');
    };
    box.appendChild(d);
  });
}

function singleSelect(boxId,attr,field){
  var box=document.getElementById(boxId);
  if(!box) return;
  box.querySelectorAll('.opt').forEach(function(o){
    o.addEventListener('click',function(){
      box.querySelectorAll('.opt').forEach(function(x){
        x.classList.remove('on'); x.setAttribute('aria-pressed','false');
      });
      o.classList.add('on'); o.setAttribute('aria-pressed','true');
      P[field]=o.dataset[attr];
    });
  });
}

/* Replaces the old "are you a boy or a girl" question. It asked for something
   the app never needed in order to pick a colour, so now it just asks for the
   colour. The top bar still overrides it at any time. */
function bindGenderPick(){
  var box=document.getElementById('oGender');
  if(!box) return;
  box.querySelectorAll('[data-gnd]').forEach(function(o){
    o.addEventListener('click',function(){
      setGender(o.dataset.gnd);   // redraws every string on screen immediately
      markSelected();
    });
  });
}
function bindAccentPick(){
  var box=document.getElementById('oAcc');
  if(!box) return;
  box.querySelectorAll('[data-acc]').forEach(function(o){
    o.addEventListener('click',function(){
      setAccent(o.dataset.acc);
      markSelected();
    });
  });
}

function markSelected(){
  document.querySelectorAll('#oGender [data-gnd]').forEach(function(o){
    var on=o.dataset.gnd===P.gender;
    o.classList.toggle('on', on);
    o.setAttribute('aria-pressed', on?'true':'false');
  });
  document.querySelectorAll('#oAcc [data-acc]').forEach(function(o){
    var on=o.dataset.acc===P.accent;
    o.classList.toggle('on', on);
    o.setAttribute('aria-pressed', on?'true':'false');
  });
  [['oTime','time','time'],['oWO','wo','workout'],
   ['oFL','fl','fitLevel'],['oSkin','skin','skinType']]
  .forEach(function(x){
    document.querySelectorAll('#'+x[0]+' .opt').forEach(function(o){
      var on=o.dataset[x[1]]===P[x[2]];
      o.classList.toggle('on', on);
      o.setAttribute('aria-pressed', on?'true':'false');
    });
  });
}

function renderBuilt(){
  var box=document.getElementById('builtList');
  if(!box) return;
  box.innerHTML =
    '<div>'+ic('check')+'<span>'+esc(t('o.9.built1',{n:Math.max(1,P.goals.length)}))+'</span></div>'+
    '<div>'+ic('check')+'<span>'+esc(t('o.9.built2'))+'</span></div>'+
    '<div>'+ic('check')+'<span>'+esc(t('o.9.built3',{n:P.userGoals.length||1}))+'</span></div>';
}

function readStep2(){
  P.name=document.getElementById('oName').value.trim();
  var a=parseInt(document.getElementById('oAge').value,10);
  if(a>=AGE_MIN && a<=AGE_MAX) P.age=String(a);
}
/* Leaving the overlay for the app when the check-in was opened from inside
   it, rather than walking on into the setup screens. */
function backToApp(page){
  document.getElementById('onboarding').style.display='none';
  document.getElementById('app').style.display='block';
  document.body.classList.add('in-app');
  goPage(page||'progress');
}

document.querySelectorAll('[data-next]').forEach(function(b){
  b.addEventListener('click',function(){
    if(os===2) readStep2();          /* the age is asked by the check-in itself */
    /* Every screen after this one speaks in the chosen form; without a choice
       it falls back to the slash form ("מתחיל/ה"), which reads as a form to
       fill in rather than as someone talking to you. "No preference" counts. */
    if(os===2 && GENDERS.indexOf(P.gender)<0){
      toast(t('t.pickgnd'));
      var og=document.getElementById('oGender'); if(og){ og.classList.remove('nudge'); void og.offsetWidth; og.classList.add('nudge'); }
      return;
    }
    var k=ONB_FLOW.indexOf(os);
    showStep(k>=0 && k<ONB_FLOW.length-1 ? ONB_FLOW[k+1] : os+1);
  });
});
document.querySelectorAll('[data-back]').forEach(function(b){
  b.addEventListener('click',function(){
    if(os===2) readStep2();
    var k=ONB_FLOW.indexOf(os);
    showStep(k>0 ? ONB_FLOW[k-1] : Math.max(1,os-1));
  });
});

document.getElementById('qzPrev').addEventListener('click',function(){
  if(S.quiz.i>0){ S.quiz.i--; renderQuiz(); }
  else if(onbActive) showStep(3);
  else backToApp();
});
document.getElementById('rsNext').addEventListener('click',function(){
  if(onbActive) showStep(6); else backToApp();
});

document.getElementById('addCustom').addEventListener('click',function(){
  var inp=document.getElementById('oCustom'), v=inp.value.trim();
  if(!v) return;
  var id='custom_'+(uid++);
  P.customCats.push({id:id,name:v,icon:'star',custom:true,sg:['sg.generic']});
  P.goals.push(id); inp.value='';
  renderGoalOpts(); toast(t('t.added',{x:v}));
});
document.getElementById('oCustom').addEventListener('keydown',function(e){
  if(e.key==='Enter'){ e.preventDefault(); document.getElementById('addCustom').click(); }
});

/* The free-text fallback under the chain: a target in the user's own words. */
function readFirstGoal(){
  var el=document.getElementById('oG1');
  var v=el ? el.value.trim() : '';
  P.userGoals = v ? [v] : [];
  P.dream = v;
}
document.getElementById('skipGoal').addEventListener('click',function(){
  P.userGoals=[]; P.chainGoal=null; resetChain(); finishOnboarding();
});
document.getElementById('oG1').addEventListener('keydown',function(e){
  if(e.key==='Enter'){ e.preventDefault(); readFirstGoal(); if(P.userGoals.length){ P.chainGoal=null; resetChain(); finishOnboarding(); } }
});
document.getElementById('oG1Go').addEventListener('click',function(){
  readFirstGoal(); if(P.userGoals.length){ P.chainGoal=null; resetChain(); finishOnboarding(); } else toast(t('t.writegoal'));
});
document.getElementById('skipBody').addEventListener('click', function(){ finishOnboarding(); });
document.getElementById('oFinish').addEventListener('click', function(){ finishOnboarding(); });
document.getElementById('skipPay').addEventListener('click',function(){
  if(!P.trialStart) P.trialStart=Date.now();
  closePlans();
});

/* Leaving the plans screen. During setup that means finishing setup; from
   inside the app it means going back to the app untouched. */
function closePlans(){
  if(onbActive){ finishOnboarding(); return; }
  document.getElementById('onboarding').style.display='none';
  document.getElementById('app').style.display='block';
  document.body.classList.add('in-app');
  renderTrial();
  window.scrollTo(0,0);
}

function finishOnboarding(){
  if(!P.trialStart) P.trialStart=Date.now();
  onbActive=false;
  applyInvite();                      /* a sign-up through a friend's link */
  buildCats(); seedState();
  /* the chain parked its target on the profile; seed it now and, if the user
     pressed "start", start it - creating a goal never starts anything by itself */
  if(P.chainGoal && P.chainGoal.goal){
    var cg=P.chainGoal.goal; cg.id=uid++; cg.actions.forEach(function(a){ a.id=uid++; });
    S.goals.unshift(cg);
    if(P.chainGoal.start){ cg.started=true; cg.startedAt=dayKey();
      var ca=areaById(cg.area);
      S.missions.push({id:uid++, catId:ca?ca.cat:'hobby', titleKey:null, title:cg.title,
        target:Math.min(7,Math.max(1, cg.freq===5?6:(cg.freq||3))), goalId:cg.id,
        days:[false,false,false,false,false,false,false]});
    }
    P.chainGoal=null;
  }
  if(S.quiz && !S.quiz.scores && quizAnswered()) { S.quiz.scores=scoreQuiz(); applyProfileToPlan(); }
  markActiveToday();
  save(); checkAchievements();
  document.getElementById('onboarding').style.display='none';
  document.getElementById('app').style.display='block';
  document.body.classList.add('in-app');
  window.scrollTo(0,0);
  startApp();
}

function difficultyMult(){ return ({easy:1,mid:1.4,hard:2})[P.diff]||1; }

function seedTasks(){
  var mult=difficultyMult();
  S.tasks=[];
  CATS.forEach(function(cat){
    S.tasks.push({id:uid++, catId:cat.id, titleKey:cat.dk||null,
      title:cat.custom?cat.name:'',
      min: cat.id==='study' ? Math.round(20*mult)
         : cat.id==='sport' ? Math.round(Number(P.time)||30) : 0,
      done:false, photo:null});
  });
}

function seedMissions(){
  var target=Math.max(2,Math.round(3*difficultyMult()));
  S.missions=[];
  CATS.forEach(function(cat){
    S.missions.push({id:uid++, catId:cat.id, titleKey:cat.custom?null:cat.k,
      title:cat.custom?cat.name:'', target:Math.min(7,target),
      days:[0,0,0,0,0,0,0].map(function(){return false;})});
  });
}

function seedGoals(){
  S.goals=[];
  P.userGoals.forEach(function(g){ S.goals.push(newGoal(g)); });
}
/* Every goal carries the ladder the app is built around: the goal itself,
   what it means this week, what it means today, and the suggested steps. */
function newGoal(title){
  return {id:uid++, title:title, week:'', today:'', now:'',
          started:false, startedAt:null,          // nothing counts until "start the target"
          area:null, kind:null, kindText:'', freq:null, obst:null,
          actions:guessSteps(title).map(function(k){
            return {id:uid++, key:k, text:'', done:false};
          })};
}

function seedState(){
  seedTasks(); seedMissions(); seedGoals();
  if(!S.mini) S.mini=emptyMini();
}
/* task/mission/action labels may be a translation key or user text */
function label(o){ return o.titleKey ? t(o.titleKey) : (o.title||''); }
function actLabel(a){ return a.key ? t(a.key) : (a.text||''); }
"""
