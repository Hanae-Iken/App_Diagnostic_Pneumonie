import React, { useState } from 'react';
import { FiUser, FiLock, FiGlobe, FiBell, FiMoon, FiSave } from 'react-icons/fi';
import './Parametr.css';

const Parametr = () => {
  const [settings, setSettings] = useState({
    profile: {
      nom: 'Dr. Ahmed Berrada',
      specialite: 'Radiologue',
      email: 'ahmed.berrada@hopital.com',
      telephone: '+212 6 12 34 56 78'
    },
    preferences: {
      langue: 'fr',
      notifications: true,
      darkMode: false
    },
    security: {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  });

  const handleChange = (e) => {
    const { name, value, type, checked, dataset } = e.target;
    const field = dataset.section;
    
    setSettings(prev => ({
      ...prev,
      [field]: {
        ...prev[field],
        [name]: type === 'checkbox' ? checked : value
      }
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Paramètres sauvegardés:', settings);
    alert('Paramètres mis à jour avec succès!');
  };

  return (
    <div className="settings-container">
      <h1>Paramètres</h1>
      
      <form onSubmit={handleSubmit}>
        <div className="settings-section">
          <div className="section-header">
            <FiUser className="section-icon" />
            <h2>Profil professionnel</h2>
          </div>
          <div className="form-grid">
            <div className="form-group">
              <label>Nom complet</label>
              <input
                type="text"
                name="nom"
                value={settings.profile.nom}
                onChange={handleChange}
                data-section="profile"
              />
            </div>
            <div className="form-group">
              <label>Spécialité</label>
              <input
                type="text"
                name="specialite"
                value={settings.profile.specialite}
                onChange={handleChange}
                data-section="profile"
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={settings.profile.email}
                onChange={handleChange}
                data-section="profile"
              />
            </div>
            <div className="form-group">
              <label>Téléphone</label>
              <input
                type="tel"
                name="telephone"
                value={settings.profile.telephone}
                onChange={handleChange}
                data-section="profile"
              />
            </div>
          </div>
        </div>

        <div className="settings-section">
          <div className="section-header">
            <FiGlobe className="section-icon" />
            <h2>Préférences</h2>
          </div>
          <div className="form-grid">
            <div className="form-group">
              <label>Langue</label>
              <select
                name="langue"
                value={settings.preferences.langue}
                onChange={handleChange}
                data-section="preferences"
              >
                <option value="fr">Français</option>
                <option value="en">English</option>
                <option value="ar">العربية</option>
              </select>
            </div>
            <div className="form-group checkbox">
              <input
                type="checkbox"
                id="notifications"
                name="notifications"
                checked={settings.preferences.notifications}
                onChange={handleChange}
                data-section="preferences"
              />
              <label htmlFor="notifications">
                <FiBell className="checkbox-icon" />
                Activer les notifications
              </label>
            </div>
            <div className="form-group checkbox">
              <input
                type="checkbox"
                id="darkMode"
                name="darkMode"
                checked={settings.preferences.darkMode}
                onChange={handleChange}
                data-section="preferences"
              />
              <label htmlFor="darkMode">
                <FiMoon className="checkbox-icon" />
                Mode sombre
              </label>
            </div>
          </div>
        </div>

        <div className="settings-section">
          <div className="section-header">
            <FiLock className="section-icon" />
            <h2>Sécurité</h2>
          </div>
          <div className="form-grid">
            <div className="form-group">
              <label>Mot de passe actuel</label>
              <input
                type="password"
                name="currentPassword"
                value={settings.security.currentPassword}
                onChange={handleChange}
                data-section="security"
                placeholder="••••••••"
              />
            </div>
            <div className="form-group">
              <label>Nouveau mot de passe</label>
              <input
                type="password"
                name="newPassword"
                value={settings.security.newPassword}
                onChange={handleChange}
                data-section="security"
                placeholder="••••••••"
              />
            </div>
            <div className="form-group">
              <label>Confirmer le mot de passe</label>
              <input
                type="password"
                name="confirmPassword"
                value={settings.security.confirmPassword}
                onChange={handleChange}
                data-section="security"
                placeholder="••••••••"
              />
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="save-btn">
            <FiSave size={18} />
            Enregistrer les modifications
          </button>
        </div>
      </form>
    </div>
  );
};

export default Parametr;