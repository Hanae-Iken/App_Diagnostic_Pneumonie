import React, { useState } from 'react';
import './SignIn.css';
import { Link } from 'react-router-dom';

const SignIn = () => {
  const [showReset, setShowReset] = useState(false);
  const [email, setEmail] = useState('');

  const handleResetSubmit = (e) => {
    e.preventDefault();
    // 👉 ici tu peux appeler une API de reset si tu en as une
    alert(`Un lien de réinitialisation a été envoyé à : ${email}`);
    setShowReset(false); // retour à la page de connexion
  };

  return (
    <div className="signin-container">
      <div className="signin-form">
        {!showReset ? (
          <>
            <h2>Sign In</h2>
            <form>
              <div>
                <label>Email</label>
                <input type="email" required />
              </div>
              <div>
                <label>Password</label>
                <input type="password" required />
              </div>
              <div style={{ textAlign: 'right', marginTop: '5px' }}>
                <button
                  type="button"
                  className="link-button"
                  onClick={() => setShowReset(true)}
                >
                  Forgot Password?
                </button>
              </div>
              <button type="submit">Sign In</button>
            </form>
            <p style={{ marginTop: '20px' }}>
              Don't have an account? <Link to="/signup">Sign Up</Link>
            </p>
          </>
        ) : (
          <>
            <h2>Reset Password</h2>
            <form onSubmit={handleResetSubmit}>
              <div>
                <label>Email</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <button type="submit">Send Reset Link</button>
              <button
                type="button"
                className="link-button"
                style={{ marginTop: '10px' }}
                onClick={() => setShowReset(false)}
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