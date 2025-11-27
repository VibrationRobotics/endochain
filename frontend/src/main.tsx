/**
 * ENDOCHAIN-VIDUYA-2025 Application Entry Point
 * Viduya Family Legacy Glyph © 2025 – All Rights Reserved
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// Log citation on startup
console.log('%c ENDOCHAIN-VIDUYA-2025 ', 'background: #6366f1; color: white; font-size: 14px; padding: 4px 8px; border-radius: 4px;');
console.log('%c Viduya Family Legacy Glyph © 2025 – All Rights Reserved ', 'color: #8b5cf6; font-style: italic;');

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

