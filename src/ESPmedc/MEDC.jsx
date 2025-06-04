import React from 'react';
import './MEDC.css';
import { FaUserMd, FaClinicMedical, FaXRay, FaUserFriends, FaHistory, FaChartBar, FaCog, FaSearch, FaBell, FaUserCircle } from 'react-icons/fa';

const MEDC = () => {
  return (
    <div className="medc-container">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="logo-section">
          <h1>DIAGNOSTIC</h1>
          <h2>PNEUMONIE</h2>
        </div>
        
        <div className="doctor-profile">
          <FaUserCircle className="profile-icon" />
          <div className="doctor-info">
            <h3>Dr. Ahmed Berrada</h3>
            <p>Radiologue</p>
          </div>
        </div>
        
        <nav className="menu">
          <ul>
            <li className="active"><FaUserMd /> Tableau de bord</li>
            <li><FaClinicMedical /> Nouveau diagnostic</li>
            <li><FaUserFriends /> Patients</li>
            <li><FaCog /> Paramètres</li>
          </ul>
        </nav>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Top Bar */}
        <div className="top-bar">
          <div className="search-box">
            <FaSearch className="search-icon" />
            <input type="text" placeholder="Rechercher..." />
          </div>
          <div className="notifications">
            <FaBell />
            <span className="badge">3</span>
          </div>
        </div>

        {/* Dashboard Content */}
        <div className="dashboard">
          <h1>Bienvenue, Dr. Berrada</h1>
          
          {/* Stats Cards */}
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Diagnostics totaux</h3>
              <p>127</p>
            </div>
            <div className="stat-card">
              <h3>Cas de pneumonie</h3>
              <p>42</p>
            </div>
            <div className="stat-card">
              <h3>Patients suivis</h3>
              <p>58</p>
            </div>
            <div className="stat-card">
              <h3>Taux de précision</h3>
              <p>98%</p>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="recent-activity">
            <h2>Activités récentes</h2>
            <div className="activity-list">
              <div className="activity-item">
                <div className="activity-icon diagnostic"></div>
                <div className="activity-details">
                  <p>Diagnostic complet - Patient: Mohammed</p>
                  <span>il y a 2 heures - Résultat: Négatif (98%)</span>
                </div>
              </div>
              <div className="activity-item">
                <div className="activity-icon positive"></div>
                <div className="activity-details">
                  <p>Diagnostic complet - Patient: Sara</p>
                  <span>il y a 4 heures - Résultat: Positif (87%)</span>
                </div>
              </div>
              <div className="activity-item">
                <div className="activity-icon new-patient"></div>
                <div className="activity-details">
                  <p>Nouveau patient ajouté - Youssef</p>
                  <span>il y a 5 heures</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MEDC;