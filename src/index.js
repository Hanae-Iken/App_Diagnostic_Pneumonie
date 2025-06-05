import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './ESPmedc/MEDC.css';

// Vérification que l'élément root existe avant le rendu
const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error("L'élément avec l'ID 'root' est introuvable dans index.html");
}

const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);