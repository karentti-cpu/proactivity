# -*- coding: utf-8 -*-
JS_RENDER = r"""
/* ================= camera ================= */
var camStream=null;
function openCam(name,cb){
  var modal=document.getElementById('camModal'), v=document.getElementById('camV'),
      pv=document.getElementById('camP'), fi=document.getElementById('camF'),
      bar=document.getElementById('camBtns');
  document.getElementById('camTN').textContent=name;
  pv.style.display='none'; v.style.display='block'; modal.classList.add('on');
  var shot=null;

  function stop(){ if(camStream){ camStream.getTracks().forEach(function(t){t.stop();}); camStream=null; } }
  function close(){ stop(); modal.classList.remove('on'); }
  function mk(cls,html){ var b=document.createElement('button'); b.className='btn '+cls; b.innerHTML=html; return b; }
  /* A photo is a nice record, not a gate: closing without one still counts. */
  function skipBtn(){ var k=mk('btn-ghost', ic('check')+'<span>'+esc(t('c.nophoto'))+'</span>'); k.onclick=function(){ close(); cb(null); }; return k; }

  function buttons(mode){
    bar.innerHTML='';
    if(mode==='live'){
      var s=mk('btn-primary', ic('camera')+'<span>'+esc(t('c.takephoto'))+'</span>'),
          g=mk('btn-ghost',   ic('image')+'<span>'+esc(t('c.gallery'))+'</span>'),
          c=mk('btn-quiet',   esc(t('c.cancel')));
      s.onclick=function(){
        var cv=document.createElement('canvas');
        cv.width=v.videoWidth||640; cv.height=v.videoHeight||480;
        cv.getContext('2d').drawImage(v,0,0,cv.width,cv.height);
        shot=cv.toDataURL('image/jpeg',0.6);
        pv.src=shot; pv.style.display='block'; v.style.display='none'; stop(); buttons('ok');
      };
      g.onclick=function(){ fi.click(); };
      c.onclick=close;
      bar.append(s,g,skipBtn(),c);
    } else if(mode==='upload'){
      var u=mk('btn-primary', ic('image')+'<span>'+esc(t('c.choosephoto'))+'</span>'),
          c2=mk('btn-quiet', esc(t('c.cancel')));
      u.onclick=function(){ fi.click(); }; c2.onclick=close;
      bar.append(u,skipBtn(),c2);
    } else {
      var ok=mk('btn-primary', ic('check')+'<span>'+esc(t('c.use'))+'</span>'),
          re=mk('btn-ghost', esc(t('c.retake')));
      ok.onclick=function(){ close(); cb(shot); };
      re.onclick=function(){ pv.style.display='none'; start(); };
      bar.append(ok,re);
    }
  }
  fi.onchange=function(e){
    var f=e.target.files[0]; if(!f) return;
    var r=new FileReader();
    r.onload=function(ev){ shot=ev.target.result; pv.src=shot; pv.style.display='block';
      v.style.display='none'; stop(); buttons('ok'); };
    r.readAsDataURL(f); fi.value='';
  };
  function start(){
    v.style.display='block';
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
      navigator.mediaDevices.getUserMedia({video:{facingMode:'environment'}})
        .then(function(s){ camStream=s; v.srcObject=s; buttons('live'); })
        .catch(function(){ v.style.display='none'; buttons('upload'); });
    } else { v.style.display='none'; buttons('upload'); }
  }
  start();
}

/* ================= home ================= */
function fmtMin(m){ return !m ? '' : (m>=60 ? Math.floor(m/60)+t('c.hr') : m+' '+t('c.min')); }

function addTask(catId,title,min){
  if(!String(title||'').trim()) return;
  S.tasks.push({id:uid++,catId:catId,titleKey:null,title:String(title).trim(),
                min:Number(min)||0,done:false,photo:null});
  save(); renderTasks(); renderStats(); renderDash();
}
function toggleTask(id){
  var task=null;
  S.tasks.forEach(function(x){ if(x.id===id) task=x; });
  if(!task) return;
  if(task.done){
    task.done=false; task.photo=null; addPts(-10);
    S.stats.tasksDone=Math.max(0,(S.stats.tasksDone||0)-1);
    save(); renderTasks(); renderStats(); renderDash(); return;
  }
  openCam(label(task), function(photo){
    task.photo=photo; task.done=true; addPts(10);
    S.stats.tasksDone=(S.stats.tasksDone||0)+1;
    markActiveToday();
    toast(praise()); save(); tip('task.done');
    renderTasks(); renderStats(); renderDash(); checkAchievements();
  });
}
function delTask(id){
  S.tasks=S.tasks.filter(function(x){ return x.id!==id; });
  save(); renderTasks(); renderStats(); renderDash();
}

function renderRing(){
  var svg=document.getElementById('rSvg');
  var r=54, cx=66, cy=66, sw=10, circ=2*Math.PI*r;
  var track=cssVar('--ink-3')||'#333947', fill=cssVar('--acc')||'#3DDCA8';
  var total=S.tasks.length;
  if(!total){
    svg.innerHTML='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="'+track+'" stroke-width="'+sw+'" stroke-dasharray="3 7"/>';
    document.getElementById('rPct').textContent='0%'; return;
  }
  var out='', off=0;
  CATS.forEach(function(cat){
    var ct=S.tasks.filter(function(x){ return x.catId===cat.id; });
    if(!ct.length) return;
    var done=ct.filter(function(x){ return x.done; }).length;
    var seg=(ct.length/total)*circ, filled=seg*(done/ct.length);
    out+='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="'+track+'" stroke-width="'+sw+'" stroke-dasharray="'+(seg-2)+' '+(circ-seg+2)+'" stroke-dashoffset="'+(-off)+'"/>';
    if(filled>0)
      out+='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="'+fill+'" stroke-width="'+sw+'" stroke-linecap="round" stroke-dasharray="'+Math.max(0,filled-2)+' '+(circ-filled+2)+'" stroke-dashoffset="'+(-off)+'"/>';
    off+=seg;
  });
  svg.innerHTML=out;
  var d=S.tasks.filter(function(x){ return x.done; }).length;
  document.getElementById('rPct').textContent=Math.round(d/total*100)+'%';
}

function renderCats(){
  var grid=document.getElementById('catGrid'); grid.innerHTML='';
  CATS.forEach(function(cat){
    var ct=S.tasks.filter(function(x){ return x.catId===cat.id; });
    var done=ct.filter(function(x){ return x.done; }).length;
    var card=document.createElement('div'); card.className='cat';

    var rows = ct.length ? ct.map(function(x){
      return '<div class="task">'+
        '<input type="checkbox" class="cb" data-id="'+x.id+'"'+(x.done?' checked':'')+'>'+
        (x.photo?'<img class="thumb" src="'+x.photo+'" alt="">':'')+
        '<div class="body"><div class="ttl'+(x.done?' done':'')+'">'+esc(label(x))+'</div>'+
        '<div class="meta">'+(x.photo?ic('camera')+'<span>'+esc(t('c.proof'))+'</span>':'')+
        (x.min?ic('clock')+'<span>'+esc(fmtMin(x.min))+'</span>':'')+'</div></div>'+
        (x.min?'<button class="tmr" data-tid="'+x.id+'" data-min="'+x.min+'" aria-label="'+esc(t('c.timer'))+'">'+ic('play')+'</button>':'')+
        '<button class="icon-btn" data-del="'+x.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button>'+
        '</div>';
    }).join('') : '<div class="empty">'+esc(t('h.empty'))+'</div>';

    var sugs=(cat.sg||['sg.generic']).map(function(k){
      return '<button class="sug" data-cat="'+cat.id+'" data-sug="'+esc(t(k))+'">'+esc(t(k))+'</button>';
    }).join('');

    card.innerHTML=
      '<div class="cathead"><div class="nm">'+ic(cat.icon)+'<span>'+esc(catName(cat))+'</span></div>'+
      '<div class="ct numf"><b>'+done+'</b>/'+ct.length+'</div></div>'+
      rows+
      '<div class="sugs">'+sugs+'</div>'+
      '<div class="addrow"><input type="text" class="nt" data-cat="'+cat.id+'" placeholder="'+esc(t('h.add.ph'))+'">'+
      '<input type="number" class="ntmin" data-cat="'+cat.id+'" min="0" placeholder="'+esc(t('h.add.min'))+'">'+
      '<button class="btn btn-primary" data-add="'+cat.id+'">'+ic('plus')+'</button></div>';
    grid.appendChild(card);
  });

  grid.querySelectorAll('.cb').forEach(function(cb){
    cb.addEventListener('change',function(e){ toggleTask(Number(e.target.dataset.id)); });
  });
  grid.querySelectorAll('[data-del]').forEach(function(b){
    b.addEventListener('click',function(){ delTask(Number(b.dataset.del)); });
  });
  grid.querySelectorAll('[data-add]').forEach(function(b){
    b.addEventListener('click',function(){
      var c=b.dataset.add;
      addTask(c, grid.querySelector('.nt[data-cat="'+c+'"]').value,
                 grid.querySelector('.ntmin[data-cat="'+c+'"]').value);
    });
  });
  grid.querySelectorAll('.nt').forEach(function(inp){
    inp.addEventListener('keydown',function(e){
      if(e.key!=='Enter') return;
      var c=inp.dataset.cat;
      addTask(c, inp.value, grid.querySelector('.ntmin[data-cat="'+c+'"]').value);
    });
  });
  grid.querySelectorAll('.sug').forEach(function(b){
    b.addEventListener('click',function(){ addTask(b.dataset.cat,b.dataset.sug,0); });
  });
  grid.querySelectorAll('.tmr').forEach(function(b){
    b.addEventListener('click',function(){ startTimer(b,Number(b.dataset.min)); });
  });
}

var timers={};
function startTimer(btn,minutes){
  var id=btn.dataset.tid;
  if(timers[id]){ clearInterval(timers[id]); delete timers[id];
    btn.classList.remove('run'); btn.innerHTML=ic('play'); return; }
  var left=minutes*60;
  btn.classList.add('run');
  timers[id]=setInterval(function(){
    left--;
    btn.textContent=Math.floor(left/60)+':'+String(left%60).padStart(2,'0');
    if(left<=0){
      clearInterval(timers[id]); delete timers[id];
      btn.classList.remove('run'); btn.innerHTML=ic('play'); toast(t('t.timerdone'));
    }
  },1000);
}

/* ================= goals ================= */
/* The point of this screen is the ladder: a goal is only real once it says
   what it means this week, what it means today, and what you do right now. */
function goalById(id){
  var g=null;
  (S.goals||[]).forEach(function(x){ if(x.id===id) g=x; });
  return g;
}
function goalPct(g){
  if(!g.actions.length) return 0;
  var done=g.actions.filter(function(a){ return a.done; }).length;
  return Math.round(done/g.actions.length*100);
}
/* A finished target is kept, not deleted: it is the evidence the app exists to
   produce. It folds down to one line and can be reopened. */
function archivedCard(g){
  var card=document.createElement('article'); card.className='goal archived';
  card.innerHTML='<h3>'+ic('check')+'<span>'+esc(g.title)+'</span>'+
    '<button class="icon-btn" data-dg="'+g.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('trash')+'</button></h3>'+
    '<span class="gstate done">'+ic('check')+esc(t('gc.done',{d:fmtDay(g.doneAt)}))+'</span>'+
    '<div class="gtools"><button class="btn btn-ghost btn-sm" data-gback="'+g.id+'">'+ic('refresh')+
      '<span>'+esc(t('gc.reopen'))+'</span></button></div>';
  return card;
}
function renderGoals(){
  renderGoalExtras();
  var box=document.getElementById('goalsCont'); box.innerHTML='';
  if(!S.goals.length){
    box.innerHTML='<div class="empty-state">'+ic('target')+
      '<p>'+esc(t('n.empty.goals'))+'</p></div>';
    return;
  }
  /* live targets first, finished ones folded to the bottom */
  var ordered=S.goals.slice().sort(function(a,b){ return (a.archived?1:0)-(b.archived?1:0); });
  ordered.forEach(function(g){
    if(g.archived){ box.appendChild(archivedCard(g)); return; }
    var done=g.actions.filter(function(a){ return a.done; }).length;
    var pct=goalPct(g);
    var started=!!g.started && !g.paused;
    var card=document.createElement('article');
    card.className='goal'+(started?'':' unstarted')+(g.paused?' paused':'');
    /* Until "start the target" is pressed the card is a written target and
       nothing else: no percentage, no counter, no bar. */
    var state = g.paused
      ? '<span class="gstate off">'+ic('clock')+esc(t('gc.paused'))+'</span>'
      : started
      ? '<span class="gstate on">'+ic('play')+esc(t('gc.started',{d:fmtDay(g.startedAt)}))+'</span>'
      : '<span class="gstate">'+ic('clock')+esc(t('gc.notstarted'))+'</span>';
    if(g.freq) state+='<span class="gstate gfreq">'+ic('calendar')+esc(t('gf.'+g.freq))+'</span>';
    if(goalEditId===g.id){
      card.innerHTML='<h3>'+ic('target')+'<span>'+esc(t('ge.btn'))+'</span></h3>'+goalEditForm(g);
      box.appendChild(card); bindGoalEdit(card,g);
      return;
    }
    card.innerHTML=
      '<h3>'+ic('target')+'<span>'+esc(g.title)+'</span>'+
      '<button class="icon-btn" data-ge-open="'+g.id+'" aria-label="'+esc(t('ge.btn'))+'">'+ic('edit')+'</button>'+
      '<button class="icon-btn" data-dg="'+g.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('trash')+'</button></h3>'+
      (g.why ? '<p class="gwhy">'+ic('compass')+'<span><b>'+esc(t('why.lab'))+'</b> '+esc(g.why)+'</span></p>'
             : '<button type="button" class="btn btn-quiet btn-sm gwhy-add" data-ge-open="'+g.id+'">'+ic('compass')+'<span>'+esc(t('why.q'))+'</span></button>')+
      state+

      '<div class="ladder">'+
        '<div class="rung"><span class="rung-k">'+esc(t('gl.week'))+'</span>'+
          '<input type="text" class="rung-in" data-lad="week" data-gid="'+g.id+'" '+
          'value="'+esc(g.week||'')+'" placeholder="'+esc(t('gl.wk.ph'))+'" aria-label="'+esc(t('gl.week'))+'"></div>'+
        '<div class="rung"><span class="rung-k">'+esc(t('gl.today'))+'</span>'+
          '<input type="text" class="rung-in" data-lad="today" data-gid="'+g.id+'" '+
          'value="'+esc(g.today||'')+'" placeholder="'+esc(t('gl.td.ph'))+'" aria-label="'+esc(t('gl.today'))+'"></div>'+
        '<div class="rung now"><span class="rung-k">'+esc(t('gl.now'))+'</span>'+
          (g.now?'<span class="rung-v">'+esc(g.now)+'</span>':'')+
          (started
            ? '<button class="btn btn-primary btn-sm" data-gnow="'+g.id+'">'+ic('play')+'<span>'+esc(t('gl.now.btn'))+'</span></button>'
            : '<button class="btn btn-primary btn-sm" data-gstart="'+g.id+'">'+ic('play')+'<span>'+esc(t('gc.start'))+'</span></button>')+
        '</div>'+
      '</div>'+
      (started||g.paused?'':'<p class="hint gstart-n">'+ic('shield')+'<span>'+esc(t('gc.start.n'))+'</span></p>')+
      (g.started
        ? '<div class="gtools">'+
            '<button class="btn btn-ghost btn-sm" data-gpause="'+g.id+'">'+ic(g.paused?'play':'clock')+
              '<span>'+esc(t(g.paused?'gc.resume':'gc.pause'))+'</span></button>'+
            '<button class="btn btn-ghost btn-sm" data-gdone="'+g.id+'">'+ic('check')+
              '<span>'+esc(t('gc.finish'))+'</span></button>'+
            '<button class="btn btn-ghost btn-sm" data-gcal="'+g.id+'">'+ic('calendar')+
              '<span>'+esc(t('cal.add'))+'</span>'+(isPro()?'':ic('lock','mini'))+'</button>'+
          '</div>'
        : '')+

      '<div class="acts-h">'+esc(t('gl.steps'))+'</div>'+
      '<div class="acts">'+g.actions.map(function(a){
        return '<label><input type="checkbox" class="cb" data-gid="'+g.id+'" data-aid="'+a.id+'"'+
          (a.done?' checked':'')+'><span'+(a.done?' class="done"':'')+'>'+esc(actLabel(a))+'</span></label>';
      }).join('')+'</div>'+
      '<div class="addrow"><input type="text" class="na" data-gid="'+g.id+'" placeholder="'+esc(t('g.step.ph'))+'" aria-label="'+esc(t('g.step.ph'))+'">'+
      '<button class="btn btn-ghost" data-na="'+g.id+'" aria-label="'+esc(t('c.add'))+'">'+ic('plus')+'</button></div>'+
      resHtml(g)+
      (started
        ? '<div class="gmeta"><span class="numf">'+done+'/'+g.actions.length+'</span><span class="numf">'+pct+'%</span></div>'+
          '<div class="gbar"><i style="width:'+pct+'%"></i></div>'
        : '');
    box.appendChild(card);
  });
  box.querySelectorAll('[data-gstart]').forEach(function(b){
    b.addEventListener('click',function(){ startGoal(goalById(Number(b.dataset.gstart))); });
  });
  bindRes(box, renderGoals);
  box.querySelectorAll('[data-ge-open]').forEach(function(b){
    b.addEventListener('click',function(){ goalEditId=Number(b.dataset.geOpen); renderGoals(); });
  });
  box.querySelectorAll('[data-gpause]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.gpause)); if(!g) return;
      g.paused=!g.paused; save(); renderGoals(); renderDash();
      toast(t(g.paused?'t.gpaused':'t.gresumed'));
    });
  });
  box.querySelectorAll('[data-gdone]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.gdone)); if(!g) return;
      g.archived=true; g.doneAt=dayKey();
      S.stats.challenges=(S.stats.challenges||0)+1;
      markActiveToday(); save(); renderGoals(); renderDash(); checkAchievements();
      toast(t('t.gdone')); tip('goal.done');
    });
  });
  box.querySelectorAll('[data-gcal]').forEach(function(b){
    b.addEventListener('click',function(){
      if(!isPro()){ openPlans(); return; }
      var g=goalById(Number(b.dataset.gcal)); if(g) downloadICS(g);
    });
  });
  box.querySelectorAll('[data-gback]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.gback)); if(!g) return;
      if(goalLimitReached()){ openPlans(); return; }
      g.archived=false; g.doneAt=null; save(); renderGoals(); renderDash();
    });
  });

  box.querySelectorAll('.cb').forEach(function(cb){
    cb.addEventListener('change',function(e){
      var g=goalById(Number(e.target.dataset.gid)), a=null;
      if(!g) return;
      g.actions.forEach(function(x){ if(x.id===Number(e.target.dataset.aid)) a=x; });
      if(!a) return;
      a.done=e.target.checked;
      if(g.started){
        addPts(a.done?12:-12);
        if(a.done){ toast(t('t.step')); markActiveToday(); }
        if(a.done && goalPct(g)===100) tip('goal.done');
      }
      save(); renderGoals(); renderStats(); renderDash(); checkAchievements();
    });
  });
  box.querySelectorAll('[data-dg]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.dg));
      if(g && confirm(t('ge.del.q',{g:g.title}))) deleteGoal(g.id);
    });
  });
  box.querySelectorAll('[data-na]').forEach(function(b){
    b.addEventListener('click',function(){
      var gid=Number(b.dataset.na), g=goalById(gid);
      if(!g) return;
      var inp=box.querySelector('.na[data-gid="'+gid+'"]'), v=inp.value.trim();
      if(!v) return;
      g.actions.push({id:uid++,key:null,text:v,done:false});
      inp.value=''; save(); renderGoals();
    });
  });
  /* The ladder inputs save on blur rather than on every keystroke: a full
     re-render mid-typing would steal the caret. */
  box.querySelectorAll('.rung-in').forEach(function(inp){
    inp.addEventListener('change',function(){
      var g=goalById(Number(inp.dataset.gid));
      if(!g) return;
      g[inp.dataset.lad]=inp.value.trim();
      save(); renderDash(); toast(t('gl.saved'));
    });
  });
  box.querySelectorAll('[data-gnow]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.gnow));
      if(!g) return;
      startFiveMinutes(g.today || g.week || g.title);
    });
  });
}
document.getElementById('aGoalBtn').addEventListener('click',addGoalFromInput);
document.getElementById('nGoalIn').addEventListener('keydown',function(e){
  if(e.key==='Enter'){ e.preventDefault(); addGoalFromInput(); }
});
function addGoalFromInput(){
  var inp=document.getElementById('nGoalIn'), v=inp.value.trim();
  if(!v){ toast(t('t.writegoal')); return; }
  if(goalLimitReached()){ toast(t('pro.goalmax',{n:GOAL_FREE_MAX})); openPlans(); return; }
  S.goals.unshift(newGoal(v));
  inp.value=''; save(); renderGoals(); renderDash(); checkAchievements();
  toast(t('t.goaladded')); tip('goal.new');
}
document.getElementById('newGoalBtn').addEventListener('click',function(){
  if(goalLimitReached()){ toast(t('pro.goalmax',{n:GOAL_FREE_MAX})); openPlans(); return; }
  resetChain();
  var host=document.getElementById('goalChain'); host.hidden=false;
  document.getElementById('newGoalBtn').hidden=true;
  renderChain('goalChain');
  host.scrollIntoView({block:'start',behavior:'smooth'});
});
function fmtDay(k){
  if(!k) return '';
  try{ return new Date(k+'T00:00:00').toLocaleDateString(cur,{day:'numeric',month:'short'}); }catch(e){ return k; }
}

/* ================= week ================= */
function dayNames(){
  var base=new Date(2024,0,7); // a Sunday
  var out=[];
  for(var i=0;i<7;i++){
    var d=new Date(base); d.setDate(base.getDate()+i);
    out.push(d.toLocaleDateString(cur,{weekday:'short'}));
  }
  return out;
}
function missionState(m){
  var c=m.days.filter(Boolean).length;
  if(m.target>0 && c>=m.target) return {txt:t('w.st.win'), cls:'win', met:true};
  if(c>0 && c>=Math.ceil(m.target/2)) return {txt:t('w.st.close'), cls:'mid', met:false};
  if(c>0) return {txt:t('w.st.going'), cls:'mid', met:false};
  return {txt:t('w.st.none'), cls:'none', met:false};
}
function renderWeek(){
  var days=dayNames(), today=new Date().getDay();
  document.getElementById('wHead').innerHTML=
    '<th class="mcol">'+esc(t('w.col.mission'))+'</th>'+
    days.map(function(d,i){ return '<th'+(i===today?' class="today"':'')+'>'+esc(d)+'</th>'; }).join('')+
    '<th>'+esc(t('w.col.status'))+'</th>';

  var body=document.getElementById('wBody'); body.innerHTML='';
  var met=0;
  S.missions.forEach(function(m){
    var cat=catById(m.catId)||{icon:'star'};
    var st=missionState(m); if(st.met) met++;
    var count=m.days.filter(Boolean).length;
    var tr=document.createElement('tr');
    var html='<td class="mcol"><div class="mrow">'+ic(cat.icon)+
      '<div><div class="mt">'+esc(label(m))+'</div>'+
      '<div class="mm">'+esc(t('w.target'))+' <span class="numf">'+count+'/'+m.target+'</span></div></div>'+
      '<button class="icon-btn" data-dm="'+m.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></div></td>';
    m.days.forEach(function(on,di){
      html+='<td class="dcell'+(on?' on':'')+'" data-mid="'+m.id+'" data-day="'+di+'">'+
            '<span class="mk">'+ic('check')+'</span></td>';
    });
    html+='<td class="scell '+st.cls+'">'+esc(st.txt)+'</td>';
    tr.innerHTML=html; body.appendChild(tr);
  });
  if(!S.missions.length)
    body.innerHTML='<tr><td colspan="9" class="empty" style="padding:var(--s4)">'+esc(t('w.empty'))+'</td></tr>';

  document.getElementById('wMet').textContent=met;
  document.getElementById('wTot').textContent=S.missions.length;

  body.querySelectorAll('.dcell').forEach(function(cell){
    cell.addEventListener('click',function(){
      var m=null;
      S.missions.forEach(function(x){ if(x.id===Number(cell.dataset.mid)) m=x; });
      if(!m) return;
      var d=Number(cell.dataset.day);
      m.days[d]=!m.days[d];
      addPts(m.days[d]?6:-6);
      if(m.days[d]){ toast(praise()); markActiveToday(); }
      save(); renderWeek(); renderStats(); renderDash(); checkAchievements();
    });
  });
  body.querySelectorAll('[data-dm]').forEach(function(b){
    b.addEventListener('click',function(){
      S.missions=S.missions.filter(function(m){ return m.id!==Number(b.dataset.dm); });
      save(); renderWeek();
    });
  });
}
function fillMissionCats(){
  document.getElementById('nMisCat').innerHTML=
    CATS.map(function(c){ return '<option value="'+c.id+'">'+esc(catName(c))+'</option>'; }).join('');
}
document.getElementById('aMisBtn').addEventListener('click',function(){
  var inp=document.getElementById('nMis'), v=inp.value.trim();
  if(!v) return;
  S.missions.push({id:uid++, catId:document.getElementById('nMisCat').value, titleKey:null, title:v,
    target:Math.min(7,Math.max(1,Number(document.getElementById('nMisT').value)||3)),
    days:[false,false,false,false,false,false,false]});
  inp.value=''; save(); renderWeek();
});
document.getElementById('rvBtn').addEventListener('click',function(){
  var met=0;
  S.missions.forEach(function(m){ if(missionState(m).met) met++; });
  var total=S.missions.length, reward=met*50;
  addPts(reward); save(); renderStats();
  var msg = total && met===total ? t('w.rev.perfect')
          : met>=total/2 && met>0 ? t('w.rev.strong') : t('w.rev.start');
  var out=document.getElementById('rvRes');
  out.innerHTML='<div class="big numf">'+met+'/'+total+'</div>'+
    '<div class="msg">'+esc(msg)+'</div>'+
    '<div class="pts">'+esc(t('t.pts',{n:reward}))+'</div>';
  out.classList.add('on');
});
document.getElementById('rWkBtn').addEventListener('click',function(){
  S.missions.forEach(function(m){ m.days=[false,false,false,false,false,false,false]; });
  document.getElementById('rvRes').classList.remove('on');
  save(); renderWeek(); toast(t('t.newweek'));
});

/* ================= body plans ================= */
function renderPlan(gridId,blocks,prefix){
  var grid=document.getElementById(gridId); grid.innerHTML='';
  blocks.forEach(function(block,bi){
    var card=document.createElement('div'); card.className='pcard';
    var title = block.k ? t(block.k) : block.label;
    var items=block.items.map(function(item,ii){
      var key=prefix+'-'+bi+'-'+ii;
      var checked=S.plan[key]?' checked':'';
      var name = item.k ? t(item.k) : item.n;
      var cam  = item.k ? false : !!item.cam;   // workout items are not photo-gated
      var meta = item.r ? '<span class="pr">'+ic('clock')+esc(item.r)+'</span>'
               : cam    ? '<span class="pr">'+ic('camera')+'</span>' : '';
      return '<div class="pitem">'+
        '<input type="checkbox" class="cb" data-key="'+key+'" data-cam="'+(cam?1:0)+'" data-name="'+esc(name)+'"'+checked+'>'+
        '<div class="pb"><span class="px'+(checked?' done':'')+'">'+esc(name)+'</span>'+
        (item.d?'<div class="pd">'+esc(item.d)+'</div>':'')+'</div>'+meta+'</div>';
    }).join('');
    card.innerHTML='<h3><span>'+esc(title)+'</span><span class="dnum">'+t('c.day')+' '+(bi+1)+'</span></h3>'+
      (block.sub?'<div class="psub2">'+esc(block.sub)+'</div>':'')+items;
    grid.appendChild(card);
  });

  grid.querySelectorAll('.cb').forEach(function(cb){
    cb.addEventListener('change',function(e){
      var key=e.target.dataset.key;
      if(e.target.checked){
        if(e.target.dataset.cam==='1'){
          e.target.checked=false;
          openCam(e.target.dataset.name,function(){
            S.plan[key]=true; addPts(8); toast(t('t.proof'));
            save(); renderPlan(gridId,blocks,prefix); renderStats();
          });
        } else {
          S.plan[key]=true; addPts(8); toast(praise()); save(); renderStats();
          var px=e.target.closest('.pitem').querySelector('.px'); if(px) px.classList.add('done');
        }
      } else {
        delete S.plan[key]; addPts(-8); save(); renderStats();
        var px2=e.target.closest('.pitem').querySelector('.px'); if(px2) px2.classList.remove('done');
      }
    });
  });
}

/* ================= why it works ================= */
function renderTheories(){
  var g=document.getElementById('thGrid');
  g.innerHTML=THEORIES.map(function(th,i){
    return '<div class="th"><div class="n">'+String(i+1).padStart(2,'0')+'</div>'+
      ic(th.icon)+
      '<h4>'+esc(t(th.n))+'</h4><div class="au">'+esc(t(th.a))+'</div>'+
      '<div class="pr2">'+esc(t(th.p))+'</div>'+
      '<div class="hw">'+esc(t(th.h))+'</div>'+
      '<dl><dt>'+esc(t('y.where'))+'</dt><dd>'+esc(t(th.f))+'</dd></dl></div>';
  }).join('');
}

/* ================= stats + insight ================= */
function renderStats(){
  renderDashStats(); renderAvatarCard();
  document.getElementById('skV').textContent=shownStreak();
  document.getElementById('ptV').textContent=S.points;
  document.getElementById('dnV').textContent=S.tasks.filter(function(x){return x.done;}).length;
  document.getElementById('tlV').textContent=S.tasks.length;
}
function renderInsight(){
  var ins=pick(INSIGHTS);
  document.getElementById('dIns').innerHTML=
    '<div class="insight">'+ic('sparkles')+'<div>'+
    '<div class="lab">'+esc(t('h.insight'))+'</div>'+
    '<div class="txt">'+esc(t(ins.t))+'</div>'+
    '<div class="src">'+esc(t(ins.s))+'</div></div></div>';
}

/* ================= the dashboard ================= */
/* Deliberately narrow: the next step first, then one quiet line of numbers.
   Big tiles full of zeros told a beginner nothing but "zero". The full task
   list, the avatar and the profile live on their own tabs. */
function renderDashStats(){
  var box=document.getElementById('dashStats');
  if(!box) return;
  var s=stageInfo(), li=levelInfo();
  var cells=[
    {ic:'star',   v:t('a.level')+' '+s.level, k:s.stage},
    {ic:'flame',  v:shownStreak(),            k:t('d.streak')},
    {ic:'target', v:(S.goals||[]).length,     k:t('d.goals')}
  ];
  box.innerHTML='<h2 class="sr">'+esc(t('d.progress'))+'</h2>'+
    '<div class="dstrip-row">'+cells.map(function(c){
      return '<div class="dchip">'+ic(c.ic)+'<b class="numf">'+esc(String(c.v))+'</b>'+
        '<span>'+esc(c.k)+'</span></div>';
    }).join('')+'</div>'+
    '<div class="xp"><i style="width:'+s.progress+'%"></i></div>'+
    '<p class="xp-n">'+esc(t('av.next',{n:li.need, l:li.level+1}))+'</p>';
}

/* ---- the five-minute starter, on the goal card's step ---- */
var fiveTimer=null, fiveLeft=0, fiveGid=null;   // which goal the running five minutes belong to
function clearFive(){
  if(fiveTimer){ clearInterval(fiveTimer); fiveTimer=null; }
}
function startFiveMinutes(labelText){
  clearFive();
  fiveLeft=5*60;
  markActiveToday(); tip('task.skip');
  goPage('home');
  fiveTimer=setInterval(function(){
    fiveLeft--;
    var el=document.getElementById('fiveTxt');
    if(el){
      var m=Math.floor(fiveLeft/60), sec=String(fiveLeft%60).padStart(2,'0');
      el.textContent=t('d.running',{t:m+':'+sec});
    }
    if(fiveLeft<=0){ clearFive(); toast(t('d.timeup')); renderToday3(); }
  },1000);
  renderToday3();   // after the timer exists, so the row shows the countdown
}

/* ---- asked once on Home if it was never answered ----
   Accounts made before the question was required still read "מתחיל/ה".
   One tap answers it, and the card does not come back. */
function renderGenderAsk(){
  var box=document.getElementById('gndBox'); if(!box) return;
  box.hidden = GENDERS.indexOf(P.gender)>=0;
  if(box.dataset.bound) return;
  box.dataset.bound='1';
  box.querySelectorAll('[data-hgnd]').forEach(function(o){
    o.addEventListener('click',function(){ setGender(o.dataset.hgnd); save(); box.hidden=true; toast(t('gl.saved')); });
  });
}

/* ---- my day: the same small ritual for everyone, every morning ----
   Three things that matter today, written by the user, before the
   personal step. A new day starts with three empty lines. */
/* The day is chosen, not handed out: picked holds the goals chosen for
   today, items the one-off things (an idea or the user's own words). A goal
   that already has today's step or was done today counts as chosen, which
   also carries over a day started before this existed. Empty lines from the
   old three fixed slots are dropped. */
var T3_MAX=5;
function today3(){
  var d=dayKey();
  if(!S.today3 || S.today3.day!==d) S.today3={day:d, items:[], picked:[]};
  var td=S.today3;
  td.items=td.items.filter(function(x){ return x.t && x.t.trim(); });
  if(!td.picked) td.picked=[];
  (S.goals||[]).forEach(function(g){
    if(!g.archived && td.picked.indexOf(g.id)<0 && ((g.day && g.day.d===d) || g.doneDay===d)) td.picked.push(g.id);
  });
  return td;
}
function pickedGoals(){
  var td=today3(); return liveGoals().filter(function(g){ return td.picked.indexOf(g.id)>=0; });
}
function addDayItem(text){
  var td=today3(); text=String(text||'').trim(); if(!text) return false;
  if(td.items.length>=T3_MAX){ toast(t('t3.full')); return false; }
  if(td.items.some(function(x){ return normLine(x.t)===normLine(text); })) return true;
  td.items.push({t:text, done:false, paid:false, gid:null}); logDay(); save(); return true;
}
/* In the order they were made, so a new goal joins the list under the
   others instead of pushing the first one down. */
/* Ideas for the three lines, in this order: today's step of each goal
   (already linked to it), then what trains the area the check-in found
   weakest, then everyday things for the user's age. Lines already written
   are left out, and without a check-in a one-minute one is offered. */
function t3Ideas(td){
  var used={}; td.items.forEach(function(x){ used[normLine(x.t)]=1; });
  var out=[];
  function add(text,cat){ if(!text || used[normLine(text)] || out.length>=6) return; used[normLine(text)]=1; out.push({t:text,cat:cat||null}); }
  /* first, a day's step from the categories this user keeps choosing */
  var have={}; (S.goals||[]).forEach(function(g){ if(g.rg) have[g.rg]=1; });
  topCats().slice(0,2).forEach(function(c){
    var rs=READY_GOALS.filter(function(r){ return r[3]===c && readyFits(r) && !have[r[0]]; });
    if(rs.length){ var r=rs[(new Date().getDate())%rs.length]; add(t('rg.'+r[0]+'.d'),c); }
  });
  if(hasProfile()) [1,2].forEach(function(n){ add(t('sq.'+weakDim()+'.'+n)); });
  var band=P.age ? ageBand(P.age) : 'a13';
  [1,2,3,4,5,6].forEach(function(n){ add(t('sq.'+band+'.'+n)); });
  return out;
}
function liveGoals(){
  return (S.goals||[]).filter(function(g){ return !g.archived; }).sort(function(a,b){ return a.id-b.id; });
}
/* The day's record, rewritten on every change so the last state of a day is
   what stays: the three lines (text, done, which goal they serve) and which
   goals' own step was done. That is what My week reads. */
var LOG_DAYS=120;
function logDay(){
  var td=today3();
  if(!S.log) S.log={};
  var prev=S.log[td.day]||{};
  S.log[td.day]={
    note: prev.note||'', feel: prev.feel||'', choice: prev.choice||'',
    items: td.items.filter(function(x){ return x.t.trim(); })
             .map(function(x){ return {t:x.t.trim(), done:!!x.done, gid:x.gid||null, url:x.url||null}; }),
    steps: (S.goals||[]).filter(function(g){ return g.doneDay===td.day; }).map(function(g){ return g.id; }),
    st: {},   // the text of each step that was done, so My week can show it
    rest: (S.goals||[]).filter(function(g){ return g.restDay===td.day; }).map(function(g){ return g.id; })
  };
  (S.goals||[]).forEach(function(g){ if(g.doneDay===td.day && dayStep(g)) S.log[td.day].st[g.id]=dayStep(g); });
  var days=Object.keys(S.log).sort();
  while(days.length>LOG_DAYS) delete S.log[days.shift()];
}
var t3Tab=null, t3IdeasMore=false;
function renderToday3(){
  var box=document.getElementById('todayBox'); if(!box) return;
  var td=today3(), all=liveGoals(), goals=pickedGoals(), today=dayKey(), running=!!fiveTimer;
  var total=goals.length+td.items.length;
  var nDone=td.items.filter(function(x){ return x.done; }).length + goals.filter(function(g){ return g.doneDay===today; }).length;
  /* the picker, in order of weight: my goals as full rows, then three
     ideas (more on request), then a line in my own words */
  var ideas=t3Ideas(td), shown=t3IdeasMore ? ideas : ideas.slice(0,3);
  function optRow(attrs, icon, text, on, cls){
    return '<button type="button" class="t3opt'+(cls?' '+cls:'')+(on?' on':'')+'" '+attrs+'>'+
      '<span class="t3opt-i">'+ic(icon)+'</span><span class="t3opt-t">'+esc(text)+'</span>'+
      '<span class="t3opt-a">'+ic(on?'check':'plus')+'</span></button>';
  }
  var picker=
    '<div class="mg-lab">'+esc(t(all.length?'t3.pick.goals':'t3.pick.sug'))+'</div>'+
    '<div class="t3list">'+(all.length
      ? all.map(function(g){
          var on=td.picked.indexOf(g.id)>=0, locked=g.doneDay===today;
          return optRow('data-t3pick="'+g.id+'" aria-pressed="'+on+'"'+(locked?' disabled':''),'target',g.title,on,'goal');
        }).join('')
      : readyGoals('for').slice(0,3).map(function(r){ return optRow('data-t3ready="'+r[0]+'"','target',t('rg.'+r[0]+'.t'),false,'goal'); }).join('')
    )+'</div>'+
    (all.length ? '' : '<button type="button" class="btn btn-quiet btn-sm t3nogoal" data-goto-goals>'+ic('plus')+'<span>'+esc(t('t3.nogoal'))+'</span></button>')+
    (shown.length && td.items.length<T3_MAX
      ? '<div class="mg-lab t3lab2">'+esc(t('sq.t'))+'</div><div class="t3list">'+shown.map(function(x){
          return optRow('data-idea="'+esc(x.t)+'"'+(x.cat?' data-cat="'+x.cat+'"':''),'sparkles',x.t,false,'idea'); }).join('')+'</div>'+
        (!t3IdeasMore && ideas.length>3 ? '<button type="button" class="btn btn-quiet btn-sm t3moreideas" data-t3more>'+esc(t('t3.moreideas'))+'</button>' : '')
      : '')+
    (td.items.length<T3_MAX ? '<div class="addrow t3own"><input type="text" id="t3Own" maxlength="80" placeholder="'+esc(t('t3.other.ph'))+'" aria-label="'+esc(t('t3.other.ph'))+'">'+
        '<button class="btn btn-ghost" id="t3OwnAdd" aria-label="'+esc(t('c.add'))+'">'+ic('plus')+'</button></div>' : '')+
    (hasProfile() ? '' : '<button type="button" class="btn btn-quiet btn-sm t3quiz" data-goquiz>'+ic('sparkles')+'<span>'+esc(t('sq.quiz'))+'</span></button>');
  /* what was chosen: a row per goal (its step chosen in place, then ticked), then the one-off things */
  var gRows=goals.map(function(g){
    var step=dayStep(g), done=g.doneDay===today, vid=firstVideo(g);
    if(!step) return '<div class="t3g ask"><div class="t3g-name">'+ic('target')+'<b>'+esc(g.title)+'</b></div>'+
      (g.why ? '<p class="t3g-why">'+ic('compass')+'<span>'+esc(t('why.lab'))+' '+esc(g.why)+'</span></p>' : '')+
      '<div class="addrow"><input type="text" data-mg-step-in="'+g.id+'" maxlength="100" placeholder="'+esc(t('mg.ask'))+'" aria-label="'+esc(t('mg.ask'))+'">'+
        '<button class="btn btn-primary" data-mg-step-set="'+g.id+'">'+esc(t('c.save'))+'</button></div>'+
      (stepChoices(g).length ? '<div class="mg-picks">'+stepChoices(g).map(function(x){
          return '<button type="button" class="t3idea" data-mg-step-pick="'+g.id+'" data-text="'+esc(x)+'">'+ic('plus')+'<span>'+esc(x)+'</span></button>';
        }).join('')+'</div>' : '')+
      /* materials can be looked for before the step is chosen, too */
      '<button type="button" class="btn btn-quiet btn-sm t3srch" data-srch-g="'+g.id+'">'+ic('globe')+'<span>'+esc(t('srch.t'))+
        ((g.res||[]).length ? ' · '+g.res.length : '')+'</span></button></div>';
    return '<div class="t3row t3g'+(done?' done':'')+'">'+
      '<button type="button" class="t3chk" data-gstep-done="'+g.id+'" aria-pressed="'+done+'" aria-label="'+esc(t('t3.mark'))+'">'+ic('check')+'</button>'+
      '<div class="t3g-body"><div class="t3g-goal">'+ic('target')+'<span>'+esc(g.title)+'</span></div><div class="t3g-step">'+esc(step)+'</div>'+
        (fiveGid===g.id && running ? '<div class="t3g-run" id="fiveTxt">'+esc(t('d.running',{t:'5:00'}))+'</div>' : '')+'</div>'+
      (done ? '' :
        (vid ? '<button type="button" class="t3act" data-mg-vid="'+g.id+'" aria-label="'+esc(t('res.video'))+'" title="'+esc(t('res.video'))+'">'+ic('play')+'</button>'
             : '<button type="button" class="t3act" data-mg-five="'+g.id+'"'+(running?' disabled':'')+' aria-label="'+esc(t('d.start5'))+'" title="'+esc(t('d.start5'))+'">'+ic('clock')+'</button>')+
        '<button type="button" class="t3act" data-mg-step-clear="'+g.id+'" aria-label="'+esc(t('mg.change'))+'" title="'+esc(t('mg.change'))+'">'+ic('refresh')+'</button>'+
        '<button type="button" class="t3act" data-srch-g="'+g.id+'" aria-label="'+esc(t('srch.t'))+'" title="'+esc(t('srch.t'))+'">'+ic('globe')+'</button>')+
      '</div>';
  }).join('');
  var iRows=td.items.map(function(it,i){
    return '<div class="t3row'+(it.done?' done':'')+'">'+
      '<button type="button" class="t3chk" data-t3="'+i+'" aria-pressed="'+(it.done?'true':'false')+'" aria-label="'+esc(t('t3.mark'))+'">'+ic('check')+'</button>'+
      '<input type="text" maxlength="80" data-t3in="'+i+'" value="'+esc(it.t)+'" aria-label="'+esc(it.t)+'">'+
      (it.url ? '<a class="t3act" href="'+esc(it.url)+'" target="_blank" rel="noopener" aria-label="'+esc(t('srch.open'))+'" title="'+esc(t('srch.open'))+'">'+ic('link')+'</a>' : '')+
      (it.done ? '' : '<button type="button" class="t3act" data-srch-i="'+i+'" aria-label="'+esc(t('srch.t'))+'" title="'+esc(t('srch.t'))+'">'+ic('globe')+'</button>'+
        '<button type="button" class="t3act" data-t3del="'+i+'" aria-label="'+esc(t('c.delete'))+'" title="'+esc(t('c.delete'))+'">'+ic('x')+'</button>')+
      '</div>';
  }).join('');
  /* two panes: today's list and choosing. On a phone a switch shows one at
     a time (choosing first, until something is chosen); on a wide screen
     they stand side by side and the switch is hidden. */
  var nBlank=td.items.length>=T3_MAX ? 0 : Math.min(T3_MAX-td.items.length, Math.max(1, 3-td.items.length));
  var blankRows='';
  for(var k=0;k<nBlank;k++){
    var ph=t('t3.ph',{n:td.items.length+k+1});
    blankRows+='<div class="t3row blank"><span class="t3chk" aria-hidden="true">'+ic('check')+'</span>'+
      '<input type="text" maxlength="80" data-t3new="'+k+'" placeholder="'+esc(ph)+'" aria-label="'+esc(ph)+'"></div>';
  }
  var chosen=total>0, tab=t3Tab || 'today';
  box.innerHTML='<div class="boxh-row"><h2 class="boxh">'+ic('sun')+'<span>'+esc(t('t3.t'))+'</span></h2>'+
      (chosen ? '<span class="boxh-n numf">'+nDone+'/'+total+'</span>' : '')+'</div>'+
    '<div class="t3seg" role="tablist">'+
      '<button type="button" role="tab" data-t3tab="today" aria-selected="'+(tab==='today')+'" class="'+(tab==='today'?'on':'')+'">'+ic('check')+
        '<span>'+esc(t('t3.tab.today'))+'</span>'+(total?'<b class="numf">'+total+'</b>':'')+'</button>'+
      '<button type="button" role="tab" data-t3tab="pick" aria-selected="'+(tab==='pick')+'" class="'+(tab==='pick'?'on':'')+'">'+ic('target')+
        '<span>'+esc(t('t3.pick.goals'))+'</span></button>'+
    '</div>'+
    '<div class="t3panes" data-tab="'+tab+'">'+
      '<section class="t3pane today"><h3 class="t3pane-h">'+ic('check')+'<span>'+esc(t('t3.tab.today'))+'</span></h3>'+
        '<p class="t3help">'+esc(t('t3.todo.h'))+'</p>'+
        gRows+iRows+blankRows+
        (goals.length || !all.length ? '' : '<button type="button" class="btn btn-quiet btn-sm t3fromgoals" data-t3tab="pick">'+ic('target')+'<span>'+esc(t('t3.fromgoals'))+'</span></button>')+
      '</section>'+
      '<section class="t3pane pick"><h3 class="t3pane-h">'+ic('target')+'<span>'+esc(t('t3.pick.goals'))+'</span></h3>'+
        '<p class="t3help">'+esc(t('t3.goal.h'))+'</p>'+picker+
      '</section>'+
    '</div>';
  /* a line written in the list joins it; Enter moves on to the next free line */
  box.querySelectorAll('[data-t3new]').forEach(function(inp){
    function add(next){
      var v=inp.value.trim(); if(!v) return;
      if(addDayItem(v)){ markActiveToday(); t3Tab='today'; renderToday3();
        if(next){ var n=box.querySelector('[data-t3new="0"]'); if(n) n.focus(); } }
    }
    inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); add(true); } });
    inp.addEventListener('change',function(){ add(false); });
  });
  box.querySelectorAll('[data-t3tab]').forEach(function(b){
    b.addEventListener('click',function(){ t3Tab=b.dataset.t3tab; renderToday3(); });
  });
  /* choosing several things in a row stays on the choosing pane */
  box.querySelector('.t3pane.pick').addEventListener('click',function(){ if(!t3Tab) t3Tab=tab; },true);
  var mi=box.querySelector('[data-t3more]');
  if(mi) mi.addEventListener('click',function(){ t3IdeasMore=true; renderToday3(); });
  box.querySelectorAll('[data-t3pick]').forEach(function(b){
    b.addEventListener('click',function(){
      var id=Number(b.dataset.t3pick), td=today3(), i=td.picked.indexOf(id), g=goalById(id);
      if(i>=0){ td.picked.splice(i,1); if(g && g.day && g.day.d===dayKey()) g.day=null; if(fiveGid===id) clearFive(); }
      else { td.picked.push(id); markActiveToday(); prefLearn(goalCat(g),1); }
      logDay(); save(); renderToday3();
      if(i<0) toast(t('t3.added'));
    });
  });
  box.querySelectorAll('[data-idea]').forEach(function(b){
    b.addEventListener('click',function(){
      if(addDayItem(b.dataset.idea)){ if(b.dataset.cat) prefLearn(b.dataset.cat,1); markActiveToday(); save(); renderToday3(); }
    });
  });
  box.querySelectorAll('[data-t3ready]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=addReadyGoal(rgById(Number(b.dataset.t3ready))); if(!g) return;
      today3().picked.push(g.id); logDay(); save(); renderToday3();
    });
  });
  var own=box.querySelector('#t3Own');
  if(own){
    var addOwn=function(){ if(!own.value.trim()){ own.focus(); return; } if(addDayItem(own.value)){ markActiveToday(); renderToday3(); } };
    box.querySelector('#t3OwnAdd').addEventListener('click',addOwn);
    own.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); addOwn(); } });
  }
  box.querySelectorAll('[data-t3in]').forEach(function(inp){
    inp.addEventListener('change',function(){
      var it=today3().items[Number(inp.dataset.t3in)];
      if(!inp.value.trim()){ inp.value=it.t; return; }
      it.t=inp.value.trim(); logDay(); save();
    });
  });
  box.querySelectorAll('[data-t3del]').forEach(function(b){
    b.addEventListener('click',function(){ today3().items.splice(Number(b.dataset.t3del),1); logDay(); save(); renderToday3(); });
  });
  box.querySelectorAll('[data-t3]').forEach(function(b){
    b.addEventListener('click',function(){
      var it=today3().items[Number(b.dataset.t3)];
      it.done=!it.done;
      if(it.done){
        markActiveToday();
        if(!it.paid){ it.paid=true; addPts(10); }
        cheerIfAll(t('t.pts',{n:10}));
      }
      logDay(); save(); renderToday3(); renderEvening(); renderDashStats(); checkAchievements();
    });
  });
  /* a goal's step ticked here is the goal's step done: points once a day,
     and it counts in My week */
  box.querySelectorAll('[data-gstep-done]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.gstepDone));
      if(g.doneDay===dayKey()){ g.doneDay=null; logDay(); save(); renderToday3(); return; }
      if(fiveGid===g.id) clearFive();
      g.doneDay=dayKey(); markActiveToday(); prefLearn(goalCat(g),1);
      if(g.paidDay!==dayKey()){
        g.paidDay=dayKey(); addPts(25);
        S.stats.challenges=(S.stats.challenges||0)+1;
      }
      cheerIfAll(t('t3.chose',{n:25}), true);
      logDay(); save(); renderToday3(); renderEvening(); renderDashStats(); renderStats(); checkAchievements();
    });
  });
  box.querySelectorAll('[data-mg-step-set]').forEach(function(b){
    var g=goalById(Number(b.dataset.mgStepSet)), inp=box.querySelector('[data-mg-step-in="'+g.id+'"]');
    function go(){ if(!inp.value.trim()){ inp.focus(); return; } setDayStep(g, inp.value); }
    b.addEventListener('click',go);
    inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); go(); } });
  });
  box.querySelectorAll('[data-mg-step-pick]').forEach(function(b){
    b.addEventListener('click',function(){ setDayStep(goalById(Number(b.dataset.mgStepPick)), b.dataset.text); });
  });
  box.querySelectorAll('[data-mg-step-clear]').forEach(function(b){
    b.addEventListener('click',function(){ var g=goalById(Number(b.dataset.mgStepClear)); g.day=null; save(); renderToday3(); });
  });
  box.querySelectorAll('[data-mg-five]').forEach(function(b){
    b.addEventListener('click',function(){ var g=goalById(Number(b.dataset.mgFive)); fiveGid=g.id; startFiveMinutes(dayStep(g)); });
  });
  box.querySelectorAll('[data-mg-vid]').forEach(function(b){
    b.addEventListener('click',function(){ openRes(firstVideo(goalById(Number(b.dataset.mgVid)))); });
  });
  var ng=box.querySelector('[data-goto-goals]'); if(ng) ng.addEventListener('click',function(){ goPage('goals'); });
  box.querySelectorAll('[data-srch-g]').forEach(function(b){
    b.addEventListener('click',function(){ srchOpen({gid:Number(b.dataset.srchG)}); });
  });
  box.querySelectorAll('[data-srch-i]').forEach(function(b){
    b.addEventListener('click',function(){ srchOpen({item:Number(b.dataset.srchI)}); });
  });
  if(box.querySelector('[data-goquiz]')) bindGoQuiz(box);
}
/* Everything on the day's list done - goal steps and the lines written -
   is the moment for confetti; a goal's step gets it too. */
function cheerIfAll(msg, isGoal){
  var td=today3(), today=dayKey();
  var all=td.items.every(function(x){ return x.done; }) && pickedGoals().every(function(g){ return g.doneDay===today; });
  toast(all ? t('t3.all') : msg);
  if(all || isGoal) celebrate();
}

/* ---- the end of the day: one line about yourself ----
   From five in the evening, or earlier once the day's three things are all
   done, Home asks how the day was: a feeling in one tap and one optional
   line. Both go into the day's record and show up in My week. At the end
   of the week (Friday and Saturday) the same card points to the week's
   reflection until it is written. */
var FEELS=[{k:'energy',e:'⚡'},{k:'calm',e:'🌿'},{k:'proud',e:'🌟'},{k:'tired',e:'🌙'}];
var eveEdit=false;
function weekKey(d){
  d=d?new Date(d):new Date(); d.setDate(d.getDate()-d.getDay());   // the week starts on Sunday
  return dayKey(d);
}
function eveTime(){
  var td=today3(), all=td.items.filter(function(x){ return x.t.trim(); });
  return new Date().getHours()>=17 || (all.length && all.every(function(x){ return x.done; }));
}
function renderEvening(){
  var box=document.getElementById('eveBox'); if(!box) return;
  var wd=new Date().getDay(), weekEnd=(wd===5||wd===6), weekDone=!!(S.weeks&&S.weeks[weekKey()]);
  var showWeek=weekEnd && !weekDone;
  if(!eveTime() && !showWeek){ box.hidden=true; return; }
  box.hidden=false;
  logDay();
  var L=S.log[dayKey()];
  var weekNudge = showWeek
    ? '<div class="eve-week">'+ic('calendar')+'<span>'+esc(t('ev.week'))+'</span>'+
        '<button class="btn btn-ghost btn-sm" data-eve-week>'+esc(t('ev.week.go'))+'</button></div>' : '';
  if(!eveTime()){ box.innerHTML=weekNudge; bindEveWeek(); return; }
  var head='<h2 class="boxh">'+ic('moon')+'<span>'+esc(t('ev.t'))+'</span></h2>';
  if((L.note||L.feel||L.choice) && !eveEdit){
    var f=FEELS.filter(function(x){ return x.k===L.feel; })[0];
    box.innerHTML=head+
      '<p class="eve-saved">'+(f?'<span class="eve-e">'+f.e+'</span>'+esc(t('ev.f.'+f.k)):'')+
        (L.note?(f?' · ':'')+'<q>'+esc(L.note)+'</q>':'')+'</p>'+
      (L.choice?'<p class="eve-choice">'+ic('compass')+'<span>'+esc(L.choice)+'</span></p>':'')+
      '<p class="next-sub">'+esc(t('ev.thanks'))+'</p>'+
      '<button class="btn btn-quiet btn-sm" data-eve-edit>'+ic('edit')+'<span>'+esc(t('ge.btn'))+'</span></button>'+
      weekNudge;
    box.querySelector('[data-eve-edit]').addEventListener('click',function(){ eveEdit=true; renderEvening(); });
    bindEveWeek(); return;
  }
  box.innerHTML=head+'<p class="psub">'+esc(t('ev.s'))+'</p>'+
    '<div class="eve-feels">'+FEELS.map(function(x){
      return '<button type="button" class="opt'+(L.feel===x.k?' on':'')+'" data-feel="'+x.k+'" aria-pressed="'+(L.feel===x.k)+'">'+
        '<span class="eve-e">'+x.e+'</span><span>'+esc(t('ev.f.'+x.k))+'</span></button>';
    }).join('')+'</div>'+
    '<div class="field"><label for="eveNote">'+esc(t('ev.q'))+'</label>'+
      '<input type="text" id="eveNote" maxlength="140" value="'+esc(L.note||'')+'" placeholder="'+esc(t('ev.ph'))+'"></div>'+
    '<div class="field"><label for="eveChoice">'+ic('compass')+'<span>'+esc(t('ev.ch.q'))+'</span></label>'+
      '<input type="text" id="eveChoice" maxlength="140" value="'+esc(L.choice||'')+'" placeholder="'+esc(t('ev.ch.ph'))+'">'+
      '<div class="mg-picks">'+[1,2,3,4,5].map(function(n){ var x=t('evc.'+n);
        return '<button type="button" class="t3idea" data-evc="'+esc(x)+'">'+ic('plus')+'<span>'+esc(x)+'</span></button>'; }).join('')+'</div></div>'+
    '<button class="btn btn-primary btn-sm" data-eve-save>'+ic('check')+'<span>'+esc(t('c.save'))+'</span></button>'+
    weekNudge;
  var pick=L.feel;
  box.querySelectorAll('[data-evc]').forEach(function(b){
    b.addEventListener('click',function(){
      var ci=document.getElementById('eveChoice'); ci.value=b.dataset.evc;
      box.querySelectorAll('[data-evc]').forEach(function(o){ o.classList.toggle('on',o===b); });
    });
  });
  box.querySelectorAll('[data-feel]').forEach(function(b){
    b.addEventListener('click',function(){
      pick = pick===b.dataset.feel ? '' : b.dataset.feel;
      box.querySelectorAll('[data-feel]').forEach(function(o){
        var on=o.dataset.feel===pick; o.classList.toggle('on',on); o.setAttribute('aria-pressed',on); });
    });
  });
  box.querySelector('[data-eve-save]').addEventListener('click',function(){
    var L=S.log[dayKey()];
    L.note=document.getElementById('eveNote').value.trim(); L.feel=pick||'';
    L.choice=document.getElementById('eveChoice').value.trim();
    if(!L.note && !L.feel && !L.choice){ document.getElementById('eveNote').focus(); return; }
    eveEdit=false; markActiveToday(); save(); toast(t('ev.thanks')); renderEvening();
  });
  bindEveWeek();
}
function bindEveWeek(){
  var b=document.querySelector('[data-eve-week]');
  if(b) b.addEventListener('click',function(){
    goPage('progress');
    var r=document.getElementById('weekRefl'); if(r) r.scrollIntoView({block:'start',behavior:'smooth'});
  });
}

/* ---- my week: Sunday to Saturday at a glance ----
   A row of seven days for each goal, with a check where its step was done,
   then the free things and how the days felt. Tapping a day opens what it
   held. Only what happened is counted: an empty day reads as rest, never
   as a zero. The arrows step back through earlier weeks. */
var wkOff=0, wkSel=null;
function weekOf(off){
  var s=new Date(weekKey()+'T00:00:00'), out=[];
  s.setDate(s.getDate()+7*off);
  for(var i=0;i<7;i++){ var x=new Date(s); x.setDate(s.getDate()+i); out.push(dayKey(x)); }
  return out;
}
function normLine(s){ return String(s||'').trim().toLowerCase().replace(/\s+/g,' '); }
function renderMyWeek(){
  var box=document.getElementById('weekBox'); if(!box) return;
  var log=S.log||{}, days=weekOf(wkOff), today=dayKey();
  function has(d){ var L=log[d]; return !!(L && (L.items.some(function(x){ return x.done; }) || L.steps.length || (L.rest||[]).length || L.note || L.feel || L.choice)); }
  var used=days.filter(has);
  if(!wkSel || days.indexOf(wkSel)<0) wkSel = days.indexOf(today)>=0 ? today : (used[used.length-1]||days[0]);
  var older=Object.keys(log).some(function(d){ return d<days[0]; });
  /* live goals, and any goal that was stepped this week and has since been put away */
  var live=liveGoals(), seen={};
  days.forEach(function(d){ ((log[d]||{}).steps||[]).forEach(function(id){ seen[id]=1; }); });
  var goals=live.concat((S.goals||[]).filter(function(g){ return seen[g.id] && live.indexOf(g)<0; }));
  function lang(d,o){ try{ return new Date(d+'T00:00:00').toLocaleDateString(cur,o); }catch(e){ return d; } }
  var steps=0, things=0, feels={}, rep={}, choices=0;
  days.forEach(function(d){
    var L=log[d]; if(!L) return;
    steps+=L.steps.length;
    if(L.choice) choices++;
    if(L.feel) feels[L.feel]=(feels[L.feel]||0)+1;
    L.items.forEach(function(x){
      if(x.done) things++;
      var k=normLine(x.t); if(!rep[k]) rep[k]={t:x.t, n:0}; rep[k].n++;
    });
  });
  var head='<div class="boxh-row"><h3 class="boxh">'+ic('calendar')+'<span>'+esc(t('wk3.t'))+'</span></h3></div>'+
    '<div class="wk-nav">'+
      '<button type="button" class="t3act" data-wk-nav="-1"'+(older?'':' disabled')+' aria-label="'+esc(t('wk.prev'))+'" title="'+esc(t('wk.prev'))+'">'+ic('chevron')+'</button>'+
      '<span>'+esc(wkOff ? t('wr.of',{d:fmtDay(days[0])}) : t('wk.this'))+'</span>'+
      '<button type="button" class="t3act" data-wk-nav="1"'+(wkOff?'':' disabled')+' aria-label="'+esc(t('wk.next'))+'" title="'+esc(t('wk.next'))+'">'+ic('chevron')+'</button>'+
    '</div>';
  if(!goals.length && !used.length){
    box.innerHTML=head+'<p class="hint">'+esc(t('wk3.none'))+'</p>'+(wkOff?'':weekReflection());
    bindWeek(); return;
  }
  /* the week in numbers - only the ones that are there */
  var tiles=[[steps,'sh.steps'],[things,'sh.done'],[choices,'wk.choices'],[used.length,'wk.active']].filter(function(c){ return c[0]>0; });
  var tilesHtml=tiles.length ? '<div class="wk-tiles">'+tiles.map(function(c){
    return '<div class="wk-tile"><b class="numf">'+c[0]+'</b><span>'+esc(t(c[1]))+'</span></div>'; }).join('')+'</div>' : '';
  function cells(fn){ return '<div class="wk-cells">'+days.map(fn).join('')+'</div>'; }
  var hdr=cells(function(d){
    return '<button type="button" class="wk-day'+(d===wkSel?' on':'')+(d===today?' today':'')+'" data-wk-day="'+d+'"'+
      (d>today?' disabled':'')+' aria-pressed="'+(d===wkSel)+'" aria-label="'+esc(lang(d,{weekday:'long',day:'numeric',month:'numeric'}))+'">'+
      '<span>'+esc(lang(d,{weekday:'narrow'}))+'</span><b class="numf">'+Number(d.slice(8))+'</b></button>';
  });
  function cls(d){ return (d>today?' fut':'')+(d===wkSel?' sel':''); }
  var rows=goals.map(function(g){
    var n=0, c=cells(function(d){
      var ok=!!(log[d] && log[d].steps.indexOf(g.id)>=0); if(ok) n++;
      var rest=!ok && !!(log[d] && (log[d].rest||[]).indexOf(g.id)>=0);
      return '<span class="wk-dot'+(ok?' on':'')+(rest?' rested':'')+cls(d)+'"'+(rest?' title="'+esc(t('rest.done'))+'"':'')+'>'+(ok?ic('check'):rest?'🌿':'')+'</span>';
    });
    return '<div class="wk-row"><div class="wk-name">'+ic('target')+'<span>'+esc(g.title)+'</span>'+
      (n?'<b class="wk-n numf">'+ic('check')+n+'</b>':'')+'</div>'+c+'</div>';
  }).join('');
  rows+='<div class="wk-row"><div class="wk-name">'+ic('sun')+'<span>'+esc(t('t3.more'))+'</span>'+
      (things?'<b class="wk-n numf">'+ic('check')+things+'</b>':'')+'</div>'+
    cells(function(d){
      var n=log[d] ? log[d].items.filter(function(x){ return x.done; }).length : 0;
      return '<span class="wk-dot'+(n?' on num':'')+cls(d)+'">'+(n?'<b class="numf">'+n+'</b>':'')+'</span>';
    })+'</div>';
  if(Object.keys(feels).length) rows+='<div class="wk-row"><div class="wk-name">'+ic('moon')+'<span>'+esc(t('wk.feel'))+'</span></div>'+
    cells(function(d){
      var f=log[d] && FEELS.filter(function(x){ return x.k===log[d].feel; })[0];
      return '<span class="wk-dot emo'+cls(d)+'">'+(f?f.e:'')+'</span>';
    })+'</div>';
  /* the chosen day, opened */
  var L=log[wkSel]||{items:[],steps:[]};
  var ds=goals.filter(function(g){ return L.steps.indexOf(g.id)>=0; }).map(function(g){
    var st=L.st&&L.st[g.id];
    return '<li>'+ic('check')+'<span><b>'+esc(g.title)+'</b>'+(st?' · '+esc(st):'')+'</span></li>'; }).join('');
  var dr=goals.filter(function(g){ return (L.rest||[]).indexOf(g.id)>=0; }).map(function(g){
    return '<li><span class="wk-li-e">🌿</span><span><b>'+esc(g.title)+'</b> · '+esc(t('rest.short'))+'</span></li>'; }).join('');
  var dt=L.items.filter(function(x){ return x.done; }).map(function(x){ return '<li>'+ic('check')+'<span>'+esc(x.t)+'</span></li>'; }).join('');
  var f=FEELS.filter(function(x){ return x.k===L.feel; })[0];
  var panel='<div class="wk-panel"><h4>'+esc(lang(wkSel,{weekday:'long',day:'numeric',month:'numeric'}))+'</h4>'+
    ((ds||dr)?'<div class="mg-lab">'+esc(t('t3.forgoals'))+'</div><ul class="wk-list">'+ds+dr+'</ul>':'')+
    (dt?'<div class="mg-lab">'+esc(t('t3.more'))+'</div><ul class="wk-list">'+dt+'</ul>':'')+
    (L.choice?'<p class="wk-feel">'+ic('compass')+'<span>'+esc(L.choice)+'</span></p>':'')+
    ((f||L.note)?'<p class="wk-feel">'+(f?'<span class="eve-e">'+f.e+'</span>'+esc(t('ev.f.'+f.k)):'')+(L.note?(f?' · ':'')+'<q>'+esc(L.note)+'</q>':'')+'</p>':'')+
    ((ds||dr||dt||f||L.note||L.choice)?'':'<p class="hint">'+esc(t(wkSel===today?'wk.d.today':'wk.d.rest'))+'</p>')+
    '</div>';
  /* a line that keeps coming back is often the real goal */
  var idea='';
  var back=Object.keys(rep).map(function(k){ return rep[k]; }).filter(function(x){ return x.n>=2; })
    .sort(function(a,b){ return b.n-a.n; })[0];
  if(back && !goals.some(function(g){ return normLine(g.title)===normLine(back.t); }))
    idea='<div class="wk3read"><p class="wk3idea">'+ic('sparkles')+'<span>'+esc(t('wk3.idea',{x:back.t}))+'</span></p>'+
      '<button class="btn btn-ghost btn-sm" data-wk3-new="'+esc(back.t)+'">'+ic('target')+'<span>'+esc(t('wk3.mk'))+'</span></button></div>';
  var vis=(P.vision||'').trim();
  box.innerHTML=head+
    (vis && !wkOff ? '<p class="wk-vision">'+ic('compass')+'<span><small>'+esc(t('vis.lab'))+'</small> '+esc(vis)+'</span></p>' : '')+
    tilesHtml+
    '<div class="wk-grid">'+hdr+rows+'</div>'+
    '<p class="hint wk-tap">'+esc(t('wk.tap'))+'</p>'+
    panel+idea+
    ((steps||things) ? '<button class="btn btn-primary btn-sm wk3share" data-wk3-share>'+ic('share')+'<span>'+esc(t('sh.btn'))+'</span></button>' : '')+
    (wkOff?'':weekReflection());
  bindWeek();
  box.querySelectorAll('[data-wk-day]').forEach(function(b){
    b.addEventListener('click',function(){ wkSel=b.dataset.wkDay; renderMyWeek(); });
  });
  var shb=box.querySelector('[data-wk3-share]');
  if(shb) shb.addEventListener('click',function(){
    var top=Object.keys(feels).sort(function(a,b){ return feels[b]-feels[a]; })[0];
    shareWeek({done:things, steps:steps, days:used.length, feel:top});
  });
  var nw=box.querySelector('[data-wk3-new]');
  if(nw) nw.addEventListener('click',function(){ openChainAt('goals', nw.dataset.wk3New); });
  function bindWeek(){
    bindWeekReflection(box);
    box.querySelectorAll('[data-wk-nav]').forEach(function(b){
      b.addEventListener('click',function(){ wkOff=Math.min(0,wkOff+Number(b.dataset.wkNav)); wkSel=null; renderMyWeek(); });
    });
  }
}

function sharpenGoals(){
  var gs=liveGoals();
  if(gs.length!==1){ goPage('goals'); return; }
  goalEditId=gs[0].id; goPage('goals');
}

/* ---- the week as a picture to share ----
   Only numbers and the week's most common feeling - never the lines
   themselves, which may be private. */
function shareWeek(w){
  var W=1080,H=1350,c=document.createElement('canvas'); c.width=W; c.height=H;
  var x=c.getContext('2d'), rtl=document.documentElement.dir==='rtl';
  var g=x.createLinearGradient(0,H,W,0); g.addColorStop(0,'#E9F0E2'); g.addColorStop(1,'#FBF8F1');
  x.fillStyle=g; x.fillRect(0,0,W,H);
  x.direction=rtl?'rtl':'ltr'; x.textAlign='center';
  var serif=getComputedStyle(document.body).getPropertyValue('--f-display')||'sans-serif';
  function txt(s,y,size,col,weight){ x.font=(weight||700)+' '+size+'px '+serif; x.fillStyle=col; x.fillText(s,W/2,y); }
  txt(t('sh.title'),250,64,'#173F2A',800);
  /* zeros are left off: the picture is something to be proud of */
  var cells=[[w.steps,t('sh.steps')],[w.done,t('sh.done')],[w.days,t('wk.active')]].filter(function(cl){ return cl[0]>0; });
  var top=430+(3-cells.length)*125;
  cells.forEach(function(cl,i){
    var y=top+i*250;
    x.fillStyle='#FFFFFF'; x.beginPath(); (x.roundRect||function(a,b,c2,d){ this.rect(a,b,c2,d); }).call(x,140,y-120,W-280,200,40); x.fill();
    txt(String(cl[0]),y+5,110,'#3D7B5E',800);
    txt(cl[1],y+60,38,'#3E5A4A',600);
  });
  var f=w.feel && FEELS.filter(function(z){ return z.k===w.feel; })[0];
  if(f) txt(f.e+'  '+t('ev.f.'+f.k),1150,52,'#173F2A',700);
  txt('Proacty · '+t('n.hero.lead'),1270,40,'#3E5A4A',600);
  var img=new Image();
  img.onload=function(){ x.drawImage(img,W/2-60,40,120,120); out(); };
  img.onerror=out;
  img.src='icon-192.png';
  function out(){
    c.toBlob(function(blob){
      var file=new File([blob],'proacty-week.png',{type:'image/png'});
      if(navigator.canShare && navigator.canShare({files:[file]})){
        navigator.share({files:[file], text:t('sh.text')}).catch(function(){});
      } else {
        var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='proacty-week.png';
        document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); },0);
        toast(t('sh.saved'));
      }
    },'image/png');
  }
}

/* ---- the week's reflection: what worked, what changes next week ----
   Kept per week (by its Sunday) in S.weeks; earlier ones fold away below,
   so it is possible to look back and see how the answers moved. */
function weekReflection(){
  var W=(S.weeks||{})[weekKey()]||{};
  var past=Object.keys(S.weeks||{}).filter(function(k){ return k!==weekKey(); }).sort().reverse().slice(0,8);
  return '<div class="wk3refl" id="weekRefl">'+
    '<h4>'+ic('sparkles')+'<span>'+esc(t('wr.t'))+'</span></h4>'+
    '<div class="field"><label for="wrGood">'+esc(t('wr.q1'))+'</label>'+
      '<textarea id="wrGood" rows="2" maxlength="300" placeholder="'+esc(t('wr.ph1'))+'">'+esc(W.good||'')+'</textarea></div>'+
    '<div class="field"><label for="wrNext">'+esc(t('wr.q2'))+'</label>'+
      '<textarea id="wrNext" rows="2" maxlength="300" placeholder="'+esc(t('wr.ph2'))+'">'+esc(W.next||'')+'</textarea></div>'+
    '<div class="row-btns">'+
      '<button class="btn btn-primary btn-sm" data-wr-save>'+ic('check')+'<span>'+esc(t('c.save'))+'</span></button>'+
      (liveGoals().length?'<button class="btn btn-ghost btn-sm" data-wr-fix>'+ic('edit')+'<span>'+esc(t('wk3.fix'))+'</span></button>':'')+
    '</div>'+
    (past.length ? '<details class="wr-past"><summary>'+esc(t('wr.past'))+'</summary>'+past.map(function(k){
        var w=S.weeks[k];
        return '<div class="wr-item"><b>'+esc(t('wr.of',{d:fmtDay(k)}))+'</b>'+
          (w.good?'<p><span>'+esc(t('wr.q1'))+'</span> '+esc(w.good)+'</p>':'')+
          (w.next?'<p><span>'+esc(t('wr.q2'))+'</span> '+esc(w.next)+'</p>':'')+'</div>';
      }).join('')+'</details>' : '')+
    '</div>';
}
function bindWeekReflection(box){
  var sv=box.querySelector('[data-wr-save]');
  if(sv) sv.addEventListener('click',function(){
    var good=document.getElementById('wrGood').value.trim(), next=document.getElementById('wrNext').value.trim();
    if(!good && !next){ document.getElementById('wrGood').focus(); return; }
    if(!S.weeks) S.weeks={};
    S.weeks[weekKey()]={good:good, next:next, at:dayKey()};
    markActiveToday(); save(); toast(t('wr.saved')); celebrate(); renderEvening();
  });
  var fx=box.querySelector('[data-wr-fix]');
  if(fx) fx.addEventListener('click',sharpenGoals);
}

/* ---- editing a goal: the name and its ladder, in one small form ----
   The weekly mission made when the goal started carries the goal's name,
   so it is renamed with it. */
var goalEditId=null;
function goalEditForm(g){
  var others=liveGoals().filter(function(o){ return o.id!==g.id; });
  function row(f,lab,ph){
    return '<div class="field"><label for="ge-'+f+'">'+esc(t(lab))+'</label>'+
      '<input type="text" id="ge-'+f+'" data-ge="'+f+'" maxlength="100" value="'+esc(g[f]||'')+'"'+
      (ph?' placeholder="'+esc(t(ph))+'"':'')+'></div>';
  }
  return '<div class="gedit">'+
    row('title','gl.goal')+whyField('ge-why', g.why)+row('week','gl.week','gl.wk.ph')+
    row('today','gl.today','gl.td.ph')+row('now','gl.now','ge.now.ph')+
    '<div class="row-btns">'+
      '<button class="btn btn-primary btn-sm" data-ge-save>'+ic('check')+'<span>'+esc(t('c.save'))+'</span></button>'+
      '<button class="btn btn-ghost btn-sm" data-ge-cancel>'+esc(t('c.cancel'))+'</button>'+
    '</div>'+
    (others.length ? '<div class="ge-merge"><label for="ge-mergeSel">'+esc(t('ge.merge'))+'</label><div class="addrow">'+
        '<select id="ge-mergeSel">'+others.map(function(o){ return '<option value="'+o.id+'">'+esc(o.title)+'</option>'; }).join('')+'</select>'+
        '<button class="btn btn-ghost btn-sm" data-ge-merge>'+ic('link')+'<span>'+esc(t('ge.merge.btn'))+'</span></button></div>'+
        '<p class="hint">'+esc(t('ge.merge.h'))+'</p></div>' : '')+
    '<button class="btn btn-quiet btn-sm ge-del" data-ge-del>'+ic('trash')+'<span>'+esc(t('ge.del'))+'</span></button>'+
    '</div>';
}
/* Deleting a goal takes its weekly mission with it and unlinks the day
   lines that pointed at it; the days it was part of stay in the log. */
function deleteGoal(id){
  prefLearn(goalCat(goalById(id)),-1);
  S.goals=(S.goals||[]).filter(function(g){ return g.id!==id; });
  S.missions=(S.missions||[]).filter(function(m){ return m.goalId!==id; });
  today3().items.forEach(function(x){ if(x.gid===id) x.gid=null; });
  if(goalEditId===id) goalEditId=null;
  save(); renderGoals(); renderWeek(); renderDash();
  toast(t('ge.deleted'));
}
/* Two goals that are really one: the one kept takes the other's steps,
   any empty rung, its started date if earlier, and every day line, day
   record and goal step that pointed at it. One weekly mission remains. */
function mergeGoals(keepId,dropId){
  var a=goalById(keepId), b=goalById(dropId);
  if(!a || !b || a===b) return;
  var seen={}; a.actions.forEach(function(x){ seen[normLine(x.text||x.key)]=1; });
  b.actions.forEach(function(x){ if(!seen[normLine(x.text||x.key)]){ a.actions.push(x); seen[normLine(x.text||x.key)]=1; } });
  /* the kept goal keeps its own step; only a goal with none takes the other's */
  if(!(a.now||a.today)) ['now','today'].forEach(function(k){ if(b[k]) a[k]=b[k]; });
  if(!a.week && b.week) a.week=b.week;
  if(!a.freq && b.freq) a.freq=b.freq;
  if(b.started && (!a.started || (b.startedAt && b.startedAt<a.startedAt))){ a.started=true; a.startedAt=b.startedAt; }
  if(b.doneDay && (!a.doneDay || b.doneDay>a.doneDay)) a.doneDay=b.doneDay;
  var keepMission=(S.missions||[]).some(function(m){ return m.goalId===a.id; });
  S.missions=(S.missions||[]).filter(function(m){
    if(m.goalId!==b.id) return true;
    if(keepMission) return false;
    m.goalId=a.id; m.title=a.title; keepMission=true; return true;
  });
  today3().items.forEach(function(x){ if(x.gid===b.id) x.gid=a.id; });
  Object.keys(S.log||{}).forEach(function(d){
    var L=S.log[d];
    L.items.forEach(function(x){ if(x.gid===b.id) x.gid=a.id; });
    L.steps=L.steps.map(function(id){ return id===b.id ? a.id : id; })
               .filter(function(id,i,arr){ return arr.indexOf(id)===i; });
    if(L.rest) L.rest=L.rest.map(function(id){ return id===b.id ? a.id : id; })
               .filter(function(id,i,arr){ return arr.indexOf(id)===i && L.steps.indexOf(id)<0; });
  });
  S.goals=S.goals.filter(function(g){ return g.id!==b.id; });
  goalEditId=null;
  save(); renderGoals(); renderWeek(); renderDash();
  toast(t('ge.merged',{a:a.title}));
}
function bindGoalEdit(host,g){
  bindWhy(host,'ge-why',function(){});
  host.querySelector('[data-ge-save]').addEventListener('click',function(){
    var v={};
    host.querySelectorAll('[data-ge]').forEach(function(i){ v[i.dataset.ge]=i.value.trim(); });
    if(!v.title){ toast(t('t.writegoal')); host.querySelector('[data-ge="title"]').focus(); return; }
    g.title=v.title; g.week=v.week; g.today=v.today; g.now=v.now;
    g.why=host.querySelector('#ge-why').value.trim();
    (S.missions||[]).forEach(function(m){ if(m.goalId===g.id) m.title=g.title; });
    goalEditId=null;
    save(); renderGoals(); renderWeek(); renderDash(); toast(t('gl.saved'));
  });
  host.querySelector('[data-ge-cancel]').addEventListener('click',function(){
    goalEditId=null; renderGoals(); renderDash();
  });
  host.querySelector('[data-ge-del]').addEventListener('click',function(){
    if(confirm(t('ge.del.q',{g:g.title}))) deleteGoal(g.id);
  });
  var mb=host.querySelector('[data-ge-merge]');
  if(mb) mb.addEventListener('click',function(){
    var other=goalById(Number(host.querySelector('#ge-mergeSel').value));
    if(other && confirm(t('ge.merge.q',{a:g.title, b:other.title}))) mergeGoals(g.id, other.id);
  });
}

/* Two live goals look like one when they share an area, or when one name
   holds a real word of the other's. Offered once per pair; "they are
   different" is remembered. */
function similarGoals(){
  var gs=liveGoals(), skip=S.mergeSkip||[];
  function words(s){ return normLine(s).split(/[\s·,.\-]+/).filter(function(w){ return w.length>=3; }); }
  for(var i=0;i<gs.length;i++) for(var j=i+1;j<gs.length;j++){
    var a=gs[i], b=gs[j], key=a.id+'-'+b.id;
    if(skip.indexOf(key)>=0) continue;
    var wa=words(a.title+' '+(a.today||'')), wb=words(b.title+' '+(b.today||''));
    var shared=wa.some(function(w){ return wb.indexOf(w)>=0; });
    if((a.area && a.area===b.area) || shared) return {a:a, b:b, key:key};
  }
  return null;
}

/* ---- materials: videos and links that help a goal ----
   Only links are kept - the video stays on YouTube, so the phone's small
   store is not filled. A YouTube link shows its thumbnail and plays in a
   player inside the app; anything else opens in a new tab. The search
   button opens YouTube with the goal's name and a few words for its area. */
var resOpen={};
function ytId(url){
  var m=String(url).match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?(?:.*&)?v=|shorts\/|embed\/|live\/))([\w-]{11})/);
  return m ? m[1] : null;
}
function firstVideo(g){ return (g.res||[]).filter(function(r){ return r.yt; })[0] || null; }
function resHtml(g){
  var list=g.res||[];
  var items=list.map(function(r){
    var thumb=r.yt ? '<img src="https://i.ytimg.com/vi/'+r.yt+'/mqdefault.jpg" alt="" loading="lazy">' : ic('link');
    return '<div class="res-item">'+
      '<button type="button" class="res-open" data-res-open="'+g.id+':'+r.id+'">'+thumb+'<span>'+esc(r.title)+'</span></button>'+
      '<button type="button" class="icon-btn" data-res-del="'+g.id+':'+r.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></div>';
  }).join('');
  return '<details class="res"'+(resOpen[g.id]?' open':'')+' data-res-box="'+g.id+'"><summary>'+ic('link')+'<span>'+esc(t('res.t'))+
      (list.length?' · '+list.length:'')+'</span></summary>'+
    (items ? '<div class="res-list">'+items+'</div>' : '<p class="hint">'+esc(t('res.empty'))+'</p>')+
    '<div class="res-add"><input type="url" inputmode="url" data-res-url="'+g.id+'" placeholder="'+esc(t('res.url.ph'))+'" aria-label="'+esc(t('res.url.ph'))+'">'+
      '<input type="text" maxlength="60" data-res-title="'+g.id+'" placeholder="'+esc(t('res.title.ph'))+'" aria-label="'+esc(t('res.title.ph'))+'">'+
      '<button class="btn btn-primary btn-sm" data-res-add="'+g.id+'">'+ic('plus')+'<span>'+esc(t('c.add'))+'</span></button></div>'+
    '<button class="btn btn-ghost btn-sm res-yt" data-res-yt="'+g.id+'">'+ic('globe')+'<span>'+esc(t('srch.t'))+'</span></button>'+
    '<p class="hint">'+esc(t('res.yt.h'))+'</p>'+
  '</details>';
}
function bindRes(host, rerender){
  function pair(v){ var a=v.split(':'); return {g:goalById(Number(a[0])), id:Number(a[1])}; }
  host.querySelectorAll('[data-res-box]').forEach(function(d){
    d.addEventListener('toggle',function(){ resOpen[d.dataset.resBox]=d.open; });
  });
  host.querySelectorAll('[data-res-add]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.resAdd));
      var u=host.querySelector('[data-res-url="'+g.id+'"]'), tt=host.querySelector('[data-res-title="'+g.id+'"]');
      var url=u.value.trim();
      if(url && !/^https?:\/\//i.test(url) && /^[\w-]+(\.[\w-]+)+/.test(url)) url='https://'+url;
      if(!/^https?:\/\/\S+\.\S+/i.test(url)){ toast(t('res.bad')); u.focus(); return; }
      var yt=ytId(url), name=tt.value.trim();
      if(!name){ try{ name = yt ? t('res.ytname') : new URL(url).hostname.replace(/^www\./,''); }catch(e){ name=url; } }
      if(!g.res) g.res=[];
      g.res.push({id:uid++, url:url, title:name, yt:yt});
      resOpen[g.id]=true; save(); rerender(); toast(t('gl.saved'));
    });
  });
  host.querySelectorAll('[data-res-del]').forEach(function(b){
    b.addEventListener('click',function(){
      var x=pair(b.dataset.resDel); if(!x.g) return;
      x.g.res=(x.g.res||[]).filter(function(r){ return r.id!==x.id; }); save(); rerender();
    });
  });
  host.querySelectorAll('[data-res-open]').forEach(function(b){
    b.addEventListener('click',function(){
      var x=pair(b.dataset.resOpen); if(!x.g) return;
      var r=(x.g.res||[]).filter(function(z){ return z.id===x.id; })[0];
      if(r) openRes(r);
    });
  });
  host.querySelectorAll('[data-res-yt]').forEach(function(b){
    b.addEventListener('click',function(){
      srchOpen({gid:Number(b.dataset.resYt)});
    });
  });
}
function openRes(r){
  if(!r.yt){ window.open(r.url,'_blank','noopener'); return; }
  var m=document.getElementById('vidModal');
  document.getElementById('vidTitle').textContent=r.title;
  document.getElementById('vidFrame').src='https://www.youtube-nocookie.com/embed/'+r.yt+'?autoplay=1&rel=0&playsinline=1';
  document.getElementById('vidOut').href=r.url;
  m.classList.add('on');
}
function closeVid(){
  var m=document.getElementById('vidModal'); m.classList.remove('on');
  document.getElementById('vidFrame').src='about:blank';   // stops the sound
}

function openChainAt(area, kindText){
  if(goalLimitReached()){ toast(t('pro.goalmax',{n:GOAL_FREE_MAX})); openPlans(); return; }
  resetChain();
  CH.area=area; CH.step=1;
  if(kindText){ CH.kind='other'; CH.kindText=kindText; CH.step=2; }
  saveChain();
  goPage('goals');
  var host=document.getElementById('goalChain'); host.hidden=false;
  document.getElementById('newGoalBtn').hidden=true;
  renderChain('goalChain');
  host.scrollIntoView({block:'start',behavior:'smooth'});
}
/* Today's step for a goal is chosen each day: what was written yesterday
   ("I went to the gym") is yesterday's. The goal's own rungs (right now,
   today) and the last few steps chosen are offered as one-tap choices,
   so a step that repeats is still one tap away. */
function dayStep(g){ return (g.day && g.day.d===dayKey()) ? g.day.t : ''; }
function stepChoices(g){
  var seen={}, out=[];
  (g.past||[]).concat([g.now, g.today]).forEach(function(s){
    s=String(s||'').trim(); var k=normLine(s);
    if(s && !seen[k] && out.length<4){ seen[k]=1; out.push(s); }
  });
  return out;
}
function setDayStep(g,text){
  text=String(text||'').trim(); if(!text) return;
  g.day={d:dayKey(), t:text};
  g.past=[text].concat((g.past||[]).filter(function(s){ return normLine(s)!==normLine(text); })).slice(0,6);
  save(); renderToday3();
}
/* A ready goal arrives whole - name, how often, this week, today, right
   now - and started, so it shows on Home at once. Teens and adults get
   different sets; goals the user already has are not offered again. */
/* ---- under "write a goal in your own words": goals to choose from ----
   For someone who does not want to write one, so it is still a choice:
   one for the area the check-in found weakest, then ideas for the age.
   A tap fills the field, where it can be changed before adding. */
function freeGoalPicks(){
  var band=P.age ? ageBand(P.age) : 'a13', out=[], have={};
  (S.goals||[]).forEach(function(g){ have[normLine(g.title)]=1; });
  if(hasProfile()) out.push(t('fg.dim.'+weakDim()));
  [1,2,3,4,5].forEach(function(n){ out.push(t('fg.'+band+'.'+n)); });
  return out.filter(function(x){ return !have[normLine(x)]; });
}
function renderFreePicks(box){
  var inp=document.getElementById(box.dataset.fgFor); if(!inp) return;
  var picks=freeGoalPicks();
  box.innerHTML=picks.length ? '<div class="mg-lab">'+esc(t('fg.t'))+'</div><div class="mg-picks">'+picks.map(function(x){
    return '<button type="button" class="t3idea" data-fg="'+esc(x)+'">'+ic('plus')+'<span>'+esc(x)+'</span></button>'; }).join('')+'</div>' : '';
  box.querySelectorAll('[data-fg]').forEach(function(b){
    b.addEventListener('click',function(){
      inp.value=b.dataset.fg; inp.dispatchEvent(new Event('input',{bubbles:true})); inp.focus();
      box.querySelectorAll('[data-fg]').forEach(function(o){ o.classList.toggle('on',o===b); });
    });
  });
}
/* filled each time the box is opened, so it follows the age, the check-in and the goals */
document.addEventListener('toggle',function(e){
  var d=e.target; if(!d.open || !d.classList || !d.classList.contains('ch-free')) return;
  var box=d.querySelector('.fg-picks'); if(box) renderFreePicks(box);
},true);

/* Ready goals: [id, area, freq, category, age, check-in area].
   age is t (up to 17), a (18 and up) or '' for everyone. */
var RG_CATS=[{id:'body',icon:'activity'},{id:'study',icon:'book'},{id:'people',icon:'users'},
             {id:'money',icon:'wallet'},{id:'calm',icon:'seedling'},{id:'create',icon:'palette'}];
var READY_GOALS=[
 [1,'study',4,'study','t','plan'],[2,'sleep',5,'body','t','plan'],[3,'habits',5,'calm','','choice'],[4,'sport',3,'body','t','init'],
 [5,'learn',4,'create','','goal'],[6,'social',2,'people','t','init'],[7,'sport',3,'body','a','init'],[8,'sleep',5,'body','a','plan'],
 [10,'learn',3,'study','a','goal'],[11,'time',5,'study','a','time'],[12,'social',2,'people','a','init'],
 [13,'sport',3,'body','t','init'],[14,'habits',5,'body','','plan'],[15,'sport',5,'body','a','init'],[16,'habits',5,'body','','plan'],
 [17,'sport',5,'body','a','time'],[18,'habits',5,'body','t','plan'],
 [19,'study',5,'study','t','time'],[20,'study',3,'study','t','solve'],[21,'learn',3,'study','a','goal'],[22,'goals',5,'study','a','goal'],
 [23,'learn',4,'study','','goal'],[24,'goals',2,'study','a','init'],
 [25,'social',2,'people','t','init'],[26,'social',3,'people','','init'],[27,'social',3,'people','','init'],[28,'social',4,'people','t','choice'],
 [29,'social',1,'people','a','plan'],[30,'social',5,'people','','choice'],
 [31,'habits',1,'money','t','goal'],[32,'habits',1,'money','t','plan'],[33,'habits',5,'money','a','plan'],[34,'time',1,'money','a','time'],
 [35,'habits',5,'money','','plan'],[36,'time',1,'money','','plan'],
 [37,'habits',5,'calm','','choice'],[38,'habits',4,'calm','','solve'],[39,'habits',5,'calm','','choice'],[40,'habits',5,'calm','','choice'],
 [41,'study',3,'calm','t','plan'],[42,'habits',3,'calm','a','time'],
 [43,'learn',4,'create','','init'],[44,'learn',3,'create','','init'],[45,'learn',1,'create','','init'],[46,'learn',3,'create','t','goal'],
 [47,'learn',2,'create','','init'],[48,'learn',1,'create','a','init']
];
function rgById(id){ return READY_GOALS.filter(function(r){ return r[0]===id; })[0]; }
/* a goal's category: its own if it came ready, else read from its area */
var AREA_CAT={sport:'body',sleep:'body',study:'study',time:'study',goals:'study',social:'people',init:'people',habits:'calm',learn:'create'};
function goalCat(g){ return g && (g.cat || AREA_CAT[g.area]) || null; }

/* ---- learning the user ----
   Every choice nudges S.pref, one number per category: a ready goal added
   (3), a goal built or picked for today (2 / 1), a step done (1), an idea
   taken (1), a category opened (0.5), a goal deleted (-1). A new day lets
   old weight fade a little, so what someone chooses now counts most. */
function prefLearn(cat, w){
  if(!cat) return;
  if(!S.pref) S.pref={};
  var d=dayKey();
  if(S.prefDay!==d){ Object.keys(S.pref).forEach(function(k){ S.pref[k]=Math.round(S.pref[k]*95)/100; }); S.prefDay=d; }
  S.pref[cat]=Math.max(0, Math.min(30, (S.pref[cat]||0)+w));
}
function topCats(){
  var p=S.pref||{};
  return Object.keys(p).filter(function(k){ return p[k]>=1; }).sort(function(a,b){ return p[b]-p[a]; });
}
function ageKey(){ return (!P.age || ageBand(P.age)==='a13') ? 't' : 'a'; }
function readyFits(r){ return !r[4] || r[4]===ageKey(); }
function readyGoals(cat){
  var have={}; (S.goals||[]).forEach(function(g){ have[normLine(g.title)]=1; });
  var list=READY_GOALS.filter(function(r){ return readyFits(r) && !have[normLine(t('rg.'+r[0]+'.t'))]; });
  if(cat && cat!=='for') return list.filter(function(r){ return r[3]===cat; });
  /* for you: the check-in's weakest area, the areas it said matter, and what
     the user keeps choosing; a daily turn breaks ties, and no category takes
     more than two of the six places */
  var weak=hasProfile()?weakDim():null, areas=(S.quiz&&S.quiz.areas)||[], p=S.pref||{}, day=dayKey();
  function rot(id){ var h=0, s=day+':'+id; for(var i=0;i<s.length;i++) h=(h*31+s.charCodeAt(i))%997; return h/997; }
  var scored=list.map(function(r){
    return {r:r, s:(r[5]===weak?2:0)+(areas.indexOf(r[1])>=0?1.5:0)+Math.min(6,p[r[3]]||0)+rot(r[0])*0.9};
  }).sort(function(a,b){ return b.s-a.s; });
  var per={}, out=[];
  scored.forEach(function(x){ if(out.length<6 && (per[x.r[3]]||0)<2){ per[x.r[3]]=(per[x.r[3]]||0)+1; out.push(x.r); } });
  return out;
}
function addReadyGoal(r){
  if(goalLimitReached()){ toast(t('pro.goalmax',{n:GOAL_FREE_MAX})); openPlans(); return; }
  var title=t('rg.'+r[0]+'.t'), g=newGoal(title);
  g.area=r[1]; g.freq=r[2]; g.cat=r[3]; g.rg=r[0];
  prefLearn(r[3],3);
  g.week=t('gw.line',{freq:t('gf.'+r[2]), kind:title});
  g.today=t('rg.'+r[0]+'.d'); g.now=t('rg.'+r[0]+'.n');
  g.actions=[{id:uid++,key:null,text:g.now,done:false},{id:uid++,key:null,text:g.today,done:false},{id:uid++,key:null,text:g.week,done:false}];
  S.goals.unshift(g);
  startGoal(g);
  toast(t('rg.added'));
  renderGoals();
  return g;
}
/* Above the goals: the offer to merge two that look alike, and the ready
   goals - both used to live in a goal card on Home. */
function renderGoalExtras(){
  var sb=document.getElementById('goalSim'), rb=document.getElementById('goalReady');
  if(sb){
    var sim=goalEditId?null:similarGoals();
    sb.innerHTML = sim ? '<div class="mg-sim">'+ic('link')+'<span>'+esc(t('mg.sim',{a:sim.a.title, b:sim.b.title}))+'</span>'+
      '<div class="row-btns"><button class="btn btn-primary btn-sm" data-sim-yes>'+esc(t('ge.merge.btn'))+'</button>'+
      '<button class="btn btn-quiet btn-sm" data-sim-no>'+esc(t('mg.sim.no'))+'</button></div></div>' : '';
    if(sim){
      sb.querySelector('[data-sim-yes]').addEventListener('click',function(){
        if(confirm(t('ge.merge.q',{a:sim.a.title, b:sim.b.title}))) mergeGoals(sim.a.id, sim.b.id);
      });
      sb.querySelector('[data-sim-no]').addEventListener('click',function(){
        S.mergeSkip=(S.mergeSkip||[]).concat(sim.key); save(); renderGoals();
      });
    }
  }
  if(rb){ var h=readyHtml(); rb.hidden=!h; rb.innerHTML=h; bindReady(rb); }
}
var rgCat='for';
function readyHtml(){
  var list=readyGoals(rgCat);
  var tabs='<div class="rg-cats" role="tablist">'+[{id:'for',icon:'sparkles'}].concat(RG_CATS).map(function(c){
    return '<button type="button" class="rg-cat'+(rgCat===c.id?' on':'')+'" data-rgcat="'+c.id+'" role="tab" aria-selected="'+(rgCat===c.id)+'">'+
      ic(c.icon)+'<span>'+esc(t('rgc.'+c.id))+'</span></button>'; }).join('')+'</div>';
  return '<div class="mg-lab">'+esc(t('rg.t'))+'</div>'+tabs+
    (rgCat==='for' ? '<p class="rg-why">'+esc(t('rgc.why'))+'</p>' : '')+
    '<div class="rg-list">'+list.map(rgCard).join('')+'</div>';
}
function rgCard(r){
  var c=RG_CATS.filter(function(x){ return x.id===r[3]; })[0];
  return '<button type="button" class="rg" data-ready="'+r[0]+'">'+ic(c?c.icon:'target')+
    '<span><b>'+esc(t('rg.'+r[0]+'.t'))+'</b><small>'+esc(t('gf.'+r[2]))+'</small></span></button>';
}
function bindReady(box){
  box.querySelectorAll('[data-rgcat]').forEach(function(b){
    b.addEventListener('click',function(){
      rgCat=b.dataset.rgcat; if(rgCat!=='for') prefLearn(rgCat,0.5);
      save(); box.innerHTML=readyHtml(); bindReady(box);
    });
  });
  box.querySelectorAll('[data-ready]').forEach(function(b){
    b.addEventListener('click',function(){ var r=rgById(Number(b.dataset.ready)); if(r) addReadyGoal(r); });
  });
}

/* The same three facts onboarding asked for, editable later. Age feeds the
   check-in band and the training plan; gender re-renders every string. */
function renderSettings(){
  var n=document.getElementById('pfName'), a=document.getElementById('pfAge');
  if(n && document.activeElement!==n) n.value=P.name||'';
  if(a && document.activeElement!==a) a.value=P.age||'';
  var rm=document.getElementById('pfRemind');
  if(rm && document.activeElement!==rm) rm.value=P.remind||'17:00';
  renderLicState();
  document.querySelectorAll('#pfGender [data-pfg]').forEach(function(o){
    var on=o.dataset.pfg===P.gender;
    o.classList.toggle('on',on); o.setAttribute('aria-pressed',on?'true':'false');
  });
}
function bindSettings(){
  var n=document.getElementById('pfName'), a=document.getElementById('pfAge');
  if(n) n.addEventListener('change',function(){ P.name=n.value.trim(); save(); startApp(); });
  if(a) a.addEventListener('change',function(){
    var v=parseInt(a.value,10);
    if(!(v>=AGE_MIN && v<=AGE_MAX)){ toast(t('t.agerange')); a.value=P.age||''; return; }
    P.age=String(v); save(); startApp(); toast(t('gl.saved'));
  });
  document.querySelectorAll('#pfGender [data-pfg]').forEach(function(o){
    o.addEventListener('click',function(){ setGender(o.dataset.pfg); });
  });
  var rm=document.getElementById('pfRemind');
  if(rm) rm.addEventListener('change',function(){
    P.remind=rm.value||'17:00'; save(); toast(t('gl.saved'));
  });
}
function renderDash(){
  renderVision(); renderGenderAsk(); renderToday3(); renderEvening(); renderBackupAsk(); renderDashStats();
  renderAvatarCard(); renderInvite();
}


/* ================= the Body tab gate =================
   The mini-apps are the one large block of value that is not the proactivity
   core, so they are where Pro sits. The tab still opens, still says what is
   inside, and offers the way in - it never just refuses. */
function renderBodyGate(){
  var lock=document.getElementById('bodyLock'), wrap=document.getElementById('bodyViews');
  if(!lock||!wrap) return;
  var open=isPro();
  wrap.hidden=!open; lock.hidden=open;
  if(!open) lock.innerHTML=lockHtml('pro.f.body');
}

/* ================= the trend =================
   One series - the proactivity score, check-in by check-in - so there is no
   legend to read and no second axis to confuse it with. Only the first and last
   points carry a printed number; the rest are on hover. */
var TREND={w:320,h:130,pt:14,pb:22,pl:30,pr:12};
function trendPoints(){
  var h=(S.hist||[]).slice(-12);
  var n=h.length, g=TREND;
  var iw=g.w-g.pl-g.pr, ih=g.h-g.pt-g.pb;
  return h.map(function(e,i){
    var v=checkinAvg(e);
    return { x: g.pl + (n===1 ? iw/2 : iw*i/(n-1)), y: g.pt + ih*(1-v/100), v: v, d: e.d };
  });
}
function renderTrend(){
  var box=document.getElementById('trendBox'); if(!box) return;
  if(!isPro()){ box.innerHTML=lockHtml('pro.f.trend'); return; }
  var h=S.hist||[];
  if(h.length<2){
    box.innerHTML='<div class="empty-state">'+ic('trending')+
      '<p>'+esc(t(h.length?'tr.one':'tr.none'))+'</p>'+
      (h.length?'<button class="btn btn-ghost btn-sm" data-retake>'+esc(t('tr.retake'))+'</button>':'')+
      '</div>';
    bindRetake(box); return;
  }
  var p=trendPoints(), g=TREND;
  var line=p.map(function(q,i){ return (i?'L':'M')+q.x.toFixed(1)+' '+q.y.toFixed(1); }).join(' ');
  var first=p[0], last=p[p.length-1], delta=last.v-first.v;
  /* grid at 0/50/100 only - enough to read the height, quiet enough to ignore */
  var grid=[0,50,100].map(function(v){
    var y=g.pt+(g.h-g.pt-g.pb)*(1-v/100);
    return '<line class="tg" x1="'+g.pl+'" y1="'+y.toFixed(1)+'" x2="'+(g.w-g.pr)+'" y2="'+y.toFixed(1)+'"/>'+
           '<text class="tl" x="'+(g.pl-6)+'" y="'+(y+3.5).toFixed(1)+'" text-anchor="end">'+v+'</text>';
  }).join('');
  var dots=p.map(function(q,i){
    var edge=(i===0||i===p.length-1);
    return '<circle class="td'+(edge?' edge':'')+'" cx="'+q.x.toFixed(1)+'" cy="'+q.y.toFixed(1)+'" r="'+(edge?4.5:3.5)+'" data-i="'+i+'"/>';
  }).join('');
  var labs=[first,last].map(function(q,i){
    return '<text class="tv" x="'+q.x.toFixed(1)+'" y="'+(q.y-9).toFixed(1)+'" text-anchor="'+(i?'end':'start')+'">'+q.v+'</text>';
  }).join('');
  box.innerHTML=
    '<p class="trend-head">'+esc(t('tr.t'))+
      '<span class="trend-delta '+(delta>0?'up':delta<0?'down':'')+'">'+(delta>0?'+':'')+delta+'</span></p>'+
    '<svg class="trend" viewBox="0 0 '+g.w+' '+g.h+'" role="img" '+
      'aria-label="'+esc(t('tr.aria',{a:first.v,b:last.v,n:p.length}))+'">'+
      grid+'<path class="tline" d="'+line+'"/>'+dots+labs+
      '<rect id="trendHit" x="'+g.pl+'" y="0" width="'+(g.w-g.pl-g.pr)+'" height="'+g.h+'" fill="transparent"/>'+
    '</svg>'+
    '<div class="trend-tip" id="trendTip" hidden></div>'+
    '<div class="dimdelta">'+dimDeltas()+'</div>'+
    '<p class="hint">'+esc(t('tr.since',{d:fmtDay(first.d)}))+'</p>'+
    '<button class="btn btn-ghost btn-sm" data-retake>'+esc(t('tr.retake'))+'</button>';
  bindTrendHover(box, p);
  bindRetake(box);
}
/* The dimensions as text rather than a second series: five lines on one
   chart would be unreadable, and a second y-axis would be a lie. */
function dimDeltas(){
  var h=S.hist||[]; if(h.length<2) return '';
  var a=h[0].s, b=h[h.length-1].s;
  return DIMS.map(function(x){ return x.id; }).filter(function(k){ return typeof a[k]==='number' && typeof b[k]==='number'; }).map(function(k){
    var d=b[k]-a[k];
    return '<div class="dd"><span class="dd-k">'+esc(t('dim.'+k))+'</span>'+
      '<span class="dd-v '+(d>0?'up':d<0?'down':'')+'">'+(d>0?'+':'')+d+'</span></div>';
  }).join('');
}
function bindTrendHover(box, p){
  var hit=box.querySelector('#trendHit'), tip=box.querySelector('#trendTip');
  var svg=box.querySelector('svg.trend');
  if(!hit||!tip||!svg) return;
  function near(evt){
    var r=svg.getBoundingClientRect();
    var x=(evt.clientX-r.left)/r.width*TREND.w;
    var best=0, bd=1e9;
    p.forEach(function(q,i){ var d=Math.abs(q.x-x); if(d<bd){ bd=d; best=i; } });
    return best;
  }
  function show(evt){
    var i=near(evt), q=p[i]; if(!q) return;
    var r=svg.getBoundingClientRect();
    tip.hidden=false;
    tip.textContent=fmtDay(q.d)+' · '+q.v;
    tip.style.insetInlineStart=(q.x/TREND.w*r.width)+'px';
    svg.querySelectorAll('.td').forEach(function(c){ c.classList.toggle('hot', Number(c.dataset.i)===i); });
  }
  hit.addEventListener('pointermove',show);
  hit.addEventListener('pointerdown',show);
  hit.addEventListener('pointerleave',function(){
    tip.hidden=true; svg.querySelectorAll('.td').forEach(function(c){ c.classList.remove('hot'); });
  });
}
function bindRetake(box){
  var b=box.querySelector('[data-retake]');
  if(b) b.addEventListener('click',function(){
    restartQuiz();
    document.getElementById('app').style.display='none';
    document.getElementById('onboarding').style.display='block';
    showStep(4);
    renderQuiz();
  });
}

document.getElementById('vidClose').addEventListener('click',closeVid);
document.getElementById('vidModal').addEventListener('click',function(e){ if(e.target.id==='vidModal') closeVid(); });

/* ================= tabs ================= */
/* One <nav> serves as top tabs on a wide screen and as the bottom bar on a
   phone, so there is a single set of buttons and a single source of truth. */
/* Tasks, Learn and Body have no tab of their own; More stays lit on them. */
var UNDER_MORE=['tasks','learn','body','circle'];
function goPage(name){
  var tabName = UNDER_MORE.indexOf(name)>=0 ? 'more' : name;
  document.querySelectorAll('.tab').forEach(function(x){
    var on=x.dataset.page===tabName;
    x.classList.toggle('on', on);
    x.setAttribute('aria-selected', on?'true':'false');
  });
  document.querySelectorAll('.page').forEach(function(p){
    p.classList.toggle('on', p.id==='page-'+name);
  });
  try{ localStorage.setItem('proactive_tab', name); }catch(e){}
  if(name==='home') renderDash();
  if(name==='goals') renderGoals();
  if(name==='progress'){ renderMyWeek(); renderProfile('profBody'); renderAchievements(); renderSettings(); renderTrend(); renderBackupLast(); }
  if(name==='circle') renderCircle();
  if(name==='body') renderBodyGate();
  window.scrollTo(0,0);
}
document.querySelectorAll('.tab').forEach(function(tab){
  tab.addEventListener('click',function(){ goPage(tab.dataset.page); });
});
document.querySelectorAll('[data-more]').forEach(function(b){
  b.addEventListener('click',function(){ goPage(b.dataset.more); });
});
function lastTab(){
  try{
    var v=localStorage.getItem('proactive_tab');
    if(v && document.getElementById('page-'+v)) return v;
  }catch(e){}
  return 'home';
}

/* ================= boot ================= */
function renderTasks(){ renderRing(); renderCats(); }
function renderHome(){ renderTasks(); }   // kept: other modules still call it

/* A moment of who this is for, right after the phone's own splash: the
   logo, the name, the line about being who you want to be, and what the
   app is for. Once per opening, a second and a half, a tap skips it. */
var splashDone=false;
function showSplash(){
  if(splashDone) return; splashDone=true;
  var sp=document.getElementById('splash'); if(!sp) return;
  var tk=(P.gender==='m'||P.gender==='f') ? 'b.tag' : 'b.tag.n';
  document.getElementById('splashTag').textContent=t(tk);
  sp.querySelectorAll('[data-i18n]').forEach(function(e){ e.textContent=t(e.getAttribute('data-i18n')); });
  sp.hidden=false;
  function hide(){ if(sp.classList.contains('out')) return; sp.classList.add('out'); setTimeout(function(){ sp.hidden=true; },350); }
  sp.addEventListener('click',hide);
  setTimeout(hide,1600);
}
function startApp(){
  showSplash();
  var name=P.name || t('a.greet.anon');
  document.getElementById('greetName').textContent=t('a.greet',{name:name});
  var tag=document.getElementById('appTag'), tk=(P.gender==='m'||P.gender==='f') ? 'b.tag' : 'b.tag.n';
  if(tag){ tag.setAttribute('data-i18n',tk); tag.textContent=t(tk); }

  var wp=buildWorkout(P.age,P.workout,P.fitLevel);
  document.getElementById('woSub').textContent=
    t(wp.levelKey)+' · '+t('wo.'+P.workout);
  document.getElementById('woInfo').innerHTML=ic('sliders')+'<span>'+esc(wp.note)+'</span>';

  fillMissionCats(); renderInsight(); renderTasks(); renderGoals(); renderWeek();
  renderPlan('woGrid', wp.blocks, 'w');   // the "my weekly plan" section of the sport mini-app
  renderPlan('hyGrid', buildHygiene(), 'hy');
  renderTheories(); renderLessons(); renderAchievements(); renderSettings();
  renderStats(); renderTrial(); renderTrend(); renderBodyGate(); renderCheckout();
  revalidateLicense(); showInstall();
  renderMini();                            // the skincare routine lives in its mini-app
  renderDash();
  checkAchievements();
  goPage(lastTab());
}

document.querySelectorAll('.langbtn').forEach(function(b){
  b.addEventListener('click',function(){ setLang(b.dataset.lang); });
});

bindMini();
bindAccentPick();
bindGenderPick();
bindQuizAge();
bindSettings();
bindLicense();
bindPay();
bindBackup();
bindInstall();
loadLic();
loadPaid();
registerSW();
loadGender();
loadChain();
loadLook();
applyTheme();
loadQuiz();
applyLang();
renderGoalOpts();
['oTime','oWO','oFL','oSkin'].forEach(function(id){
  var attr={oTime:'time',oWO:'wo',oFL:'fl',oSkin:'skin'}[id];
  var field={oTime:'time',oWO:'workout',oFL:'fitLevel',oSkin:'skinType'}[id];
  singleSelect(id,attr,field);
});
markSelected();
captureRefParam();                 /* before load(): a ?ref= only counts on a fresh device */

if(load()){
  loadLook(); loadGender(); applyTheme();     // the profile may carry an older look; the keys win
  buildCats();
  document.getElementById('landing').style.display='none';
  document.body.classList.remove('has-sticky');
  document.getElementById('stickyCta').style.display='none';
  document.getElementById('app').style.display='block';
  document.body.classList.add('in-app');
  renderGoalOpts(); markSelected();
  startApp();
}
"""
