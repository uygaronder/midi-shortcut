import React, { useState, useEffect } from 'react';

import '../../../Assets/CSS/pages/dashboard/components/AvailableDevices.css';

import Keyboard from "../../../Assets/SVG/keyboard.svg";
import Piano from "../../../Assets/SVG/piano.svg";
import Mouse from "../../../Assets/SVG/mouse.svg";
import Gamepad from "../../../Assets/SVG/gamepad.svg";

import { useRawInput } from '../../../contexts/rawInputContext';



const AvailableDevices = ({ onSelectDevice }) => {
    const [devices, setDevices] = useState([]);
    useEffect(() => {
        fetch("http://localhost:5000/devices/")
          .then((res) => res.json())
          .then((data) => {
            setDevices(data);
          })
          .catch((err) => console.error("Error fetching devices:", err));
      }, []);

    const rawEvent = useRawInput();
    const [glowMap, setGlowMap] = useState({});

    React.useEffect(() => {
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
            <h3>Available Devices</h3>
            <div className='devices'>
                {Object.keys(devices).map((deviceType) => (
                    devices[deviceType].map((device) => {
                        const isGlowing = glowMap[device.name];                    
                        return (
                        <div key={device.name} className={`device ${isGlowing ? 'glow' : ''}`} onClick={() => onSelectDevice(device)}>
                          <span className='device-logo'>
                            {deviceType === 'keyboard' && <img src={Keyboard} className='svg' alt='Keyboard' />}
                            {deviceType === 'midi' && <img src={Piano} className='svg' alt='Piano' />}
                            {deviceType === 'other' && <img src={Mouse} className='svg' alt='Mouse' />}
                            {deviceType === 'gamepad' && <img src={Gamepad} className='svg' alt='Gamepad' />}
                          </span>
                          <span className='device-nickname'>Unnamed Device</span>
                          <span className='device-name' title={device}>{device.name.substring(0, 25) + "..."}</span>
                        </div>
                      )})
                ))}
            </div>
        </div>
    );
};

export default AvailableDevices;