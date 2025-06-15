import React, { useState, useEffect } from 'react';
import { FiSearch, FiUserPlus, FiEdit2, FiTrash2, FiChevronLeft, FiChevronRight, FiX, FiSave } from 'react-icons/fi';
import './MesPats.css';

const MesPats = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingPatient, setEditingPatient] = useState(null);
  const [editForm, setEditForm] = useState({
    name: '',
    age: '',
    cin: '',
    symptoms: '',
    notes: ''
  });
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);
  const patientsPerPage = 8;

  // Fonction pour récupérer les patients depuis l'API
  const fetchPatients = async () => {
    try {
      const token = localStorage.getItem('token');
      
      if (!token) {
        throw new Error('Token d\'authentification manquant');
      }
      
      console.log('Récupération des patients...');
      
      const response = await fetch('http://localhost:5000/api/patients', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      console.log('Réponse reçue:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Erreur réponse:', errorText);
        throw new Error(`Erreur ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log('Données reçues:', data);
      setPatients(data.patients || []);
    } catch (err) {
      setError(err.message);
      console.error('Erreur complète:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fonction pour modifier un patient
  const updatePatient = async (patientId, updatedData) => {
    try {
      setActionLoading(true);
      const token = localStorage.getItem('token');
      
      if (!token) {
        throw new Error('Token d\'authentification manquant');
      }

      const response = await fetch(`http://localhost:5000/api/patients/${patientId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Erreur lors de la modification');
      }

      const result = await response.json();
      
      // Mettre à jour la liste des patients localement
      setPatients(prevPatients => 
        prevPatients.map(patient => 
          patient.id === patientId 
            ? { ...patient, ...updatedData }
            : patient
        )
      );

      setEditingPatient(null);
      setError('');
      
      // Afficher un message de succès
      alert('Patient modifié avec succès !');
      
    } catch (err) {
      setError(err.message);
      console.error('Erreur modification:', err);
    } finally {
      setActionLoading(false);
    }
  };

  // Fonction pour supprimer un patient
  const deletePatient = async (patientId) => {
    try {
      setActionLoading(true);
      const token = localStorage.getItem('token');
      
      if (!token) {
        throw new Error('Token d\'authentification manquant');
      }

      const response = await fetch(`http://localhost:5000/api/patients/${patientId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Erreur lors de la suppression');
      }

      // Supprimer le patient de la liste locale
      setPatients(prevPatients => 
        prevPatients.filter(patient => patient.id !== patientId)
      );

      setDeleteConfirm(null);
      setError('');
      
      // Afficher un message de succès
      alert('Patient supprimé avec succès !');
      
    } catch (err) {
      setError(err.message);
      console.error('Erreur suppression:', err);
    } finally {
      setActionLoading(false);
    }
  };

  // Gérer l'ouverture du formulaire de modification
  const handleEditClick = (patient) => {
    setEditingPatient(patient.id);
    setEditForm({
      name: patient.name,
      age: patient.age,
      cin: patient.cin,
      symptoms: patient.symptoms || '',
      notes: patient.notes || ''
    });
  };

  // Gérer la soumission du formulaire de modification
  const handleEditSubmit = (e) => {
    e.preventDefault();
    if (editingPatient) {
      updatePatient(editingPatient, editForm);
    }
  };

  // Gérer la confirmation de suppression
  const handleDeleteClick = (patient) => {
    setDeleteConfirm(patient);
  };

  // Confirmer la suppression
  const confirmDelete = () => {
    if (deleteConfirm) {
      deletePatient(deleteConfirm.id);
    }
  };

  // Charger les patients au montage du composant
  useEffect(() => {
    fetchPatients();
  }, []);

  // Filtrage des patients
  const filteredPatients = patients.filter(patient =>
    patient.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Pagination
  const indexOfLastPatient = currentPage * patientsPerPage;
  const indexOfFirstPatient = indexOfLastPatient - patientsPerPage;
  const currentPatients = filteredPatients.slice(indexOfFirstPatient, indexOfLastPatient);
  const totalPages = Math.ceil(filteredPatients.length / patientsPerPage);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  if (loading) {
    return (
      <div className="patients-container">
        <div className="loading">Chargement des patients...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="patients-container">
        <div className="error">Erreur: {error}</div>
        <button onClick={fetchPatients} className="retry-btn">
          Réessayer
        </button>
      </div>
    );
  }

  return (
    <div className="patients-container">
      <div className="patients-header">
        <h1>Mes patients</h1>
        <div className="patients-actions">
          <div className="search-box">
            <FiSearch className="search-icon" />
            <input
              type="text"
              placeholder="Rechercher un patient..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          {/* <button className="add-patient-btn">
            <FiUserPlus size={18} />
            Nouveau patient
          </button> */}
        </div>
      </div>

      <div className="patients-table-container">
        <table className="patients-table">
          <thead>
            <tr>
              <th>Nom complet</th>
              <th>Âge</th>
              <th>Genre</th>
              <th>CIN</th>
              <th>Dernière visite</th>
              <th>Statut</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {currentPatients.length > 0 ? (
              currentPatients.map(patient => (
                <tr key={patient.id}>
                  <td>
                    <div className="patient-info">
                      <div className={`patient-avatar ${patient.gender}`}>
                        {patient.gender === 'M' ? 'H' : 'F'}
                      </div>
                      <span>{patient.name}</span>
                    </div>
                  </td>
                  <td>{patient.age} ans</td>
                  <td>{patient.gender === 'M' ? 'Homme' : 'Femme'}</td>
                  <td>{patient.cin}</td>
                  <td>{patient.lastVisit}</td>
                  <td>
                    <span className={`status-badge ${patient.status}`}>
                      {patient.status === 'active' ? 'Actif' : 'Inactif'}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button 
                        className="edit-btn"
                        onClick={() => handleEditClick(patient)}
                        disabled={actionLoading}
                      >
                        <FiEdit2 size={16} />
                      </button>
                      <button 
                        className="delete-btn"
                        onClick={() => handleDeleteClick(patient)}
                        disabled={actionLoading}
                      >
                        <FiTrash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7" className="no-results">
                  {searchTerm ? 
                    `Aucun patient trouvé pour "${searchTerm}"` : 
                    'Aucun patient enregistré'
                  }
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {filteredPatients.length > 0 && (
        <div className="pagination">
          <button 
            onClick={() => paginate(currentPage - 1)} 
            disabled={currentPage === 1}
            className="pagination-btn"
          >
            <FiChevronLeft size={18} />
          </button>
          
          {Array.from({ length: totalPages }, (_, i) => i + 1).map(number => (
            <button
              key={number}
              onClick={() => paginate(number)}
              className={`pagination-btn ${currentPage === number ? 'active' : ''}`}
            >
              {number}
            </button>
          ))}
          
          <button 
            onClick={() => paginate(currentPage + 1)} 
            disabled={currentPage === totalPages}
            className="pagination-btn"
          >
            <FiChevronRight size={18} />
          </button>
        </div>
      )}

      {/* Modal de modification */}
      {editingPatient && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2>Modifier le patient</h2>
              <button 
                className="close-btn"
                onClick={() => setEditingPatient(null)}
              >
                <FiX size={20} />
              </button>
            </div>
            <form onSubmit={handleEditSubmit} className="edit-form">
              <div className="form-group">
                <label>Nom complet</label>
                <input
                  type="text"
                  value={editForm.name}
                  onChange={(e) => setEditForm({...editForm, name: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Âge</label>
                <input
                  type="number"
                  value={editForm.age}
                  onChange={(e) => setEditForm({...editForm, age: parseInt(e.target.value)})}
                  required
                />
              </div>
              <div className="form-group">
                <label>CIN</label>
                <input
                  type="text"
                  value={editForm.cin}
                  onChange={(e) => setEditForm({...editForm, cin: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Symptômes</label>
                <textarea
                  value={editForm.symptoms}
                  onChange={(e) => setEditForm({...editForm, symptoms: e.target.value})}
                  rows="3"
                />
              </div>
              <div className="form-group">
                <label>Notes</label>
                <textarea
                  value={editForm.notes}
                  onChange={(e) => setEditForm({...editForm, notes: e.target.value})}
                  rows="3"
                />
              </div>
              <div className="form-actions">
                <button 
                  type="button" 
                  className="cancel-btn"
                  onClick={() => setEditingPatient(null)}
                >
                  Annuler
                </button>
                <button 
                  type="submit" 
                  className="save-btn"
                  disabled={actionLoading}
                >
                  <FiSave size={16} />
                  {actionLoading ? 'Enregistrement...' : 'Enregistrer'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal de confirmation de suppression */}
      {deleteConfirm && (
        <div className="modal-overlay">
          <div className="modal-content delete-modal">
            <div className="modal-header">
              <h2>Confirmer la suppression</h2>
            </div>
            <div className="modal-body">
              <p>Êtes-vous sûr de vouloir supprimer le patient <strong>{deleteConfirm.name}</strong> ?</p>
              <p className="warning">Cette action est irréversible et supprimera toutes les données associées.</p>
            </div>
            <div className="modal-actions">
              <button 
                className="cancel-btn"
                onClick={() => setDeleteConfirm(null)}
                disabled={actionLoading}
              >
                Annuler
              </button>
              <button 
                className="delete-confirm-btn"
                onClick={confirmDelete}
                disabled={actionLoading}
              >
                {actionLoading ? 'Suppression...' : 'Supprimer'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MesPats;