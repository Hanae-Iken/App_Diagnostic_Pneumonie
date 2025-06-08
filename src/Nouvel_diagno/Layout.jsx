import React from 'react';
import { Link, Outlet } from 'react-router-dom';
import './Layout.css';

const Layout = () => {
  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="profile">
          <div className="avatar">AB</div>
          <h3>Dr. Ahmed Berrada</h3>
          <p>Radiologue</p>
        </div>
        <nav>
          <Link to="/" className="menu-item">Tableau de bord</Link>
          <Link to="/nouvelle-analyse" className="menu-item">Nouvelle analyse</Link>
          <Link to="#" className="menu-item">Bibliothèque d'images</Link>
          <Link to="#" className="menu-item">Mes patients</Link>
          <Link to="#" className="menu-item">Historique</Link>
          <Link to="#" className="menu-item">Statistiques</Link>
          <Link to="#" className="menu-item">Paramètres</Link>
        </nav>
      </div>

      {/* Contenu principal */}
      <div className="main-content">
        <Outlet />
      </div>
    </div>
  );
};

export default Layout;