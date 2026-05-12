const { app, BrowserWindow, Tray, Menu, nativeImage, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');

// ─── Config ──────────────────────────────────────────────────────────────────

const CONFIG_PATH = path.join(__dirname, 'storage', 'device_configs.json');

function loadConfigs() {
  if (!fs.existsSync(CONFIG_PATH)) return [];
  try {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  } catch (e) {
    console.error('Failed to load configs:', e);
    return [];
  }
}

function saveConfigs(configs) {
  fs.mkdirSync(path.dirname(CONFIG_PATH), { recursive: true });
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(configs, null, 2));
}

// ─── MIDI ─────────────────────────────────────────────────────────────────────

let JZZ = null;
let midiInputs = {}; // keyed by port name

function initMidi() {
  try {
    JZZ = require('jzz');
    console.log('JZZ loaded successfully');
  } catch (e) {
    console.warn('JZZ not available:', e.message);
  }
}

async function getMidiPortNames() {
  if (!JZZ) return [];
  try {
    const engine = await JZZ();
    const info = await engine.info();
    return info.inputs.map(i => i.name);
  } catch (e) {
    console.warn('Failed to get MIDI ports:', e.message);
    return [];
  }
}

async function openMidiPort(portName) {
  if (!JZZ) return;
  if (midiInputs[portName]) return;

  try {
    const engine = await JZZ();
    const port = await engine.openMidiIn(portName);

    port.connect((msg) => {
      let event = null;

      // note on
      if (msg.isNoteOn()) {
        event = {
          type: 'midi',
          device: portName,
          message: {
            type: 'noteon',
            note: msg[1],
            value: msg[2],
            channel: msg[0] & 0x0f
          }
        };
      }
      // note off
      else if (msg.isNoteOff()) {
        event = {
          type: 'midi',
          device: portName,
          message: {
            type: 'noteoff',
            note: msg[1],
            value: msg[2],
            channel: msg[0] & 0x0f
          }
        };
      }
      // control change (knobs, faders)
      else if (msg.isControl()) {
        event = {
          type: 'midi',
          device: portName,
          message: {
            type: 'controlchange',
            control: msg[1],
            value: msg[2],
            channel: msg[0] & 0x0f
          }
        };
      }

      if (event) {
        if (mainWindow && !mainWindow.isDestroyed()) {
          mainWindow.webContents.send('raw-input-event', event);
        }
        handleMappingExecution(event);
      }
    });

    midiInputs[portName] = port;
    console.log('Opened MIDI port:', portName);
  } catch (e) {
    console.warn('Failed to open MIDI port:', portName, e.message);
  }
}

async function closeMidiPort(portName) {
  if (midiInputs[portName]) {
    try {
      await midiInputs[portName].close();
    } catch (e) {}
    delete midiInputs[portName];
    console.log('Closed MIDI port:', portName);
  }
}

async function closeAllMidiPorts() {
  for (const name of Object.keys(midiInputs)) {
    await closeMidiPort(name);
  }
}

// ─── Mapping Execution ────────────────────────────────────────────────────────

function handleMappingExecution(event) {
  const configs = loadConfigs();

  for (const config of configs) {
    const device = config?.device;
    const mappings = config?.config?.mappings;
    if (!device || !mappings) continue;

    // Match device name
    if (device.name !== event.device) continue;

    for (const mapping of mappings) {
      if (!mappingMatches(mapping.input, event)) continue;
      executeAction(mapping.action);
    }
  }
}

function mappingMatches(mappingInput, event) {
  if (!mappingInput || !event.message) return false;

  const msg = event.message;

  // Must match message type
  if (mappingInput.type !== msg.type) return false;

  // For notes: match note number
  if (msg.type === 'noteon' || msg.type === 'noteoff') {
    return mappingInput.note === msg.note;
  }

  // For CC: match control number
  if (msg.type === 'controlchange') {
    return mappingInput.control === msg.control;
  }

  return false;
}

function executeAction(action) {
  if (!action) return;

  switch (action.type) {
    case 'shortcut':
      executeShortcut(action.keys);
      break;
    case 'volume_master':
      setMasterVolume(action.value);
      break;
    case 'volume_app':
      setAppVolume(action.appName, action.value);
      break;
    case 'media':
      executeMediaKey(action.key);
      break;
    default:
      console.warn('Unknown action type:', action.type);
  }
}

// ─── Keyboard Shortcuts ───────────────────────────────────────────────────────

function executeShortcut(keys) {
  // keys is an array like ['ctrl', 'shift', 'a']
  try {
    const robot = require('robotjs');
    const modifiers = [];
    let mainKey = null;

    const modMap = { ctrl: 'control', shift: 'shift', alt: 'alt', win: 'command' };

    for (const key of keys) {
      const lower = key.toLowerCase();
      if (modMap[lower]) modifiers.push(modMap[lower]);
      else mainKey = lower;
    }

    if (mainKey) {
      robot.keyTap(mainKey, modifiers);
    }
  } catch (e) {
    console.warn('robotjs not available:', e.message);
  }
}

function executeMediaKey(key) {
  // key: 'play_pause' | 'next' | 'prev' | 'mute'
  try {
    const robot = require('robotjs');
    const keyMap = {
      play_pause: 'audio_play',
      next: 'audio_next',
      prev: 'audio_prev',
      mute: 'audio_mute',
      volume_up: 'audio_vol_up',
      volume_down: 'audio_vol_down',
    };
    if (keyMap[key]) robot.keyTap(keyMap[key]);
  } catch (e) {
    console.warn('robotjs not available:', e.message);
  }
}

