import React, { useState } from 'react';
import { FiSearch, FiFilter, FiDownload, FiEye } from 'react-icons/fi';
import './BiblioIMG.css';

const BiblioIMG = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');
  
  const cases = [
    { id: 1, patient: 'Mohammed', date: '15/05/2023', type: 'RX Thorax', result: 'positive', image: 'case1.jpg' },
    { id: 2, patient: 'Fatima', date: '10/05/2023', type: 'CT Scan', result: 'negative', image: 'case2.jpg' },
    { id: 3, patient: 'Karim', date: '05/05/2023', type: 'RX Thorax', result: 'positive', image: 'case3.jpg' },
    { id: 4, patient: 'Leila', date: '28/04/2023', type: 'IRM', result: 'negative', image: 'case4.jpg' },
    { id: 5, patient: 'Youssef', date: '22/04/2023', type: 'RX Thorax', result: 'positive', image: 'case5.jpg' },
    { id: 6, patient: 'Amina', date: '18/04/2023', type: 'CT Scan', result: 'negative', image: 'case6.jpg' }
  ];

  const filteredCases = cases.filter(caseItem => {
    const matchesSearch = caseItem.patient.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         caseItem.type.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === 'all' || caseItem.result === filter;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="library">
      <div className="library-header">
        <h1>Bibliothèque d'images</h1>
        <div className="library-controls">
          <div className="search-box">
            <FiSearch className="search-icon" />
            <input 
              type="text" 
              placeholder="Rechercher par patient ou type..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="filter-dropdown">
            <FiFilter className="filter-icon" />
            <select value={filter} onChange={(e) => setFilter(e.target.value)}>
              <option value="all">Tous les cas</option>
              <option value="positive">Positifs</option>
              <option value="negative">Négatifs</option>
            </select>
          </div>
        </div>
      </div>

      <div className="cases-grid">
        {filteredCases.length > 0 ? (
          filteredCases.map(caseItem => (
            <div key={caseItem.id} className={`case-card ${caseItem.result}`}>
              <div className="case-image">
                <img src={`/images/${caseItem.image}`} alt={`${caseItem.type} - ${caseItem.patient}`} />
                <div className="case-overlay">
                  <button className="icon-btn">
                    <FiEye size={18} />
                  </button>
                  <button className="icon-btn">
                    <FiDownload size={18} />
                  </button>
                </div>
              </div>
              <div className="case-details">
                <h3>{caseItem.patient}</h3>
                <p>{caseItem.type}</p>
                <div className="case-meta">
                  <span>{caseItem.date}</span>
                  <span className={`case-tag ${caseItem.result}`}>
                    {caseItem.result === 'positive' ? 'Positif' : 'Négatif'}
                  </span>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="no-results">
            <p>Aucun résultat trouvé</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default BiblioIMG;