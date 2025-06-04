import ReactDOM from 'react-dom/client';

import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import './index.css';
// Nouvelle méthode pour React 18+


// Si vous voulez mesurer les performances dans votre app, passez une fonction
// pour logger les résultats (par exemple: reportWebVitals(console.log))
// ou envoyez-les à un point d'analytique. Apprenez-en plus: https://bit.ly/CRA-vitals

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
