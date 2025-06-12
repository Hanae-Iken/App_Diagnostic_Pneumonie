import React from 'react';
import { Link } from 'react-router-dom'; // Ajout pour le routing
import '../styles/Navbar.css';
import logo from '../assets/Logo.png';

const Navbar = () => {
  const handleScroll = (e, sectionId) => {
    e.preventDefault();
    const section = document.getElementById(sectionId);
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <img src={logo} alt="Logo" className="logo" />
      </div>

      <ul className="nav-links">
        <li><a href="#hero" onClick={(e) => handleScroll(e, 'hero')}>Accueil</a></li>
        <li><a href="#apropos" onClick={(e) => handleScroll(e, 'apropos')}>À propos</a></li>
        <li><a href="#but" onClick={(e) => handleScroll(e, 'but')}>But</a></li>
        <li><a href="#fonctionnement" onClick={(e) => handleScroll(e, 'fonctionnement')}>Fonctionnement</a></li>
        <li><a href="#feedbacks" onClick={(e) => handleScroll(e, 'feedbacks')}>Feedbacks</a></li>
        <li><a href="#contact" onClick={(e) => handleScroll(e, 'contact')}>Contact</a></li>
      </ul>

      <div className="auth-buttons">
        <Link to="/signin" className="signin-btn">Sign In</Link>
        <Link to="/signup" className="signup-btn">Sign Up</Link>
      </div>
    </nav>
  );
};

export default Navbar;