// ─── Audio Control (Windows) ──────────────────────────────────────────────────

function setMasterVolume(value) {
  // value: 0.0 - 1.0 (or 0-127 from MIDI CC, normalise here)
  const normalised = value > 1 ? value / 127 : value;
  try {
    const { execSync } = require('child_process');
    // Uses nircmd if available, fallback to PowerShell
    const vol = Math.round(normalised * 65535);
    execSync(`nircmd.exe setsysvolume ${vol}`, { windowsHide: true });
  } catch {
    try {
      const { execSync } = require('child_process');
      const pct = Math.round(normalised * 100);
      execSync(
        `powershell -command "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"`,
        { windowsHide: true }
      );
      // A better approach once loudness npm package is installed:
      // const loudness = require('loudness');
      // loudness.setVolume(pct);
    } catch (e) {
      console.warn('Volume control failed:', e.message);
    }
  }
}

function setAppVolume(appName, value) {
  // Placeholder — requires native addon or loudness package
  // Will be wired up once loudness is installed
  console.log(`Set app volume: ${appName} → ${value}`);
}

// ─── IPC Handlers ─────────────────────────────────────────────────────────────

function registerIpcHandlers() {
  // Renderer asks for device list
  ipcMain.handle('get-devices', async () => {
    const devices = { midi: [], keyboard: [], other: [] };

    const portNames = await getMidiPortNames();
    portNames.forEach((name, index) => {
        devices.midi.push({
        index,
        name,
        config: { displayName: name, logo: 'piano', active: false }
        });
    });

    return devices;
    });

  // Renderer asks to open a MIDI port
  ipcMain.handle('open-midi-port', async (_, portName) => {
    await openMidiPort(portName);
    return { success: true };
    });

    ipcMain.handle('close-midi-port', async (_, portName) => {
    await closeMidiPort(portName);
    return { success: true };
    });

  // Config CRUD
  ipcMain.handle('get-configs', () => loadConfigs());

  ipcMain.handle('save-config', (_, config) => {
    const configs = loadConfigs();
    const deviceId = `${config.device.type}_${config.device.name.replace(/\s/g, '')}`;

    const idx = configs.findIndex(c => {
      const d = c.device;
      return d && `${d.type}_${d.name.replace(/\s/g, '')}` === deviceId;
    });

    if (idx >= 0) configs[idx] = config;
    else configs.push(config);

    saveConfigs(configs);
    return { success: true };
  });

  ipcMain.handle('delete-config', (_, deviceId) => {
    const configs = loadConfigs().filter(c => {
      const d = c.device;
      return d && `${d.type}_${d.name.replace(/\s/g, '')}` !== deviceId;
    });
    saveConfigs(configs);
    return { success: true };
  });

  // Window controls (for frameless window later)
  ipcMain.on('window-minimize', () => mainWindow?.minimize());
  ipcMain.on('window-close', () => mainWindow?.hide()); // hide to tray, not close
}

// ─── Window ───────────────────────────────────────────────────────────────────

let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1100,
    height: 700,
    minWidth: 800,
    minHeight: 500,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    // Uncomment for frameless later:
    // frame: false,
    show: false, // don't flash on startup
  });

  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:9000');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'));
  }

  mainWindow.once('ready-to-show', () => mainWindow.show());

  // Intercept close → hide to tray instead
  mainWindow.on('close', (e) => {
    if (!app.isQuitting) {
      e.preventDefault();
      mainWindow.hide();
    }
  });
}

// ─── Tray ─────────────────────────────────────────────────────────────────────

let tray = null;

function createTray() {
  // Use a 16x16 PNG from your assets, or generate a simple one
  const iconPath = path.join(__dirname, 'src', 'Assets', 'tray-icon.png');
  const icon = fs.existsSync(iconPath)
    ? nativeImage.createFromPath(iconPath)
    : nativeImage.createEmpty();

  tray = new Tray(icon);
  tray.setToolTip('MIDI Shortcut');

  const menu = Menu.buildFromTemplate([
    {
      label: 'Show',
      click: () => {
        mainWindow?.show();
        mainWindow?.focus();
      }
    },
    { type: 'separator' },
    {
      label: 'Quit',
      click: () => {
        app.isQuitting = true;
        app.quit();
      }
    }
  ]);

  tray.setContextMenu(menu);
  tray.on('double-click', () => {
    mainWindow?.show();
    mainWindow?.focus();
  });
}

// ─── App Lifecycle ────────────────────────────────────────────────────────────

app.whenReady().then(() => {
  initMidi();
  registerIpcHandlers();
  createWindow();
  createTray();

  // Auto-open all MIDI ports that have saved configs marked active
  const configs = loadConfigs();
    for (const config of configs) {
    if (config?.config?.active && config?.device?.type === 'midi') {
        openMidiPort(config.device.name);
    }
    }
});

app.on('window-all-closed', () => {
  // Do nothing — keep running in tray
});

app.on('activate', () => {
  // macOS: re-show if dock icon clicked (not really needed for Windows-only)
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

app.on('before-quit', () => {
  app.isQuitting = true;
  closeAllMidiPorts();
});