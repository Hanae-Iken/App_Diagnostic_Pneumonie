import React from 'react';
import '../App.css';

const SignUpPage = () => {
  return (
    <div className="signup-container">
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
  );
};

export default SignUpPage;