const { contextBridge, ipcRenderer } = require('electron');

// Everything exposed here becomes available in React as window.electronAPI
// The renderer cannot access Node/Electron directly — only what's listed here.

contextBridge.exposeInMainWorld('electronAPI', {

  // ─── Devices ───────────────────────────────────────────────────────────────

  // Get all available input devices (MIDI ports, keyboards, etc.)
  // Usage in React: const devices = await window.electronAPI.getDevices()
  getDevices: () => ipcRenderer.invoke('get-devices'),

  // Tell the main process to start listening on a MIDI port
  // Usage: await window.electronAPI.openMidiPort(0)
  openMidiPort: (portIndex) => ipcRenderer.invoke('open-midi-port', portIndex),

  // Tell the main process to stop listening on a MIDI port
  closeMidiPort: (portIndex) => ipcRenderer.invoke('close-midi-port', portIndex),


  // ─── Configs ───────────────────────────────────────────────────────────────

  // Load all saved device configs from storage/device_configs.json
  getConfigs: () => ipcRenderer.invoke('get-configs'),

  // Save or update a single device config
  // config shape: { device: { type, name }, config: { displayName, logo, color, active, mappings[] } }
  saveConfig: (config) => ipcRenderer.invoke('save-config', config),

  // Delete a device config by its ID string ("midi_DeviceName")
  deleteConfig: (deviceId) => ipcRenderer.invoke('delete-config', deviceId),


  // ─── Real-time Events ──────────────────────────────────────────────────────

  // Subscribe to raw input events (MIDI notes, CC, keyboard keys)
  // Usage:
  //   const unsub = window.electronAPI.onRawInputEvent((event) => { ... })
  //   unsub() // call this to stop listening (do this in useEffect cleanup)
  onRawInputEvent: (callback) => {
    const handler = (_, event) => callback(event);
    ipcRenderer.on('raw-input-event', handler);

    // Return an unsubscribe function
    return () => ipcRenderer.removeListener('raw-input-event', handler);
  },


  // ─── Window Controls ───────────────────────────────────────────────────────

  // These are for if you add a custom titlebar later (frame: false in main.js)
  minimizeWindow: () => ipcRenderer.send('window-minimize'),
  closeWindow: () => ipcRenderer.send('window-close'), // hides to tray

});