import React from 'react';
import './Hero.css';

const Hero = () => {
  return (
    <section className="hero">
      <div className="hero-content">
        <h1>Bienvenue sur Diagnostic Pneumonie</h1>
        <p>Un outil intelligent pour aider au diagnostic des infections pulmonaires</p>
        <a href="#apropos" className="hero-button">En savoir plus</a>
      </div>
    </section>
  );
};

export default Hero;

