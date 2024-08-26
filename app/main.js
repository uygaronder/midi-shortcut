const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let pythonProcess;

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    win.loadFile('app/index.html');
}

app.whenReady().then(() => {
    createWindow();

    // Start a Python script when the app is ready
    pythonProcess = spawn('python', ['backend/midi_handler.py']);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
    });

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        if (pythonProcess) pythonProcess.kill();
        app.quit();
    }
});

// Handle requests from the renderer process
ipcMain.on('run-python-script', (event, scriptPath, args) => {
    const script = spawn('python', [scriptPath, ...args]);

    script.stdout.on('data', (data) => {
        event.reply('python-output', data.toString());
    });

    script.stderr.on('data', (data) => {
        console.error(`Python error: ${data}`);
    });

    script.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
    });
});
