import React, { useState, useRef } from 'react';
import { FiUpload, FiX, FiChevronDown } from 'react-icons/fi';
import './NOVANALY.css';

const NewAnalysis = () => {
  const [patient, setPatient] = useState({
    nom: '',
    age: '',
    sexe: '',
    symptomes: ''
  });
  const [image, setImage] = useState(null);
  const fileInputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Analyse soumise:', { patient, image });
    // Logique de soumission ici
  };

  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setImage(e.target.files[0]);
    }
  };

  return (
    <div className="new-analysis-page">
      <div className="page-header">
        <h1>Nouvelle analyse</h1>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h2>Informations patient</h2>
          
          <div className="form-group">
            <label>Nom complet</label>
            <input
              type="text"
              value={patient.nom}
              onChange={(e) => setPatient({...patient, nom: e.target.value})}
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Âge</label>
              <input
                type="number"
                value={patient.age}
                onChange={(e) => setPatient({...patient, age: e.target.value})}
                required
                min="1"
                max="120"
              />
            </div>
            
            <div className="form-group">
              <label>Sexe</label>
              <div className="custom-select">
                <select
                  value={patient.sexe}
                  onChange={(e) => setPatient({...patient, sexe: e.target.value})}
                  required
                >
                  <option value="">Sélectionner</option>
                  <option value="M">Masculin</option>
                  <option value="F">Féminin</option>
                </select>
                <FiChevronDown className="select-arrow" />
              </div>
            </div>
          </div>

          <div className="form-group">
            <label>Symptômes</label>
            <textarea
              value={patient.symptomes}
              onChange={(e) => setPatient({...patient, symptomes: e.target.value})}
              required
              placeholder="Décrivez les symptômes observés..."
            />
          </div>
        </div>

        <div className="form-section">
          <h2>Imagerie médicale</h2>
          
          <div className="upload-container">
            {image ? (
              <div className="image-preview-container">
                <div className="image-preview">
                  <img src={URL.createObjectURL(image)} alt="Preview" />
                  <button
                    type="button"
                    onClick={() => setImage(null)}
                    className="remove-image"
                  >
                    <FiX size={20} />
                  </button>
                </div>
                <div className="image-info">
                  <p>{image.name}</p>
                  <span>{(image.size / 1024).toFixed(2)} KB</span>
                </div>
              </div>
            ) : (
              <div 
                className="upload-area"
                onClick={() => fileInputRef.current.click()}
              >
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleImageChange}
                  accept="image/*,.dcm"
                  hidden
                />
                <FiUpload size={40} className="upload-icon" />
                <p>Glissez-déposez une image ou <span>parcourir</span></p>
                <small>Formats supportés: JPG, PNG, DICOM</small>
              </div>
            )}
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="secondary-btn">
            Annuler
          </button>
          <button type="submit" className="primary-btn" disabled={!image}>
            Lancer l'analyse
          </button>
        </div>
      </form>
    </div>
  );
};

export default NewAnalysis;