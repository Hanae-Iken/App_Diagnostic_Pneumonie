import React from 'react';
import '../components/Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <p>&copy; {new Date().getFullYear()} Diagnostic Pneumonie. Tous droits réservés.</p>
        <div className="footer-links">
          <a href="#apropos">À propos</a>
          <a href="#contact">Contact</a>
          <a href="/signin">Connexion</a>
          <a href="/signup">Inscription</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

