import React from 'react';
import './SectionStyle.css';

const But = () => {
  return (
    <section id="but" className="section">
      <h2>Notre objectif</h2>
      <ul>
        <li><strong>Réduire le temps de diagnostic</strong> des pneumonies pour les patients en situation critique.</li>
        <li><strong>Offrir un outil d’aide</strong> à la décision médicale basé sur des images radiographiques.</li>
        <li><strong>Soutenir les médecins</strong> dans les régions à faible accès à des spécialistes.</li>
      </ul>
    </section>
  );
};

export default But;

