const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('kaka', {
  setClickThrough: (v)=> ipcRenderer.send('kaka:click-through', v),
  quit: ()=> ipcRenderer.send('kaka:quit'),
  isElectron: true,
});
