import React from 'react';
import { register } from '../api';

const SignUp = () => {
  const [formData, setFormData] = useState({
    nom: '',
    prenom: '',
    email: '',
    password: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await register(formData);
      alert(response.message || 'Inscription réussie !');
      window.location.href = '/signin'; // Redirection
    } catch (error) {
      alert(error.message || 'Erreur lors de l\'inscription');
    }
  };

  // ... (le reste du formulaire reste inchangé)
};
import '../App.css';
import thumbnailImage from './image/thumbnail_800x480px-119034.jpg';

const SignUp = () => {
  return (
    <div className="signup-container">
      <div className="signup-image-container">
        <img 
          src={thumbnailImage} 
          alt="Pneumonia Diagnostic" 
          className="signup-image" 
        />
      </div>
      
      <div className="signup-content">
        <div className="welcome-header">
          <h1>WELCOME</h1>
          <h2>DIAGNOSTIC</h2>
          <h3>PNEUMONIE</h3>
        </div>

        <div className="signup-form">
          <h2>Sign Up</h2>
          <form>
            <div className="form-group">
              <label htmlFor="fullName">Full name</label>
              <input type="text" id="fullName" name="fullName" required />
            </div>
            
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input type="email" id="email" name="email" required />
            </div>
            
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input type="password" id="password" name="password" required />
            </div>
            
            <button type="submit" className="signup-btn">Sign Up</button>
          </form>
          
          <p className="login-link">
            Already have an account? <a href="/signin">Sign In</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignUp;