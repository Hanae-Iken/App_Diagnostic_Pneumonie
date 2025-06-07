import React from 'react';
import './MEDC.css';

const MEDC = () => {
  // Données des activités
  const activities = [
    { patient: 'Mohammed', time: 'il y a 2 heures', result: 'Négatif', confidence: '98%' },
    { patient: 'Sara', time: 'il y a 4 heures', result: 'Positif', confidence: '87%' },
    { patient: 'Youssef', time: 'il y a 5 heures', action: 'Nouveau patient' },
    { patient: 'Karim', time: 'il y a 8 heures', result: 'Négatif', confidence: '95%' }
  ];

  // Données du calendrier
  const calendarDays = ['Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa'];
  const calendarDates = [
    [28, 29, 30, 1, 2, 3],
    [4, 5, 6, 7, 8, 9],
    [10, 11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20, 21]
  ];

  return (
    <div className="medc-dashboard">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="profile">
          <div className="avatar">AB</div>
          <h3>Dr. Ahmed Berrada</h3>
          <p>Radiologue</p>
        </div>
        <nav>
          <button className="active">Tableau de bord</button>
          <button>Nouvelle analyse</button>
          <button>Mes patients</button>
          <button>Paramètres</button>
        </nav>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <header>
          <h1>Tableau de bord</h1>
        </header>

        {/* Stats Cards */}
        <div className="stats-container">
          <div className="stat-card">
            <h3>Total d'analyses</h3>
            <p>127</p>
          </div>
          <div className="stat-card">
            <h3>Cas de pneumonie</h3>
            <p>42</p>
          </div>
          <div className="stat-card">
            <h3>Patients suivis</h3>
            <p>58</p>
          </div>
        </div>

        {/* Activity and Calendar */}
        <div className="content-grid">
          <div className="activity-section">
            <h2>Activités récentes</h2>
            <ul>
              {activities.map((activity, index) => (
                <li key={index}>
                  {activity.action ? (
                    <p><strong>{activity.action}</strong> - {activity.patient}<br />
                    <small>{activity.time}</small></p>
                  ) : (
                    <p><strong>Analyse réalisée</strong> - Patient: {activity.patient}<br />
                    <small>{activity.time} - Résultat: <span className={activity.result === 'Positif' ? 'positive' : 'negative'}>{activity.result} ({activity.confidence})</span></small></p>
                  )}
                </li>
              ))}
            </ul>
          </div>

          <div className="calendar-section">
            <h2>Calendrier</h2>
            <table>
              <caption>MAI 2025</caption>
              <thead>
                <tr>
                  {calendarDays.map(day => <th key={day}>{day}</th>)}
                </tr>
              </thead>
              <tbody>
                {calendarDates.map((week, weekIndex) => (
                  <tr key={weekIndex}>
                    {week.map((date, dateIndex) => (
                      <td key={dateIndex} className={date === 8 ? 'current-day' : ''}>{date}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MEDC;