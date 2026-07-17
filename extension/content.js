// Kaka chrome extension content script
// Inject a tiny walking Kaka at the bottom of every page.
(function(){
  if(typeof window === 'undefined') return;
  // Run only in top frame
  try { if (window.top !== window) return; } catch(e) { return; }
  if (!document.documentElement) return;

  const STORAGE_KEY = 'kaka_ext_state_v1';
  const PET_SIZE = 72;
  const TICK_HZ = 30;

  function clamp(v, lo, hi){ return v < lo ? lo : (v > hi ? hi : v); }

  let state = {
    hunger: 70,
    mood: 75,
    affinity: 10,
    dnd: false,
    lastUpdated: Date.now(),
    personality: 'extrovert'
  };

  let canvas, ctx, container, menu;
  let pet = {
    x: 0,
    y: 0,
    vx: 0.6,
    facing: 1,
    bubbleText: '',
    bubbleUntil: 0
  };
  let lastTime = performance.now();
  let saveTimer = null;

  function scheduleSave(){
    if(!chrome || !chrome.storage || !chrome.storage.local) return;
    if(saveTimer) return;
    saveTimer = setTimeout(function(){
      saveTimer = null;
      state.lastUpdated = Date.now();
      chrome.storage.local.set({ [STORAGE_KEY]: state });
    }, 3000);
  }

  function applyDndUI(){
    if(!container) return;
    if(state.dnd) container.classList.add('kaka-ext-dnd');
    else container.classList.remove('kaka-ext-dnd');
    if(menu){
      const dndBtn = menu.querySelector('button[data-action="dnd"] span.label');
      if(dndBtn) dndBtn.textContent = state.dnd ? '关闭勿扰' : '开启勿扰';
    }
  }

  function showBubble(text, ms){
    if(state.dnd) return;
    pet.bubbleText = text;
    pet.bubbleUntil = performance.now() + (ms || 1600);
  }

  function drawPetSprite(){
    const size = PET_SIZE;
    const g = 16; const c = size / g;
    const S = { body:'#F5C542', dark:'#C08A18', cheek:'#F58A8A', eye:'#222', white:'#fff' };
    function R(px,py,w,h,col){ ctx.fillStyle = col; ctx.fillRect(pet.x+px*c, pet.y+py*c, w*c, h*c); }
    ctx.save();
    ctx.translate(pet.x + size/2, pet.y + size/2);
    if(pet.facing < 0) ctx.scale(-1,1);
    ctx.translate(-size/2, -size/2);
    ctx.imageSmoothingEnabled = false;
    R(4,3,8,1,S.body);R(3,4,10,1,S.body);R(2,5,12,6,S.body);
    R(3,11,10,1,S.body);R(4,12,8,1,S.body);R(4,13,3,1,S.body);R(9,13,3,1,S.body);
    R(3,10,10,1,S.dark);R(4,11,8,1,S.dark);
    const hungry = state.hunger < 35;
    R(5,6,2,2,S.white);R(9,6,2,2,S.white);
    R(6,7,1,1,S.eye);R(10,7,1,1,S.eye);
    R(4,9,1,1,S.cheek);R(11,9,1,1,S.cheek);
    if(hungry){ R(7,9,2,2,S.eye); }
    else { R(7,10,2,1,S.eye); }
    ctx.restore();
  }

  function drawBubble(){
    if(!pet.bubbleText || performance.now() > pet.bubbleUntil) return;
    const text = pet.bubbleText;
    const cx = pet.x + PET_SIZE/2;
    const cy = pet.y - 12;
    ctx.save();
    ctx.font = '12px -apple-system,\"PingFang SC\"';
    const w = ctx.measureText(text).width + 14;
    const h = 20;
    const x = cx - w/2;
    const y = cy - h;
    const r = 9;
    ctx.fillStyle = 'rgba(28,28,30,.9)';
    ctx.beginPath();
    ctx.moveTo(x+r,y);
    ctx.lineTo(x+w-r,y);
    ctx.quadraticCurveTo(x+w,y,x+w,y+r);
    ctx.lineTo(x+w,y+h-r);
    ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);
    ctx.lineTo(cx+4,y+h);
    ctx.lineTo(cx,y+h+6);
    ctx.lineTo(cx-4,y+h);
    ctx.lineTo(x+r,y+h);
    ctx.quadraticCurveTo(x,y+h,x,y+h-r);
    ctx.lineTo(x,y+r);
    ctx.quadraticCurveTo(x,y,x+r,y);
    ctx.fill();
    ctx.fillStyle = '#fff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, cx, y + h/2);
    ctx.restore();
  }

  function draw(){
    if(!ctx) return;
    const w = canvas.width, h = canvas.height;
    ctx.clearRect(0,0,w,h);
    const floorY = h - 10;
    ctx.strokeStyle = 'rgba(60,60,67,.15)';
    ctx.setLineDash([4,6]);
    ctx.beginPath();
    ctx.moveTo(0,floorY);
    ctx.lineTo(w,floorY);
    ctx.stroke();
    ctx.setLineDash([]);

    if(state.dnd){
      ctx.save();
      ctx.globalAlpha = 0.12;
      drawPetSprite();
      ctx.restore();
    } else {
      drawPetSprite();
      drawBubble();
    }
  }

  function update(dtMs){
    const dt = dtMs / 16.67;
    const w = canvas.width;
    const floorY = canvas.height - PET_SIZE - 8;
    if(!state.dnd){
      pet.x += pet.vx * dt;
      if(pet.x < 0){ pet.x = 0; pet.vx = Math.abs(pet.vx); pet.facing = 1; }
      else if(pet.x > w - PET_SIZE){ pet.x = w - PET_SIZE; pet.vx = -Math.abs(pet.vx); pet.facing = -1; }
    }
    pet.y = floorY;
    const minutes = dtMs / 60000;
    state.hunger = clamp(state.hunger - minutes * 3.5, 0, 100);
    state.mood = clamp(state.mood - minutes * 1.5, 0, 100);
    if(state.hunger > 70) state.mood = clamp(state.mood + minutes * 2.0, 0, 100);
    scheduleSave();
  }

  function loop(t){
    const dt = Math.min(80, t - lastTime);
    lastTime = t;
    if(canvas && ctx){ update(dt); draw(); }
    requestAnimationFrame(loop);
  }

  function handleMenuClick(action){
    if(action === 'feed'){
      state.hunger = clamp(state.hunger + 25, 0, 100);
      state.mood = clamp(state.mood + 8, 0, 100);
      showBubble('好吃好吃 🍪', 1600);
    } else if(action === 'pat'){
      state.mood = clamp(state.mood + 6, 0, 100);
      state.affinity = clamp(state.affinity + 2, 0, 100);
      showBubble('摸摸～', 1400);
    } else if(action === 'dnd'){
      state.dnd = !state.dnd;
      applyDndUI();
    } else if(action === 'open'){
      try { window.open('https://ustiniankw.github.io/Kaka/', '_blank'); } catch(e) {}
    }
    scheduleSave();
  }

  function setupMenu(){
    if(menu) return;
    menu = document.createElement('div');
    menu.id = 'kaka-ext-menu';
    menu.className = 'kaka-ext-menu';
    menu.innerHTML = [
      '<button data-action="feed"><span>🍪</span><span class="label">喂点吃的</span></button>',
      '<button data-action="pat"><span>🤚</span><span class="label">摸摸头</span></button>',
      '<hr />',
      '<button data-action="dnd"><span>🔕</span><span class="label">开启勿扰</span></button>',
      '<button data-action="open"><span>🖥</span><span class="label">打开完整界面</span></button>'
    ].join('');
    document.body.appendChild(menu);
    menu.addEventListener('click', function(e){
      const btn = e.target.closest('button');
      if(!btn) return;
      const action = btn.getAttribute('data-action');
      hideMenu();
      handleMenuClick(action);
    });
    document.addEventListener('click', function(e){
      if(!menu) return;
      if(menu.contains(e.target)) return;
      hideMenu();
    });
  }

  function showMenu(x,y){
    setupMenu();
    if(!menu) return;
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';
    menu.classList.add('show');
  }

  function hideMenu(){
    if(menu) menu.classList.remove('show');
  }

  function setupUI(){
    if(document.getElementById('kaka-ext-container')) return;
    container = document.createElement('div');
    container.id = 'kaka-ext-container';
    const hint = document.createElement('div');
    hint.className = 'kaka-ext-hint';
    hint.textContent = '右键 Kaka 打开菜单';
    canvas = document.createElement('canvas');
    canvas.width = 200;
    canvas.height = 160;
    container.appendChild(canvas);
    container.appendChild(hint);
    document.body.appendChild(container);
    ctx = canvas.getContext('2d');
    const rect = container.getBoundingClientRect();
    const rightPct = 10 + Math.random() * 70;
    container.style.right = rightPct + '%';
    pet.x = (canvas.width - PET_SIZE) * Math.random();
    pet.y = canvas.height - PET_SIZE - 8;
    canvas.addEventListener('contextmenu', function(e){
      e.preventDefault();
      showMenu(e.clientX, e.clientY);
    });
    applyDndUI();
  }

  function hydrateFromStorage(){
    if(!chrome || !chrome.storage || !chrome.storage.local){
      setupUI();
      requestAnimationFrame(loop);
      return;
    }
    chrome.storage.local.get(STORAGE_KEY, function(data){
      if(data && data[STORAGE_KEY]){
        try{
          const saved = data[STORAGE_KEY];
          const now = Date.now();
          const last = saved.lastUpdated || now;
          const elapsed = Math.max(0, now - last);
          state = Object.assign({}, state, saved);
          const hours = elapsed / 3600000;
          if(hours > 0){
            state.hunger = clamp(state.hunger - hours*8, 0, 100);
            state.mood = clamp(state.mood - hours*3, 0, 100);
          }
        }catch(e){}
      }
      setupUI();
      applyDndUI();
      requestAnimationFrame(loop);
    });
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', hydrateFromStorage);
  } else {
    hydrateFromStorage();
  }
})();
