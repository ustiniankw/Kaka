const { app, BrowserWindow, Tray, Menu, ipcMain, screen, shell, globalShortcut } = require('electron');
const path = require('path');
const fs = require('fs');

const REMOTE_URL = 'https://ustiniankw.github.io/Kaka/embed-desktop.html';
// dev override: file:///.../docs/embed-desktop.html via KAKA_DEV env

let win, tray;
let clickThrough = false;

// -------- persisted preferences (top-level / desktop-level) --------
const CONFIG_DIR = app.getPath('userData');
const CONFIG_PATH = path.join(CONFIG_DIR, 'kaka-desktop-config.json');

function loadConfig() {
  try {
    const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
    const obj = JSON.parse(raw);
    if (obj && typeof obj === 'object') return obj;
  } catch (e) { /* first run */ }
  return {};
}
function saveConfig(patch) {
  try {
    const cur = loadConfig();
    const next = Object.assign({}, cur, patch);
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(next, null, 2), 'utf8');
    return next;
  } catch (e) { return null; }
}

// alwaysOnTop: true = 顶层（永远在最前，默认）; false = 桌面层（其他窗口可覆盖）
const prefs = Object.assign({ alwaysOnTop: true }, loadConfig());

function applyTopMode(enabled) {
  prefs.alwaysOnTop = !!enabled;
  saveConfig({ alwaysOnTop: prefs.alwaysOnTop });
  if (!win) return;
  if (prefs.alwaysOnTop) {
    win.setAlwaysOnTop(true, 'screen-saver');
    win.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });
  } else {
    win.setAlwaysOnTop(false);
    win.setVisibleOnAllWorkspaces(false);
  }
  if (tray) rebuildTrayMenu();
}

function createWindow() {
  const display = screen.getPrimaryDisplay();
  const { width, height } = display.workAreaSize;

  win = new BrowserWindow({
    width, height,
    x: 0, y: 0,
    frame: false,
    transparent: true,
    resizable: false,
    movable: false,
    hasShadow: false,
    alwaysOnTop: prefs.alwaysOnTop,
    skipTaskbar: true,
    focusable: true,
    backgroundColor: '#00000000',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    }
  });

  if (prefs.alwaysOnTop) {
    win.setAlwaysOnTop(true, 'screen-saver');
    win.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });
  } else {
    win.setAlwaysOnTop(false);
    win.setVisibleOnAllWorkspaces(false);
  }

  // Start with mouse events enabled; toggle click-through via tray menu or IPC.
  win.setIgnoreMouseEvents(false);

  const url = process.env.KAKA_DEV
    ? 'file://' + path.join(__dirname, '..', 'docs', 'embed-desktop.html')
    : REMOTE_URL;
  win.loadURL(url);

  // If remote load fails, fall back to a local minimal HTML that shows a retry button.
  win.webContents.on('did-fail-load', (_e, _code, _desc) => {
    win.loadFile(path.join(__dirname, 'fallback.html'));
  });
}

function setClickThrough(v) {
  clickThrough = v;
  if (win) win.setIgnoreMouseEvents(v, { forward: true });
}

function rebuildTrayMenu() {
  if (!tray) return;
  const menu = Menu.buildFromTemplate([
    { label: '🐱 Kaka 桌面宠物', enabled: false },
    { type: 'separator' },
    {
      label: '窗口层级',
      submenu: [
        {
          label: '顶层（永远在最前）',
          type: 'radio',
          checked: prefs.alwaysOnTop === true,
          click: () => applyTopMode(true)
        },
        {
          label: '桌面层（其他窗口可覆盖）',
          type: 'radio',
          checked: prefs.alwaysOnTop === false,
          click: () => applyTopMode(false)
        }
      ]
    },
    { label: '穿透模式（不响应点击）', type: 'checkbox', checked: clickThrough, click: (i) => setClickThrough(i.checked) },
    { label: '重新加载', click: () => win && win.reload() },
    { type: 'separator' },
    { label: '打开 GitHub', click: () => shell.openExternal('https://github.com/ustiniankw/Kaka') },
    { label: '打开 Web 版', click: () => shell.openExternal('https://ustiniankw.github.io/Kaka/') },
    { type: 'separator' },
    { label: '退出', role: 'quit' },
  ]);
  tray.setToolTip('Kaka 桌面宠物 · ' + (prefs.alwaysOnTop ? '顶层' : '桌面层'));
  tray.setContextMenu(menu);
}

function createTray() {
  const iconPath = path.join(__dirname, 'build', 'tray.png');
  tray = new Tray(iconPath);
  rebuildTrayMenu();
}

app.whenReady().then(() => {
  createWindow();
  createTray();
  // Global boss-key: Ctrl+Shift+H → hide/show
  globalShortcut.register('CommandOrControl+Shift+H', () => {
    if (!win) return;
    if (win.isVisible()) win.hide(); else win.show();
  });
});
app.on('window-all-closed', () => { /* keep alive via tray */ });
app.on('will-quit', () => globalShortcut.unregisterAll());

// IPC bridge from renderer for future features
ipcMain.on('kaka:click-through', (_e, v) => setClickThrough(!!v));
ipcMain.on('kaka:quit', () => app.quit());
ipcMain.on('kaka:top-mode', (_e, v) => applyTopMode(!!v));
