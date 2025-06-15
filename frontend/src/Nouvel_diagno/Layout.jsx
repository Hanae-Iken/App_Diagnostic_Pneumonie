import React, { useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import './Layout.css';

const Layout = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  
  const menuItems = [
    { 
      path: '/app', 
      name: 'Tableau de bord', 
      icon: '📊'
    },
    { 
      path: '/app/new-analysis', 
      name: 'Nouvelle analyse', 
      icon: '➕'
    },
    { 
      path: '/app/patients', 
      name: 'Patients', 
      icon: '👥'
    },
    { 
      path: '/app/history', 
      name: 'Historique', 
      icon: '🕐'
    }
  ];

  // Récupérer le nom d'utilisateur depuis localStorage
  const username = localStorage.getItem('username') || 'Dr. Utilisateur';

  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className={`sidebar ${mobileMenuOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="profile">
            <div className="avatar">
              <span style={{fontSize: '24px'}}>👤</span>
            </div>
            <div className="profile-info">
              <h3>{username}</h3>
              <p>Médecin spécialiste</p>
            </div>
          </div>
          <button
            className="close-menu"
            onClick={() => setMobileMenuOpen(false)}
          >
            <span style={{fontSize: '24px'}}>✕</span>
          </button>
        </div>
        
        <nav>
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`menu-item ${location.pathname === item.path ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <span className="menu-icon">{item.icon}</span>
              <span className="menu-text">{item.name}</span>
            </Link>
          ))}
        </nav>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Top Bar */}
        <header className="top-bar">
          <button
            className="menu-toggle"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <span style={{fontSize: '24px'}}>☰</span>
          </button>

          <div className="search-bar">
            <span className="search-icon" style={{fontSize: '16px'}}>🔍</span>
            <input
              type="text"
              placeholder="Rechercher patients, analyses..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {/* <div className="user-actions">
            <button className="notification-btn">
              <span style={{fontSize: '20px'}}>🔔</span>
              <span className="badge">3</span>
            </button>
            <div className="user-profile">
              <span>{username}</span>
            </div>
          </div> */}
        </header>

        {/* Page Content */}
        <div className="page-content">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;