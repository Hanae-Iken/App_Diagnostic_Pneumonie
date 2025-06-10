import React, { useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { FiSearch, FiBell, FiUser } from 'react-icons/fi';
import './Layout.css';

const Layout = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const location = useLocation();

  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="profile">
          <div className="avatar">
            <FiUser size={24} />
          </div>
          <h3>Dr. Ahmed Berrada</h3>
          <p>Radiologue</p>
        </div>
        <nav>
          <Link to="/" className={`menu-item ${location.pathname === '/' ? 'active' : ''}`}>
            Tableau de bord
          </Link>
          <Link to="/nouvelle-analyse" className={`menu-item ${location.pathname === '/nouvelle-analyse' ? 'active' : ''}`}>
            Nouvelle analyse
          </Link>
          <Link to="/bibliotheque" className={`menu-item ${location.pathname === '/bibliotheque' ? 'active' : ''}`}>
            Bibliothèque d'images
          </Link>
          <Link to="/patients" className={`menu-item ${location.pathname === '/patients' ? 'active' : ''}`}>
            Mes patients
          </Link>
          <Link to="/historique" className={`menu-item ${location.pathname === '/historique' ? 'active' : ''}`}>
            Historique
          </Link>
          <Link to="/statistiques" className={`menu-item ${location.pathname === '/statistiques' ? 'active' : ''}`}>
            Statistiques
          </Link>
          <Link to="/parametres" className={`menu-item ${location.pathname === '/parametres' ? 'active' : ''}`}>
            Paramètres
          </Link>
        </nav>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Top Bar avec recherche */}
        <div className="top-bar">
          <div className="search-bar">
            <FiSearch className="search-icon" />
            <input
              type="text"
              placeholder="Rechercher patients, analyses..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="notifications">
            <FiBell size={20} />
            <span className="badge">3</span>
          </div>
        </div>

        {/* Contenu des pages */}
        <div className="content-wrapper">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;