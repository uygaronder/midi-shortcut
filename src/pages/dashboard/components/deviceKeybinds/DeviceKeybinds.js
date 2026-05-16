import React from "react";

import '../../../../Assets/CSS/pages/dashboard/components/DeviceKeybinds.css';

const shortcuts = require('../../../../../storage/shortcuts.json');



const DeviceKeybinds = ({ deviceRawEvent }) => {
    return (
        <div className="device-keybinds">
            <div className="add-keybind-container">
                <button className="add-keybind-button button-1">Add Shortcut</button>
            </div>
            <div className="keybinds-list">
            </div>
        </div>
    );
}

export default DeviceKeybinds;