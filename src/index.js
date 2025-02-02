import React from 'react';
import { createRoot } from 'react-dom/client';

import App from './App';

const Index = () => (
    <App />
);

const root = createRoot(document.getElementById('root'));
root.render(<Index />);
