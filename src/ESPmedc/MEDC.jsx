import React from 'react';
import './MEDC.css';

const MEDC = () => {
  const stats = [
    { title: 'Total analyses', value: 127, trend: 'up', change: '12%' },
    { title: 'Cas pneumonie', value: 42, trend: 'down', change: '5%' },
    { title: 'Patients suivis', value: 58, trend: 'up', change: '8%' }
  ];

  const activities = [
    { id: 1, patient: 'Mohammed', time: 'il y a 2 heures', result: 'Négatif', confidence: '98%' },
    { id: 2, patient: 'Sara', time: 'il y a 4 heures', result: 'Positif', confidence: '87%' },
    { id: 3, patient: 'Youssef', time: 'il y a 5 heures', action: 'Nouveau patient' },
    { id: 4, patient: 'Karim', time: 'il y a 8 heures', result: 'Négatif', confidence: '95%' }
  ];

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Tableau de bord</h1>
        <div className="date-filter">
          <select>
            <option>Aujourd'hui</option>
            <option>Cette semaine</option>
            <option>Ce mois</option>
          </select>
        </div>
      </div>

      <div className="stats-grid">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card">
            <h3>{stat.title}</h3>
            <div className="stat-value">
              <span>{stat.value}</span>
              <span className={`trend ${stat.trend}`}>
                {stat.trend === 'up' ? '↑' : '↓'} {stat.change}
              </span>
            </div>
            <div className="progress-bar">
              <div 
                className={`progress ${stat.trend}`} 
                style={{ width: `${Math.random() * 100}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>

      <div className="content-grid">
        <div className="activity-card">
          <div className="card-header">
            <h2>Activités récentes</h2>
            <button className="view-all">Voir tout</button>
          </div>
          <ul>
            {activities.map(activity => (
              <li key={activity.id}>
                <div className="activity-icon">
                  {activity.action ? '🆕' : activity.result === 'Positif' ? '⚠️' : '✅'}
                </div>
                <div className="activity-details">
                  <p>
                    {activity.action || 'Analyse réalisée'} - <strong>{activity.patient}</strong>
                  </p>
                  <small>
                    {activity.time}
                    {activity.result && (
                      <>
                        {' • '}
                        <span className={`result ${activity.result === 'Positif' ? 'positive' : 'negative'}`}>
                          {activity.result} ({activity.confidence})
                        </span>
                      </>
                    )}
                  </small>
                </div>
              </li>
            ))}
          </ul>
        </div>

        <div className="calendar-card">
          <div className="card-header">
            <h2>Calendrier</h2>
            <span>MAI 2025</span>
          </div>
          <div className="calendar">
            <div className="weekdays">
              {['Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa'].map(day => (
                <div key={day} className="weekday">{day}</div>
              ))}
            </div>
            <div className="days">
              {[28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21].map(day => (
                <div 
                  key={day} 
                  className={`day ${day === 8 ? 'current' : ''} ${day > 21 ? 'disabled' : ''}`}
                >
                  {day}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MEDC;