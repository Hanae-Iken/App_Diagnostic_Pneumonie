import React, { useState, useEffect } from 'react';
import { FiSearch, FiUserPlus, FiEdit2, FiTrash2, FiChevronLeft, FiChevronRight } from 'react-icons/fi';
import './MesPats.css';

const MesPats = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
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
          <button className="add-patient-btn">
            <FiUserPlus size={18} />
            Nouveau patient
          </button>
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
                      <button className="edit-btn">
                        <FiEdit2 size={16} />
                      </button>
                      <button className="delete-btn">
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
    </div>
  );
};

export default MesPats;