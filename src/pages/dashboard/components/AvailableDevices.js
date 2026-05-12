import React, { useState, useEffect } from 'react';

import '../../../Assets/CSS/pages/dashboard/components/AvailableDevices.css';

import { useRawInput } from '../../../contexts/rawInputContext';
import { deviceIcons } from '../../../utils/logos';

const AvailableDevices = ({ onSelectDevice }) => {
    const [devices, setDevices] = useState({});

    useEffect(() => {
        if (!window.electronAPI) return;

        window.electronAPI.getDevices().then((data) => {
            setDevices(data);
        }).catch((err) => console.error('Error fetching devices:', err));
    }, []);

    const rawEvent = useRawInput();
    const [glowMap, setGlowMap] = useState({});

    useEffect(() => {
        if (rawEvent && rawEvent.device) {
            const deviceName = rawEvent.device;
            setGlowMap((prev) => ({ ...prev, [deviceName]: true }));
            setTimeout(() => {
                setGlowMap((prev) => ({ ...prev, [deviceName]: false }));
            }, 500);
        }
    }, [rawEvent]);

    return (
        <div className='available-devices'>
            {/* <h3>Available Devices</h3> */}
            <div className='devices'>
                {Object.keys(devices).map((deviceType) => (
                    devices[deviceType].map((device) => {
                        const isGlowing = glowMap[device.name];
                        return (
                            <div key={device.name} className={`device ${isGlowing ? 'glow' : ''}`} onClick={() => onSelectDevice(device)}>
                                <span className='device-logo'>
                                    <img src={deviceIcons[device.config?.logo]} className='svg' alt={`${device.name} logo`} />
                                </span>
                                <span className='device-nickname'>{device.config?.displayName || 'Unnamed Device'}</span>
                                <span className='device-name' title={device.name}>{device.name.substring(0, 25)}...</span>
                            </div>
                        );
                    })
                ))}
            </div>
        </div>
    );
};

export default AvailableDevices;