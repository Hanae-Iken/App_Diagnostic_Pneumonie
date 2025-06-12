import React from 'react';
import SignIn from './SignIn';  // Chemin mis à jour si SignIn est dans "pages"
import SignUp from './SignUp';
import FeedbackSection from './Feedbacks'; // si tu l'as fait
import { Link } from "react-router-dom";

// Dans le return du composant :
<Link to="/signin">
  <button className="btn-primary">Sign In</button>
</Link>


const Accueil = () => {
  return (
    <div>
      <section id="hero">
        <h1>Bienvenue sur l'application de diagnostic</h1>
      </section>

      <section id="signin-signup">
        <SignIn />
        <SignUp />
      </section>

      <section id="feedback">
        <FeedbackSection />
      </section>
      

// Dans le return du composant :
<Link to="/signin">
  <button className="btn-primary">Sign In</button>
</Link>

    </div>
  );
};

export default Accueil;






