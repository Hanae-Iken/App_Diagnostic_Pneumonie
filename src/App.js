import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './Nouvel_diagno/Layout';
import Dashboard from './ESPmedc/MEDC';
import NewAnalysis from './Nouvel_diagno/NOVANALY';
import ImageLibrary from './Bibliotheque/BiblioIMG';
import Patients from './MesPatients/MesPats';
import History from './Historique/Historic';
import Statistics from './Statistique/Statistic';
import Settings from './Parametres/Parametr';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="nouvelle-analyse" element={<NewAnalysis />} />
          <Route path="bibliotheque" element={<ImageLibrary />} />
          <Route path="patients" element={<Patients />} />
          <Route path="historique" element={<History />} />
          <Route path="statistiques" element={<Statistics />} />
          <Route path="parametres" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;