const { ipcRenderer } = require('electron');

// Import the necessary modules


// DOM elements
const button = document.getElementById('myButton');

// Event listener for button click
button.addEventListener('click', () => {
    // Send a message to the main process
    ipcRenderer.send('buttonClicked');
});

// Event listener for receiving messages from the main process
ipcRenderer.on('messageFromMain', (event, message) => {
    // Handle the received message
    console.log('Received message from main process:', message);
});