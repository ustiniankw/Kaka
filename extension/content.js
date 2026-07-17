// Kaka Chrome 扩展 · 薄壳（thin shell）内容脚本
// 所有 UI / 物理 / 交互逻辑都在 https://ustiniankw.github.io/Kaka/embed.html
// 本脚本仅负责：注入 iframe、桥接 chrome.storage、代理打开外链。
(function () {
  if (typeof window === 'undefined') return;
  try { if (window.top !== window) return; } catch (e) { return; }
  if (!document.documentElement) return;
  if (document.getElementById('kaka-ext-container')) return;

  var STORAGE_KEY = 'kaka_state_v1';
  // 使用当天日期作为 cache-buster：既能吃到 GH Pages 的 CDN 缓存，又能保证每天最多滞后一天更新。
  var day = new Date().toISOString().slice(0, 10);
  var IFRAME_URL = 'https://ustiniankw.github.io/Kaka/embed.html?ts=' + encodeURIComponent(day);

  function mount() {
    if (document.getElementById('kaka-ext-container')) return;
    var container = document.createElement('div');
    container.id = 'kaka-ext-container';
    var iframe = document.createElement('iframe');
    iframe.id = 'kaka-ext-frame';
    iframe.src = IFRAME_URL;
    iframe.setAttribute('title', 'Kaka');
    iframe.setAttribute('allowtransparency', 'true');
    iframe.setAttribute('scrolling', 'no');
    container.appendChild(iframe);
    document.body.appendChild(container);
  }

  function isFromKakaFrame(event) {
    var iframe = document.getElementById('kaka-ext-frame');
    return iframe && event.source === iframe.contentWindow;
  }

  function safePost(msg) {
    var iframe = document.getElementById('kaka-ext-frame');
    if (iframe && iframe.contentWindow) {
      try { iframe.contentWindow.postMessage(msg, '*'); } catch (e) {}
    }
  }

  window.addEventListener('message', function (event) {
    var data = event && event.data;
    if (!data || typeof data !== 'object' || !data.type) return;
    if (!isFromKakaFrame(event)) return;

    if (data.type === 'kaka:getState') {
      if (chrome && chrome.storage && chrome.storage.local) {
        chrome.storage.local.get(STORAGE_KEY, function (res) {
          safePost({ type: 'kaka:state', payload: (res && res[STORAGE_KEY]) || null, reqId: data.reqId });
        });
      } else {
        safePost({ type: 'kaka:state', payload: null, reqId: data.reqId });
      }
    } else if (data.type === 'kaka:setState') {
      if (chrome && chrome.storage && chrome.storage.local) {
        var payload = data.payload || {};
        payload.lastUpdated = Date.now();
        var obj = {}; obj[STORAGE_KEY] = payload;
        chrome.storage.local.set(obj);
      }
    } else if (data.type === 'kaka:open') {
      try { window.open(String(data.url || ''), '_blank', 'noopener,noreferrer'); } catch (e) {}
    } else if (data.type === 'kaka:resize') {
      var el = document.getElementById('kaka-ext-container');
      if (el) {
        var w = Math.max(80, Math.min(600, +data.w || 260));
        var h = Math.max(80, Math.min(600, +data.h || 210));
        el.style.width = w + 'px';
        el.style.height = h + 'px';
      }
    }
  }, false);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
