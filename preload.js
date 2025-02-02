// preload.js
// This file is executed before your renderer process loads.
// You can expose a safe API here if needed.

console.log('Preload script loaded successfully.');

// If you're using contextBridge, you might do:
// const { contextBridge, ipcRenderer } = require('electron');
// contextBridge.exposeInMainWorld('electronAPI', {
//   sendMessage: (message) => ipcRenderer.send('message', message)
// });
