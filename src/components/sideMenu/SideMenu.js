import React from 'react';
import '../../Assets/CSS/components/SideMenu.css';

import homeIcon from '../../Assets/SVG/home.svg';
import settingsIcon from '../../Assets/SVG/settings.svg';

const SideMenu = () => {
    return (
        <div className="side-menu">
            <ul>
                <li><a href="#home"><img src={homeIcon} alt="Home" className='svg' /></a></li>
            </ul>
            
            <ul>
                <li><a href="#settings"><img src={settingsIcon} alt="Settings" className='svg' /></a></li>
            </ul>
        </div>
    );
};

export default SideMenu;