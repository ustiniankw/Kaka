// Kaka Chrome 扩展 · 薄壳（thin shell）内容脚本
// 所有 UI / 物理 / 交互逻辑优先从 https://ustiniankw.github.io/Kaka/embed.html 远端加载。
// 如果 GH Pages 暂时不可达，则自动回退到扩展内置 embed.html。
(function () {
  if (typeof window === 'undefined') return;
  try { if (window.top !== window) return; } catch (e) { return; }
  if (!document.documentElement) return;
  if (document.getElementById('kaka-ext-container')) return;

  var STORAGE_KEY = 'kaka_state_v1';
  var day = new Date().toISOString().slice(0, 10);
  var REMOTE_IFRAME_URL = 'https://ustiniankw.github.io/Kaka/embed.html?ts=' + encodeURIComponent(day);
  var LOCAL_IFRAME_URL = (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.getURL)
    ? chrome.runtime.getURL('embed.html') + '?fallback=1&ts=' + encodeURIComponent(day)
    : '';
  var FALLBACK_MESSAGE = 'Kaka 加载失败：已切到本地备用模式（GH Pages 未就绪）';
  var REMOTE_CHECK_TIMEOUT = 3000;
  var BADGE_HIDE_DELAY = 8000;

  var boot = {
    iframeReady: false,
    remoteReachable: null,
    didFallback: false,
    fallbackTimer: null,
    badgeTimer: null,
    healthTimeout: null
  };

  function getFrame() {
    return document.getElementById('kaka-ext-frame');
  }

  function getStatusBadge() {
    return document.getElementById('kaka-ext-status');
  }

  function showStatusBadge(text) {
    var badge = getStatusBadge();
    if (!badge) return;
    badge.textContent = text;
    badge.classList.add('show');
    clearTimeout(boot.badgeTimer);
    boot.badgeTimer = setTimeout(function () {
      badge.classList.remove('show');
    }, BADGE_HIDE_DELAY);
  }

  function clearFallbackTimer() {
    clearTimeout(boot.fallbackTimer);
    boot.fallbackTimer = null;
  }

  function completeRemoteBoot() {
    boot.iframeReady = true;
    clearFallbackTimer();
  }

  function fallbackToLocal(reason) {
    if (boot.didFallback || !LOCAL_IFRAME_URL) return;
    boot.didFallback = true;
    clearFallbackTimer();
    var iframe = getFrame();
    if (iframe) {
      iframe.src = LOCAL_IFRAME_URL;
    }
    showStatusBadge(reason || FALLBACK_MESSAGE);
  }

  function armFallbackTimer() {
    clearFallbackTimer();
    boot.fallbackTimer = setTimeout(function () {
      if (boot.iframeReady || boot.remoteReachable === true) return;
      fallbackToLocal(FALLBACK_MESSAGE);
    }, REMOTE_CHECK_TIMEOUT);
  }

  function probeRemoteAvailability() {
    if (typeof fetch !== 'function') return;
    if (typeof AbortController === 'undefined') return;

    var controller = new AbortController();
    boot.healthTimeout = setTimeout(function () {
      controller.abort();
    }, REMOTE_CHECK_TIMEOUT - 200);

    fetch(REMOTE_IFRAME_URL, {
      method: 'GET',
      cache: 'no-store',
      credentials: 'omit',
      signal: controller.signal
    }).then(function (response) {
      clearTimeout(boot.healthTimeout);
      boot.remoteReachable = !!(response && response.ok);
      if (!boot.remoteReachable && !boot.iframeReady) {
        fallbackToLocal(FALLBACK_MESSAGE);
      }
    }).catch(function () {
      clearTimeout(boot.healthTimeout);
      boot.remoteReachable = false;
      if (!boot.iframeReady) {
        fallbackToLocal(FALLBACK_MESSAGE);
      }
    });
  }

  function mount() {
    if (document.getElementById('kaka-ext-container')) return;
    if (!document.body) return;

    var container = document.createElement('div');
    container.id = 'kaka-ext-container';

    var badge = document.createElement('div');
    badge.id = 'kaka-ext-status';
    badge.setAttribute('role', 'status');
    badge.setAttribute('aria-live', 'polite');

    var iframe = document.createElement('iframe');
    iframe.id = 'kaka-ext-frame';
    iframe.src = REMOTE_IFRAME_URL;
    iframe.setAttribute('title', 'Kaka');
    iframe.setAttribute('allowtransparency', 'true');
    iframe.setAttribute('scrolling', 'no');

    container.appendChild(badge);
    container.appendChild(iframe);
    document.body.appendChild(container);

    probeRemoteAvailability();
    armFallbackTimer();
  }

  function isFromKakaFrame(event) {
    var iframe = getFrame();
    return iframe && event.source === iframe.contentWindow;
  }

  function safePost(msg) {
    var iframe = getFrame();
    if (iframe && iframe.contentWindow) {
      try { iframe.contentWindow.postMessage(msg, '*'); } catch (e) {}
    }
  }

  window.addEventListener('message', function (event) {
    var data = event && event.data;
    if (!data || typeof data !== 'object' || !data.type) return;
    if (!isFromKakaFrame(event)) return;

    if (data.type === 'kaka:ready') {
      completeRemoteBoot();
      return;
    }

    if (data.type === 'kaka:getState') {
      if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
        chrome.storage.local.get(STORAGE_KEY, function (res) {
          safePost({ type: 'kaka:state', payload: (res && res[STORAGE_KEY]) || null, reqId: data.reqId });
        });
      } else {
        safePost({ type: 'kaka:state', payload: null, reqId: data.reqId });
      }
    } else if (data.type === 'kaka:setState') {
      if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
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
