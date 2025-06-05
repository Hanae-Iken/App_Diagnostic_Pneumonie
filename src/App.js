import React from 'react';
import MEDC from './ESPmedc/MEDC';  // <-- Problème probable ici

function App() {
  return (
    <div className="app">
      <MEDC />  {/* L'erreur pointe vers ce rendu */}
    </div>
  );
}

export default App;