import React, { useState } from 'react';
import '../pages/SignUp.css';
import { Link, useNavigate } from 'react-router-dom';

const SignUp = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    // Efface l'erreur quand l'utilisateur tape
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // CORRECTION: URL complète avec le préfixe /api/auth
      const response = await fetch('http://localhost:5000/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        alert('Compte créé avec succès !');
        // Rediriger vers la page de connexion
        navigate('/signin');
      } else {
        setError(data.error || 'Une erreur est survenue');
      }
    } catch (error) {
      console.error('Erreur lors de l\'inscription:', error);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-form">
        <h2>Créer un compte</h2>
        <form onSubmit={handleSubmit}>
          {error && (
            <div style={{
              color: 'red',
              marginBottom: '15px',
              padding: '10px',
              backgroundColor: '#ffebee',
              border: '1px solid #ffcdd2',
              borderRadius: '4px'
            }}>
              {error}
            </div>
          )}
         
          <div>
            <label>Nom d'utilisateur</label>
            <input
              type="text"
              name="username"
              required
              value={formData.username}
              onChange={handleChange}
              disabled={loading}
            />
          </div>
         
          <div>
            <label>Email</label>
            <input
              type="email"
              name="email"
              required
              value={formData.email}
              onChange={handleChange}
              disabled={loading}
            />
          </div>
         
          <div>
            <label>Mot de passe</label>
            <input
              type="password"
              name="password"
              required
              value={formData.password}
              onChange={handleChange}
              disabled={loading}
              minLength="6"
            />
          </div>
         
          <button type="submit" disabled={loading}>
            {loading ? 'Inscription en cours...' : 'S\'inscrire'}
          </button>
        </form>
       
        <p style={{ marginTop: '20px' }}>
          Vous avez déjà un compte ? <Link to="/signin">Se connecter</Link>
        </p>
      </div>
    </div>
  );
};

export default SignUp;