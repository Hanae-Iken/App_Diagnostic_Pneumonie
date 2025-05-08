import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// Nouvelle méthode pour React 18+
const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Si vous voulez mesurer les performances dans votre app, passez une fonction
// pour logger les résultats (par exemple: reportWebVitals(console.log))
// ou envoyez-les à un point d'analytique. Apprenez-en plus: https://bit.ly/CRA-vitals
reportWebVitals();