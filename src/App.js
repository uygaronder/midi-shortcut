import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import useRawInputEvents from './hooks/useRawInputEvents';
import { RawInputProvider } from './contexts/rawInputContext';

import './Assets/CSS/main/root.css';
import './Assets/CSS/main/App.css';

import Dashboard from './pages/dashboard/Dashboard';
//import Settings from './pages/settings/Settings';
import SideMenu from './components/sideMenu/SideMenu';


function App() {
    const rawEvent = useRawInputEvents();

    const layout = (content) => (
        <div className='main'>
            <SideMenu />
            <RawInputProvider value={rawEvent}>
                {content}
            </RawInputProvider>
        </div>
    );

    return (
        <Router>
            <Routes>
                <Route path='/' element={layout(<Dashboard />)} />
            </Routes>
        </Router>
    );
}

export default App;