// Popup for Kaka chrome extension
(function(){
  const STORAGE_KEY = 'kaka_ext_state_v1';
  function clamp(v,lo,hi){return v<lo?lo:(v>hi?hi:v);}  

  function updateView(state){
    const h = document.getElementById('val-hunger');
    const m = document.getElementById('val-mood');
    const a = document.getElementById('val-aff');
    const st = document.getElementById('val-status');
    const bh = document.getElementById('bar-hunger');
    const bm = document.getElementById('bar-mood');
    const ba = document.getElementById('bar-aff');
    const sub = document.getElementById('subtitle');
    const btnDnd = document.getElementById('btn-dnd-popup');
    if(!state){
      h.textContent=m.textContent=a.textContent=st.textContent='--';
      bh.style.width=bm.style.width=ba.style.width='0%';
      sub.textContent='尚未创建 Kaka 状态';
      btnDnd.textContent='🔕 勿扰';
      return;
    }
    h.textContent = Math.round(state.hunger);
    m.textContent = Math.round(state.mood);
    a.textContent = Math.round(state.affinity||0);
    bh.style.width = clamp(state.hunger,0,100) + '%';
    bm.style.width = clamp(state.mood,0,100) + '%';
    ba.style.width = clamp(state.affinity||0,0,100) + '%';
    const hungry = state.hunger < 35;
    const lowMood = state.mood < 40;
    if(hungry && lowMood) st.textContent = '很饿又有点丧，快去安慰下';
    else if(hungry) st.textContent = '有点饿了，喂点东西？';
    else if(lowMood) st.textContent = '心情一般，多摸摸头~';
    else st.textContent = '状态不错，在页面底部乱逛中';
    sub.textContent = '浏览器内的小 Kaka · 数据本地持久化';
    btnDnd.textContent = state.dnd ? '🔔 关闭勿扰' : '🔕 开启勿扰';
  }

  function loadState(cb){
    if(!chrome || !chrome.storage || !chrome.storage.local){ cb(null); return; }
    chrome.storage.local.get(STORAGE_KEY, function(data){
      cb(data && data[STORAGE_KEY] ? data[STORAGE_KEY] : null);
    });
  }

  function saveState(state){
    if(!chrome || !chrome.storage || !chrome.storage.local) return;
    state.lastUpdated = Date.now();
    chrome.storage.local.set({ [STORAGE_KEY]: state });
  }

  function withState(mutator){
    loadState(function(state){
      state = state || { hunger:70, mood:75, affinity:10, dnd:false, lastUpdated:Date.now(), personality:'extrovert' };
      mutator(state);
      saveState(state);
      updateView(state);
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    loadState(updateView);
    document.getElementById('btn-feed-popup').addEventListener('click', function(){
      withState(function(s){
        s.hunger = clamp(s.hunger + 25,0,100);
        s.mood = clamp(s.mood + 6,0,100);
      });
    });
    document.getElementById('btn-pat-popup').addEventListener('click', function(){
      withState(function(s){
        s.mood = clamp(s.mood + 6,0,100);
        s.affinity = clamp((s.affinity||0) + 3,0,100);
      });
    });
    document.getElementById('btn-dnd-popup').addEventListener('click', function(){
      withState(function(s){ s.dnd = !s.dnd; });
    });
    document.getElementById('btn-signin-popup').addEventListener('click', function(){
      // 简单提示：真正的连续签到逻辑在 Web 端 demo 里，这里只给一点零食作为彩蛋。
      withState(function(s){
        s.mood = clamp(s.mood + 4,0,100);
        s.affinity = clamp((s.affinity||0) + 1,0,100);
      });
      alert('🎁 今日签到：Kaka 心情 +4 · 好感度 +1（详细签到系统请在 Web 版中查看）');
    });
  });
})();
