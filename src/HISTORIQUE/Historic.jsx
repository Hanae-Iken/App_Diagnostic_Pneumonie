import React, { useState } from 'react';
import { FiCalendar, FiChevronDown } from 'react-icons/fi';
import './Historic.css';

const Historic = () => {
  const [timeFilter, setTimeFilter] = useState('week');
  const [searchTerm] = useState('');

  const historyItems = [
    { id: 1, patient: 'Mohammed Alami', date: '15/05/2023 09:30', action: 'Diagnostic', type: 'RX Thorax', result: 'Positif' },
    { id: 2, patient: 'Fatima Zahra', date: '14/05/2023 14:15', action: 'Contrôle', type: 'Consultation', result: 'Amélioration' },
    { id: 3, patient: 'Karim Benzema', date: '12/05/2023 11:00', action: 'Diagnostic', type: 'CT Scan', result: 'Négatif' },
    { id: 4, patient: 'Leila Marrakchi', date: '10/05/2023 16:45', action: 'Première visite', type: 'Consultation', result: 'Suivi requis' },
    { id: 5, patient: 'Youssef Nouri', date: '08/05/2023 10:30', action: 'Diagnostic', type: 'RX Thorax', result: 'Positif' }
  ];

  const filteredItems = historyItems.filter(item =>
    item.patient.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.action.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="history-container">
      <div className="history-header">
        <h1>Historique des consultations</h1>
        <div className="history-filters">
          <div className="search-box">
           
          </div>
          <div className="time-filter">
            <FiCalendar className="calendar-icon" />
            <select value={timeFilter} onChange={(e) => setTimeFilter(e.target.value)}>
              <option value="day">Aujourd'hui</option>
              <option value="week">Cette semaine</option>
              <option value="month">Ce mois</option>
              <option value="all">Tout l'historique</option>
            </select>
            <FiChevronDown className="chevron-icon" />
          </div>
        </div>
      </div>

      <div className="history-list">
        {filteredItems.length > 0 ? (
          filteredItems.map(item => (
            <div key={item.id} className="history-item">
              <div className="item-date">
                <span className="date">{item.date.split(' ')[0]}</span>
                <span className="time">{item.date.split(' ')[1]}</span>
              </div>
              <div className="item-content">
                <div className="item-header">
                  <h3>{item.patient}</h3>
                  <span className={`action-tag ${item.action.replace(' ', '-').toLowerCase()}`}>
                    {item.action}
                  </span>
                </div>
                <div className="item-details">
                  <p>{item.type}</p>
                  <span className={`result ${item.result === 'Positif' ? 'positive' : item.result === 'Négatif' ? 'negative' : 'neutral'}`}>
                    {item.result}
                  </span>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="no-results">
            Aucun résultat trouvé
          </div>
        )}
      </div>
    </div>
  );
};

export default Historic;