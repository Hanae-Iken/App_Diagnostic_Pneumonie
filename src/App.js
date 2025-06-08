import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './Nouvel_diagno/Layout';
import Dashboard from './ESPmedc/MEDC';
import NewAnalysis from './Nouvel_diagno/NOVANALY';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="nouvelle-analyse" element={<NewAnalysis />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;