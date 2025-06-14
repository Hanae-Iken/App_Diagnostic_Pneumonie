import React, { useState } from 'react';
import '../pages/SignIn.css';
import { Link, useNavigate } from 'react-router-dom';

const SignIn = () => {
  const [showReset, setShowReset] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [resetEmail, setResetEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [resetMessage, setResetMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (error) setError('');
  };

  const handleSignInSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/api/auth/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        // Stocker le token et les informations utilisateur
        localStorage.setItem('token', data.token);
        localStorage.setItem('username', data.username);
        
        alert(`Bienvenue ${data.username} !`);
        // Rediriger vers l'application principale
        navigate('/app');
      } else {
        setError(data.error || 'Une erreur est survenue');
      }
    } catch (error) {
      console.error('Erreur lors de la connexion:', error);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const handleResetSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResetMessage('');

    try {
      const response = await fetch('http://localhost:5000/api/auth/forgot-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: resetEmail })
      });

      const data = await response.json();

      if (response.ok) {
        setResetMessage(`Un lien de réinitialisation a été envoyé à : ${resetEmail}`);
        // En développement, afficher le token (à supprimer en production)
        console.log('Token de réinitialisation:', data.reset_token);
      } else {
        setError(data.error || 'Une erreur est survenue');
      }
    } catch (error) {
      console.error('Erreur lors de la réinitialisation:', error);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const goBackToSignIn = () => {
    setShowReset(false);
    setError('');
    setResetMessage('');
    setResetEmail('');
  };

  return (
    <div className="signin-container">
      <div className="signin-form">
        {!showReset ? (
          <>
            <h2>Sign In</h2>
            <form onSubmit={handleSignInSubmit}>
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
                <label>Password</label>
                <input 
                  type="password" 
                  name="password"
                  required 
                  value={formData.password}
                  onChange={handleChange}
                  disabled={loading}
                />
              </div>
              <div style={{ textAlign: 'right', marginTop: '5px' }}>
                <button
                  type="button"
                  className="link-button"
                  onClick={() => setShowReset(true)}
                  disabled={loading}
                >
                  Forgot Password?
                </button>
              </div>
              <button type="submit" disabled={loading}>
                {loading ? 'Connexion en cours...' : 'Sign In'}
              </button>
            </form>
            <p style={{ marginTop: '20px' }}>
              Don't have an account? <Link to="/signup">Sign Up</Link>
            </p>
          </>
        ) : (
          <>
            <h2>Reset Password</h2>
            <form onSubmit={handleResetSubmit}>
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
              
              {resetMessage && (
                <div style={{ 
                  color: 'green', 
                  marginBottom: '15px', 
                  padding: '10px', 
                  backgroundColor: '#e8f5e8',
                  border: '1px solid #c8e6c9',
                  borderRadius: '4px'
                }}>
                  {resetMessage}
                </div>
              )}
              
              <div>
                <label>Email</label>
                <input
                  type="email"
                  required
                  value={resetEmail}
                  onChange={(e) => setResetEmail(e.target.value)}
                  disabled={loading}
                />
              </div>
              <button type="submit" disabled={loading}>
                {loading ? 'Envoi en cours...' : 'Send Reset Link'}
              </button>
              <button
                type="button"
                className="link-button"
                style={{ marginTop: '10px' }}
                onClick={goBackToSignIn}
                disabled={loading}
              >
                Back to Sign In
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
};

export default SignIn;