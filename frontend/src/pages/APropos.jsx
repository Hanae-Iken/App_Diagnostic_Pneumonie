import React from 'react';
import './SectionStyle.css'; // même CSS partagé
import './APropos.css'; // si tu veux du spécifique

const Apropos = () => {
  return (
    <section className="section">
      <h2 className="apropos-title">À propos de notre application</h2>
      <p>
        <span className="highlight">Notre application</span> a été conçue avec l'objectif clair d'assister les professionnels de santé
        dans le diagnostic précoce de la <strong>pneumonie</strong>. Grâce à l’intégration d’un algorithme d’intelligence
        artificielle, elle permet d’analyser des radiographies pulmonaires en quelques secondes avec un haut
        taux de fiabilité.
      </p>
      <p>
        Nous savons à quel point chaque seconde compte dans les situations d’urgence médicale. C’est pourquoi
        notre outil a été pensé pour être <strong>rapide, intuitif</strong> et accessible aussi bien aux médecins qu’aux patients,
        dans une démarche de prévention et de soutien à la décision.
      </p>
      <ul>
        <li>Analyse intelligente d’images radiographiques</li>
        <li>Interface claire et fluide pour une navigation simple</li>
        <li>Résultats instantanés avec indicateurs visuels</li>
        <li>Support multi-utilisateurs : médecins & patients</li>
      </ul>
      <p>
        En combinant technologie moderne et besoins du terrain, notre application représente une solution
        concrète face aux défis de la pneumonie dans le monde actuel.
      </p>
    </section>
  );
};

export default Apropos;




