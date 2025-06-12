import React from 'react';
import './SectionStyle.css';

const Feedbacks = () => {
  return (
    <section id="feedbacks" className="section">
      <h2 className="apropos-title">Avis de nos utilisateurs</h2>
      <div className="feedback-box">
        <p><strong>👩‍⚕️ Dr. Leila B.</strong> : "Une aide précieuse dans mon service de pédiatrie. Rapide et intuitif !"</p>
        <p><strong>👨‍⚕️ Dr. Karim T.</strong> : "Simple, efficace et complémentaire à mon analyse radiographique."</p>
        <p><strong>🧑‍⚕️ Dr. Amine S.</strong> : "Un gain de temps considérable pour la détection des cas urgents."</p>
        <p><strong>👨‍🦱 Youssef M.</strong> : "J’ai pu mieux comprendre mon état et poser les bonnes questions à mon médecin."</p>
        <p><strong>👩‍🦰 Salma R.</strong> : "L’interface est facile à utiliser, même pour les non-experts. Très rassurant !"</p>


      </div>
    </section>
  );
};

export default Feedbacks;




