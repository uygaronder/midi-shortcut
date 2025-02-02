// src/components/InputDetailPanel.js
import React, { useState, useEffect } from 'react';
import '../../../../Assets/CSS/pages/dashboard/components/DeviceDetailPanel.css';

import { useRawInput } from '../../../../contexts/rawInputContext';
import { deviceIcons } from '../../../../utils/logos';


const DeviceDetailPanel = ({ selectedDevice }) => {
    const [deviceName, setDeviceName] = useState(selectedDevice.config.displayName);
    const [deviceRawEvent, setDeviceRawEvent] = useState(null);
    const rawEvent = useRawInput();

    useEffect(() => {
        setDeviceName(selectedDevice.config.displayName);
        setDeviceRawEvent(null);
    }, [selectedDevice]);

    useEffect(() => {
        if (rawEvent && rawEvent.device === selectedDevice.name) {
            setDeviceRawEvent(rawEvent);
        }
    }, [rawEvent, selectedDevice]);

    const handleDeviceNameChange = (e) => {
        setDeviceName(e.target.value);
    };

    return (
        <div className='device-detail-panel'>
            <div className='device-info'>
                <div className='device-logo'>
                    <img src={selectedDevice.config.logo == "" ? deviceIcons.keyboard : deviceIcons[selectedDevice.config.logo]} className='svg' alt={`${selectedDevice.name} logo`} />
                </div>
                <div className='device-edit-inputs'>
                    <input type='text' placeholder='Device Name' value={deviceName} onChange={(e) => handleDeviceNameChange(e)} />
                </div>
                <div className='device-settings'>
                    <div className='device-active-switch'>
                        <label htmlFor='device-active-switch'>Active</label>
                        <input type='checkbox' id='device-active-switch' />
                    </div>
                </div>
            </div>
            <div className='device-input'>
                <div className='last-detected-input'>
                    <h3>Last Detected Input</h3>
                    <div className='input-info'>
                        <div className='input-value'>{deviceRawEvent?.message.type}</div>
                        <div className='input-value'>{deviceRawEvent?.message.control}</div>
                        <div className='input-value'>{deviceRawEvent?.message.value}</div>
                        <div className='input-value'>{deviceRawEvent?.message.note}</div>
                    </div>
                </div>

            </div>
        </div>
    );
}

export default DeviceDetailPanel;