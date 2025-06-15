import React, { useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { FiSearch, FiBell, FiUser, FiMenu, FiX } from 'react-icons/fi';
import './Layout.css';

const Layout = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const menuItems = [
    { path: '/app', name: 'Tableau de bord', icon: '📊' },
    { path: '/app/new-analysis', name: 'Nouvelle analyse', icon: '🖼️' },
    // { path: '/app/image-library', name: 'Bibliothèque', icon: '📚' },
    { path: '/app/patients', name: 'Patients', icon: '👨‍⚕️' },
    { path: '/app/history', name: 'Historique', icon: '🕒' },
    // { path: '/app/statistics', name: 'Statistiques', icon: '📈' },
    // { path: '/app/settings', name: 'Paramètres', icon: '⚙️' }
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
              <FiUser size={24} />
            </div>
            <div className="profile-info">
              <h3>{username}</h3>
              <p>Radiologue</p>
            </div>
          </div>
          <button 
            className="close-menu"
            onClick={() => setMobileMenuOpen(false)}
          >
            <FiX size={24} />
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
            <FiMenu size={24} />
          </button>
          <div className="search-bar">
            <FiSearch className="search-icon" />
            <input
              type="text"
              placeholder="Rechercher patients, analyses..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="user-actions">
            <button className="notification-btn">
              <FiBell size={20} />
              <span className="badge">3</span>
            </button>
            <div className="user-profile">
              <span>{username}</span>
            </div>
          </div>
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