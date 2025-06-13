import React, { useState } from 'react';
import { FiSearch, FiUserPlus, FiEdit2, FiTrash2, FiChevronLeft, FiChevronRight } from 'react-icons/fi';
import './MesPats.css';

const MesPats = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const patientsPerPage = 8;

  const patients = [
    { id: 1, name: 'Mohammed Alami', age: 45, gender: 'M', lastVisit: '15/05/2023', status: 'active' },
    { id: 2, name: 'Fatima Zahra', age: 32, gender: 'F', lastVisit: '10/05/2023', status: 'active' },
    { id: 3, name: 'Karim Benzema', age: 28, gender: 'M', lastVisit: '05/05/2023', status: 'inactive' },
    { id: 4, name: 'Leila Marrakchi', age: 56, gender: 'F', lastVisit: '28/04/2023', status: 'active' },
    { id: 5, name: 'Youssef Nouri', age: 38, gender: 'M', lastVisit: '22/04/2023', status: 'active' },
    { id: 6, name: 'Amina Belhaj', age: 29, gender: 'F', lastVisit: '18/04/2023', status: 'inactive' },
    { id: 7, name: 'Hassan El Fassi', age: 62, gender: 'M', lastVisit: '15/04/2023', status: 'active' },
    { id: 8, name: 'Khadija Toumi', age: 41, gender: 'F', lastVisit: '10/04/2023', status: 'active' },
    { id: 9, name: 'Omar Saber', age: 35, gender: 'M', lastVisit: '05/04/2023', status: 'inactive' },
    { id: 10, name: 'Zineb Akkaoui', age: 27, gender: 'F', lastVisit: '01/04/2023', status: 'active' }
  ];

  const filteredPatients = patients.filter(patient =>
    patient.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const indexOfLastPatient = currentPage * patientsPerPage;
  const indexOfFirstPatient = indexOfLastPatient - patientsPerPage;
  const currentPatients = filteredPatients.slice(indexOfFirstPatient, indexOfLastPatient);
  const totalPages = Math.ceil(filteredPatients.length / patientsPerPage);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

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
                <td colSpan="6" className="no-results">
                  Aucun patient trouvé
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