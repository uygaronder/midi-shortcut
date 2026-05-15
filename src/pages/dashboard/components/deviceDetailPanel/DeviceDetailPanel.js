// src/components/InputDetailPanel.js
import React, { useState, useEffect } from 'react';
import '../../../../Assets/CSS/pages/dashboard/components/DeviceDetailPanel.css';

import DeviceKeybinds from '../deviceKeybinds/DeviceKeybinds';

import { useRawInput } from '../../../../contexts/rawInputContext';
import { deviceIcons } from '../../../../utils/logos';

import Chevron from '../../../../Assets/SVG/chevron-up.svg';


const DeviceDetailPanel = ({ selectedDevice, onBack }) => {
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

    useEffect(() => {
        setDeviceName(selectedDevice.config.displayName);
        setDeviceRawEvent(null);

        // Open the MIDI port when device is selected
        if (window.electronAPI && selectedDevice.name) {
            window.electronAPI.openMidiPort(selectedDevice.name)
                .then(() => console.log('MIDI port opened:', selectedDevice.name))
                .catch(err => console.error('Failed to open MIDI port:', err));
        }

        // Close the port when we switch away
        return () => {
            if (window.electronAPI && selectedDevice.name) {
                window.electronAPI.closeMidiPort(selectedDevice.name);
            }
        };
    }, [selectedDevice]);

    return (
        <div className='device-detail-panel'>
            <div className='device-info'>
                <button className='back-button button-2' onClick={onBack}>
                    <img src={Chevron} alt='Back' className='svg' />
                </button>
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
            <DeviceKeybinds deviceRawEvent={deviceRawEvent} />
        </div>
    );
}

export default DeviceDetailPanel;