// src/components/InputDetailPanel.js
import React, { useState, useEffect } from 'react';
import '../../../../Assets/CSS/pages/dashboard/components/DeviceDetailPanel.css';

import { useRawInput } from '../../../../contexts/rawInputContext';



const DeviceDetailPanel = ({ selectedDevice }) => {
    const rawEvent = useRawInput();

    const getLogoUrl = (deviceConfig, deviceType) => {
        // If the configuration includes a logoUrl, use it; otherwise, use a default.
        return deviceConfig && deviceConfig.logoUrl 
          ? deviceConfig.logoUrl 
          : `/static/logos/${deviceType}.svg`;
      };

    useEffect(() => {
        console.log("selectedDevice:", selectedDevice);
    }, [selectedDevice]);

    console.log("selectedDevice:", selectedDevice);

    return (
        <div className='device-detail-panel'>
            <div className='device-info'>
                <div className='device-logo'>
                    <img src={selectedDevice.logoUrl} alt={`${selectedDevice.name} logo`} />
                </div>
                <h3>{selectedDevice.name}</h3>
            </div>
        </div>
    );
}

export default DeviceDetailPanel;