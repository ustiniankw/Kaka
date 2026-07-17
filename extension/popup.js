// Kaka 扩展 popup —— 只读 chrome.storage.local 中的最新状态，展示 3 个入口链接。
(function () {
  var STORAGE_KEY = 'kaka_state_v1';

  function render(state) {
    var vh = document.getElementById('v-hunger');
    var vm = document.getElementById('v-mood');
    var va = document.getElementById('v-aff');
    var sub = document.getElementById('subtitle');
    if (!state) {
      vh.textContent = vm.textContent = va.textContent = '--';
      sub.textContent = '尚未生成状态，去任意页面加载一次即可初始化。';
      return;
    }
    vh.textContent = Math.round(state.hunger != null ? state.hunger : 0);
    vm.textContent = Math.round(state.mood != null ? state.mood : 0);
    va.textContent = Math.round(state.affinity != null ? state.affinity : 0);
    if (state.dnd) {
      sub.textContent = '🔕 勿扰模式已开启';
    } else if ((state.hunger || 0) < 30) {
      sub.textContent = '有点饿了，去 web 版投喂它一下吧～';
    } else {
      sub.textContent = '状态良好 · 数据来自本地 chrome.storage';
    }
  }

  if (chrome && chrome.storage && chrome.storage.local) {
    chrome.storage.local.get(STORAGE_KEY, function (data) {
      render(data && data[STORAGE_KEY] ? data[STORAGE_KEY] : null);
    });
  } else {
    render(null);
  }
})();
