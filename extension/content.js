// Kaka Chrome 扩展 · 薄壳（thin shell）内容脚本
// 所有 UI / 物理 / 交互逻辑优先从 https://ustiniankw.github.io/Kaka/embed.html 远端加载。
// 如果 GH Pages 暂时不可达，则自动回退到扩展内置 embed.html。
//
// v1.3.0：容器扩为整个视口，iframe 本身 pointer-events:none；
//   父页面上放一个 hitbox 元素（只覆盖 Kaka 当前包围盒或菜单区域），
//   将鼠标事件通过 postMessage 转发到 iframe。这样 Kaka 可以在整块视口
//   自由漫游、拥有真实重力，同时页面滚动/点击不会被劫持。
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

  function getFrame() { return document.getElementById('kaka-ext-frame'); }
  function getHitbox() { return document.getElementById('kaka-ext-hitbox'); }
  function getStatusBadge() { return document.getElementById('kaka-ext-status'); }

  function showStatusBadge(text) {
    var badge = getStatusBadge();
    if (!badge) return;
    badge.textContent = text;
    badge.classList.add('show');
    clearTimeout(boot.badgeTimer);
    boot.badgeTimer = setTimeout(function () { badge.classList.remove('show'); }, BADGE_HIDE_DELAY);
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
    if (iframe) iframe.src = LOCAL_IFRAME_URL;
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
    boot.healthTimeout = setTimeout(function () { controller.abort(); }, REMOTE_CHECK_TIMEOUT - 200);
    fetch(REMOTE_IFRAME_URL, { method: 'GET', cache: 'no-store', credentials: 'omit', signal: controller.signal })
      .then(function (response) {
        clearTimeout(boot.healthTimeout);
        boot.remoteReachable = !!(response && response.ok);
        if (!boot.remoteReachable && !boot.iframeReady) fallbackToLocal(FALLBACK_MESSAGE);
      }).catch(function () {
        clearTimeout(boot.healthTimeout);
        boot.remoteReachable = false;
        if (!boot.iframeReady) fallbackToLocal(FALLBACK_MESSAGE);
      });
  }

  // ---------- Hitbox helpers ----------
  var FORWARD_EVENTS = ['mousedown', 'mouseup', 'mousemove', 'click', 'dblclick', 'contextmenu', 'wheel'];
  function attachHitboxHandlers(hitbox) {
    FORWARD_EVENTS.forEach(function (evName) {
      hitbox.addEventListener(evName, function (e) {
        if (evName === 'contextmenu') e.preventDefault();
        safePost({
          type: 'kaka:pointer',
          event: evName,
          clientX: e.clientX,
          clientY: e.clientY,
          button: (typeof e.button === 'number') ? e.button : 0,
          buttons: (typeof e.buttons === 'number') ? e.buttons : 0,
          shiftKey: !!e.shiftKey,
          ctrlKey: !!e.ctrlKey,
          altKey: !!e.altKey,
          metaKey: !!e.metaKey,
          deltaX: e.deltaX || 0,
          deltaY: e.deltaY || 0
        });
      }, { passive: false });
    });

    // 触摸支持（简单映射为 mousedown/move/up）
    var touchActive = false;
    hitbox.addEventListener('touchstart', function (e) {
      if (!e.touches || !e.touches[0]) return;
      touchActive = true;
      var t = e.touches[0];
      safePost({ type: 'kaka:pointer', event: 'mousedown', clientX: t.clientX, clientY: t.clientY, button: 0, buttons: 1 });
    }, { passive: true });
    hitbox.addEventListener('touchmove', function (e) {
      if (!touchActive || !e.touches[0]) return;
      var t = e.touches[0];
      safePost({ type: 'kaka:pointer', event: 'mousemove', clientX: t.clientX, clientY: t.clientY, button: 0, buttons: 1 });
    }, { passive: true });
    hitbox.addEventListener('touchend', function (e) {
      if (!touchActive) return;
      touchActive = false;
      var t = (e.changedTouches && e.changedTouches[0]) || null;
      var cx = t ? t.clientX : 0, cy = t ? t.clientY : 0;
      safePost({ type: 'kaka:pointer', event: 'mouseup', clientX: cx, clientY: cy, button: 0, buttons: 0 });
      safePost({ type: 'kaka:pointer', event: 'click', clientX: cx, clientY: cy, button: 0, buttons: 0 });
    });
  }

  function updateHitbox(rect, fullscreen) {
    var hb = getHitbox();
    if (!hb) return;
    if (fullscreen) {
      hb.classList.add('kaka-hb-fullscreen');
      hb.style.display = 'block';
      return;
    }
    hb.classList.remove('kaka-hb-fullscreen');
    if (!rect || rect.w <= 0 || rect.h <= 0) {
      hb.style.display = 'none';
      return;
    }
    hb.style.left = Math.round(rect.x) + 'px';
    hb.style.top = Math.round(rect.y) + 'px';
    hb.style.width = Math.round(rect.w) + 'px';
    hb.style.height = Math.round(rect.h) + 'px';
    hb.style.display = 'block';
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

    var hitbox = document.createElement('div');
    hitbox.id = 'kaka-ext-hitbox';
    hitbox.setAttribute('aria-hidden', 'true');

    container.appendChild(iframe);
    container.appendChild(hitbox);
    container.appendChild(badge);
    document.body.appendChild(container);

    attachHitboxHandlers(hitbox);
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
      // 通知 iframe：告诉它父页面视口尺寸，方便远端首帧对齐
      safePost({ type: 'kaka:viewport', w: window.innerWidth, h: window.innerHeight });
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
    } else if (data.type === 'kaka:hitbox') {
      // iframe 每帧上报 Kaka 命中区域（视口坐标）
      updateHitbox(data.rect || null, !!data.fullscreen);
    } else if (data.type === 'kaka:resize') {
      // 兼容旧协议：忽略窗口大小请求（现在始终全屏）
    }
  }, false);

  window.addEventListener('resize', function () {
    safePost({ type: 'kaka:viewport', w: window.innerWidth, h: window.innerHeight });
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
