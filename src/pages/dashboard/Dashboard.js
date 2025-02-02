import React, {useState} from 'react';

import '../../Assets/CSS/pages/dashboard/Dashboard.css';

import AvailableDevices from '../../pages/dashboard/components/AvailableDevices';
import DeviceDetailPanel from './components/deviceDetailPanel/DeviceDetailPanel';

const Dashboard = () => {
    const [selectedDevice, setSelectedDevice] = useState(null);

    const handleSelectDevice = (device) => {
        console.log("Selected device:", device);

        setSelectedDevice(device);
    };

    return (
        <div className='dashboard'>
            <AvailableDevices onSelectDevice={handleSelectDevice} />
            {
                !selectedDevice ? <div className='no-device-selected'>No device selected</div> : 
                <DeviceDetailPanel selectedDevice={selectedDevice} />
            }
        </div>
    );
};

export default Dashboard;