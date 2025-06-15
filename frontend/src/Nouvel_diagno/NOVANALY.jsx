import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { FiUpload, FiUser, FiCalendar, FiFileText, FiImage, FiLoader, FiCheckCircle, FiAlertTriangle, FiPrinter, FiRefreshCw } from 'react-icons/fi';
import './NOVANALY.css';

const NewAnalysis = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    age: '',
    cin: '',
    symptoms: '',
    notes: '',
    file: null
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    setFormData(prev => ({ ...prev, file: e.target.files[0] }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setAnalysisResult(null);

    try {
      const token = localStorage.getItem('token');
      
      const formDataToSend = new FormData();
      formDataToSend.append('file', formData.file);
      formDataToSend.append('fullName', formData.fullName);
      formDataToSend.append('age', formData.age);
      formDataToSend.append('cin', formData.cin);
      formDataToSend.append('symptoms', formData.symptoms);
      formDataToSend.append('notes', formData.notes);

      console.log('📤 Upload en cours...');
      const uploadResponse = await axios.post('http://localhost:5000/upload', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      });

      if (uploadResponse.status === 200) {
        const fileId = uploadResponse.data.fileId;
        console.log('✅ Upload réussi, ID:', fileId);

        console.log('🔍 Lancement de l\'analyse IA...');
        const analysisResponse = await axios.post(
          `http://localhost:5000/api/analyze/${fileId}`,
          {},
          {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          }
        );

        if (analysisResponse.status === 200) {
          console.log('✅ Analyse terminée:', analysisResponse.data.analysis);
          setAnalysisResult(analysisResponse.data.analysis);
        }
      }
    } catch (err) {
      console.error('Erreur:', err);
      setError(err.response?.data?.error || 'Erreur lors de l\'analyse');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      fullName: '',
      age: '',
      cin: '',
      symptoms: '',
      notes: '',
      file: null
    });
    setAnalysisResult(null);
    setError('');
  };

  return (
    <div className="new-analysis-container">
      {/* Header */}
      <div className="analysis-header">
        <div className="header-content">
          <FiImage className="header-icon" />
          <h1 className="main-title">Nouvelle Analyse Médicale</h1>
          <p className="subtitle">Analyse IA avancée pour le diagnostic de pneumonie</p>
        </div>
      </div>

      {/* Message d'erreur */}
      {error && (
        <div className="error-message">
          <FiAlertTriangle className="error-icon" />
          <span className="error-text">Erreur: {error}</span>
        </div>
      )}

      {/* Formulaire */}
      {!analysisResult && (
        <div className="form-container">
          <form onSubmit={handleSubmit} className="analysis-form">
            <div className="form-row">
              {/* Nom Complet */}
              <div className="form-group">
                <label className="form-label">
                  <FiUser className="label-icon" />
                  Nom Complet *
                </label>
                <input
                  type="text"
                  name="fullName"
                  value={formData.fullName}
                  onChange={handleChange}
                  required
                  className="form-input"
                  placeholder="Entrez le nom complet..."
                />
              </div>

              {/* Âge */}
              <div className="form-group">
                <label className="form-label">
                  <FiCalendar className="label-icon" />
                  Âge *
                </label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  required
                  className="form-input"
                  placeholder="Âge en années..."
                />
              </div>

              {/* CIN */}
              <div className="form-group">
                <label className="form-label">
                  <FiFileText className="label-icon" />
                  CIN *
                </label>
                <input
                  type="text"
                  name="cin"
                  value={formData.cin}
                  onChange={handleChange}
                  required
                  className="form-input"
                  placeholder="Numéro CIN..."
                />
              </div>

              {/* Fichier */}
              <div className="form-group">
                <label className="form-label">
                  <FiUpload className="label-icon" />
                  Image Médicale * (.png, .jpg, .jpeg, .dcm)
                </label>
                <input
                  type="file"
                  accept=".png,.jpg,.jpeg,.dcm"
                  onChange={handleFileChange}
                  required
                  className="form-file-input"
                />
              </div>
            </div>

            {/* Symptômes */}
            <div className="form-group full-width">
              <label className="form-label">
                <FiFileText className="label-icon" />
                Symptômes *
              </label>
              <textarea
                name="symptoms"
                value={formData.symptoms}
                onChange={handleChange}
                required
                className="form-textarea"
                rows="3"
                placeholder="Décrivez les symptômes du patient..."
              />
            </div>

            {/* Notes */}
            <div className="form-group full-width">
              <label className="form-label">
                <FiFileText className="label-icon" />
                Notes supplémentaires
              </label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                className="form-textarea"
                rows="3"
                placeholder="Notes additionnelles (optionnel)..."
              />
            </div>

            {/* Bouton Submit */}
            <div className="form-actions">
              <button
                type="submit"
                disabled={isLoading}
                className={`submit-btn ${isLoading ? 'loading' : ''}`}
              >
                {isLoading ? (
                  <>
                    <FiLoader className="btn-icon spinning" />
                    Analyse en cours...
                  </>
                ) : (
                  <>
                    <FiImage className="btn-icon" />
                    Analyser l'image
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Résultats de l'analyse */}
      {analysisResult && (
        <div className="results-card">
          <div className="results-header">
            <h2 className="results-title">
              <FiCheckCircle className="title-icon" />
              Résultats de l'Analyse
            </h2>
          </div>

          {/* Informations Patient */}
          <div className="patient-info-card">
            <h3 className="section-title">
              <FiUser className="section-icon" />
              Informations Patient
            </h3>
            <div className="patient-details">
              <div className="detail-item">
                <span className="detail-label">Nom:</span>
                <span className="detail-value">{analysisResult.patient?.nomComplet}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Âge:</span>
                <span className="detail-value">{analysisResult.patient?.age} ans</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">CIN:</span>
                <span className="detail-value">{analysisResult.patient?.cin}</span>
              </div>
            </div>
          </div>

          {/* Diagnostic Principal */}
          <div className={`diagnostic-card ${analysisResult.resultat === 'NORMAL' ? 'normal' : 'pneumonia'}`}>
            <div className="diagnostic-content">
              <div className="diagnostic-icon">
                {analysisResult.resultat === 'NORMAL' ? 
                  <FiCheckCircle /> : 
                  <FiAlertTriangle />
                }
              </div>
              <div className="diagnostic-text">
                <h3 className="diagnostic-title">
                  {analysisResult.resultat === 'NORMAL' ? 'NORMAL' : 'PNEUMONIE DÉTECTÉE'}
                </h3>
                <p className="confidence-score">
                  Confiance: {(analysisResult.confiance * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>

          {/* Images et Analyse */}
          {analysisResult.heatmap && (
            <div className="analysis-section">
              <h3 className="section-title">
                <FiImage className="section-icon" />
                Analyse Visuelle
              </h3>
              
              <div className="images-grid">
                {/* Heatmap */}
                <div className="image-card heatmap-card">
                  <h4 className="image-title">Heatmap - Zones d'influence IA</h4>
                  <div className="image-container">
                    <img
                      src={analysisResult.heatmap}
                      alt="Heatmap de l'analyse"
                      className="analysis-image"
                    />
                  </div>
                  <p className="image-description">
                    Les zones colorées indiquent les régions qui ont le plus influencé la décision de l'IA
                  </p>
                </div>

                {/* Détails et Probabilités */}
                <div className="details-panel">
                  {/* Probabilités */}
                  <div className="probabilities-card">
                    <h4 className="card-title">Probabilités</h4>
                    <div className="probability-item">
                      <div className="probability-header">
                        <span>Normal</span>
                        <span className="probability-value">
                          {(analysisResult.details.probabilite_normale * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="progress-bar">
                        <div 
                          className="progress-fill normal"
                          style={{ width: `${analysisResult.details.probabilite_normale * 100}%` }}
                        ></div>
                      </div>
                    </div>
                    
                    <div className="probability-item">
                      <div className="probability-header">
                        <span>Pneumonie</span>
                        <span className="probability-value">
                          {(analysisResult.details.probabilite_pneumonie * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="progress-bar">
                        <div 
                          className="progress-fill pneumonia"
                          style={{ width: `${analysisResult.details.probabilite_pneumonie * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>

                  {/* Détails supplémentaires */}
                  <div className="additional-details">
                    <h4 className="card-title">Détails</h4>
                    <div className="detail-item">
                      <span className="detail-label">Sévérité:</span>
                      <span className="detail-value">{analysisResult.details.severite}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Zone:</span>
                      <span className="detail-value">{analysisResult.details.zone_affectee}</span>
                    </div>
                  </div>

                  {/* Recommandations */}
                  {analysisResult.details?.recommendations && (
                    <div className="recommendations-card">
                      <h4 className="card-title">Recommandations</h4>
                      <ul className="recommendations-list">
                        {analysisResult.details.recommendations.map((rec, index) => (
                          <li key={index} className="recommendation-item">{rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Date d'analyse */}
          <div className="analysis-date">
            <FiCalendar className="date-icon" />
            Analysé le: {new Date(analysisResult.dateAnalyse).toLocaleString('fr-FR')}
          </div>

          {/* Actions */}
          <div className="results-actions">
            <button onClick={resetForm} className="btn btn-primary">
              <FiRefreshCw className="btn-icon" />
              Nouvelle Analyse
            </button>
            <button onClick={() => window.print()} className="btn btn-secondary">
              <FiPrinter className="btn-icon" />
              Imprimer
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default NewAnalysis;