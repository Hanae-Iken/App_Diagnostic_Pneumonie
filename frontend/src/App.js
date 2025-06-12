import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

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
    </>
  );
}

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/signin" element={<SignIn />} />
        <Route path="/signup" element={<SignUp />} />
      </Routes>
    </Router>
  );
}

export default App;







