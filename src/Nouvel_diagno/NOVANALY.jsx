import React, { useState } from 'react';
import './NOVANALY.css';

const NOVANALY = () => {
  const [patient, setPatient] = useState({
    nom: '',
    age: '',
    sexe: '',
    symptomes: ''
  });
  const [image, setImage] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Données soumises:', { patient, image });
    // Ajoutez ici la logique de soumission
  };

  return (
    <div className="new-analysis">
      <h1>Nouvelle analyse</h1>
      
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
              />
            </div>
            
            <div className="form-group">
              <label>Sexe</label>
              <select
                value={patient.sexe}
                onChange={(e) => setPatient({...patient, sexe: e.target.value})}
                required
              >
                <option value="">Sélectionner</option>
                <option value="M">Masculin</option>
                <option value="F">Féminin</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Symptômes</label>
            <textarea
              value={patient.symptomes}
              onChange={(e) => setPatient({...patient, symptomes: e.target.value})}
              required
            />
          </div>
        </div>

        <div className="form-section">
          <h2>Imagerie médicale</h2>
          
          <div className="upload-area">
            {image ? (
              <div className="image-preview">
                <img src={URL.createObjectURL(image)} alt="Preview" />
                <button
                  type="button"
                  onClick={() => setImage(null)}
                  className="remove-btn"
                >
                  Supprimer
                </button>
              </div>
            ) : (
              <>
                <input
                  type="file"
                  id="image-upload"
                  accept="image/*,.dcm"
                  onChange={(e) => setImage(e.target.files[0])}
                  hidden
                />
                <label htmlFor="image-upload" className="upload-label">
                  <span>+</span>
                  <p>Glissez-déposez une image ou cliquez pour sélectionner</p>
                  <small>Formats acceptés: JPG, PNG, DICOM</small>
                </label>
              </>
            )}
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="submit-btn">
            Lancer l'analyse
          </button>
        </div>
      </form>
    </div>
  );
};

export default NOVANALY;