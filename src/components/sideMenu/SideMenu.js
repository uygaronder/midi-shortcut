import React from 'react';
import '../../Assets/CSS/components/SideMenu.css';

const SideMenu = () => {
    return (
        <div className="side-menu">
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
            
            <ul>
                <li><a href="#settings">Settings</a></li>
                <li><a href="#logout">Logout</a></li>
            </ul>
        </div>
    );
};

export default SideMenu;