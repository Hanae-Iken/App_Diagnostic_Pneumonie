import React, { useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { FiSearch, FiBell, FiUser, FiMenu, FiX } from 'react-icons/fi';
import './Layout.css';

const Layout = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const menuItems = [
    { path: '/', name: 'Tableau de bord', icon: '📊' },
    { path: '/new-analysis', name: 'Nouvelle analyse', icon: '🖼️' },
    { path: '/image-library', name: 'Bibliothèque', icon: '📚' },
    { path: '/patients', name: 'Patients', icon: '👨‍⚕️' },
    { path: '/history', name: 'Historique', icon: '🕒' },
    { path: '/statistics', name: 'Statistiques', icon: '📈' },
    { path: '/settings', name: 'Paramètres', icon: '⚙️' }
  ];

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
              <h3>Dr.  Mohamed Berrada</h3>
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
              <span>Dr. Berrada</span>
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