import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './Nouvel_diagno/Layout';
import Dashboard from './ESPmedc/MEDC';
import NewAnalysis from './Nouvel_diagno/NOVANALY';
import ImageLibrary from './Bibliotheque/BiblioIMG';
import Patients from './MesPatients/MesPats';
import History from './HISTORIQUE/Historic';
import Statistics from './Statistique/Statistic';
import Settings from './Parametres/Parametr';

import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Apropos from './pages/APropos';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Accueil from './pages/Accueil';
import But from './pages/But';
import Fonctionnement from './pages/Fonctionnement';
import Feedbacks from './pages/Feedbacks';
import Contact from './pages/Contact';
import Footer from './components/Footer';

import './App.css';

function HomePage() {
  return (
    <>
      <div id="hero"><Hero /></div>
      <div id="apropos"><Apropos /></div>
      <div id="but"><But /></div>
      <div id="fonctionnement"><Fonctionnement /></div>
      <div id="feedbacks"><Feedbacks /></div>
      <div id="contact"><Contact /></div>
      <Footer />
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Routes publiques (site vitrine) */}
        <Route path="/" element={
          <>
            <Navbar />
            <HomePage />
          </>
        } />
        <Route path="/signin" element={
          <>
            <Navbar />
            <SignIn />
            <Footer />
          </>
        } />
        <Route path="/signup" element={
          <>
            <Navbar />
            <SignUp />
            <Footer />
          </>
        } />

        {/* Routes privées (application médicale) */}
        <Route path="/app" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="new-analysis" element={<NewAnalysis />} />
          <Route path="image-library" element={<ImageLibrary />} />
          <Route path="patients" element={<Patients />} />
          <Route path="history" element={<History />} />
          <Route path="statistics" element={<Statistics />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;