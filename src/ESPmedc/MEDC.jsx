import React from 'react';
import './MEDC.css';
import { FiActivity, FiUser, FiTrendingUp, FiTrendingDown } from 'react-icons/fi';
import {  BsLungs, BsHeartPulse } from 'react-icons/bs';

const Dashboard = () => {
  const stats = [
    { title: 'Total analyses', value: 127, trend: 'up', change: '12%', icon: <FiActivity />, color: '#6366F1' },
    { title: 'Cas pneumonie', value: 42, trend: 'down', change: '5%', icon: <BsLungs />, color: '#EC4899' },
    { title: 'Patients suivis', value: 58, trend: 'up', change: '8%', icon: <FiUser />, color: '#10B981' },
    { title: 'Analyses urgentes', value: 15, trend: 'up', change: '23%', icon: <BsHeartPulse />, color: '#F59E0B' }
  ];

  const activities = [
    { id: 1, patient: 'Mohammed', time: 'il y a 2 heures', result: 'Négatif', confidence: '98%', type: 'analysis' },
    { id: 2, patient: 'Sara', time: 'il y a 4 heures', result: 'Positif', confidence: '87%', type: 'analysis' },
    { id: 3, patient: 'Youssef', time: 'il y a 5 heures', action: 'Nouveau patient', type: 'new' },
    { id: 4, patient: 'Karim', time: 'il y a 8 heures', result: 'Négatif', confidence: '95%', type: 'analysis' }
  ];

  const upcomingTasks = [
    { id: 1, title: 'Revue des cas critiques', time: '10:00 AM', priority: 'high' },
    { id: 2, title: 'Réunion équipe médicale', time: '14:30 PM', priority: 'medium' },
    { id: 3, title: 'Mise à jour logiciel', time: 'Demain', priority: 'low' }
  ];

  return (
    <div className="dashboard-page">
      {/* Top Navigation */}
      <div className="dashboard-nav">
      
       
      </div>

      <div className="page-header">
        <h1>Tableau de bord</h1>
        <div className="header-actions">
          <select className="time-filter">
            <option>Aujourd'hui</option>
            <option>Cette semaine</option>
            <option>Ce mois</option>
          </select>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card" style={{ '--card-color': stat.color }}>
            <div className="stat-icon">{stat.icon}</div>
            <div className="stat-content">
              <h3>{stat.title}</h3>
              <div className="stat-value">
                <span>{stat.value}</span>
                <span className={`trend ${stat.trend}`}>
                  {stat.trend === 'up' ? <FiTrendingUp /> : <FiTrendingDown />} {stat.change}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Main Content */}
      <div className="content-grid">
        {/* Activity Card */}
        <div className="dashboard-card activity-card">
          <div className="card-header">
            <h2>Activités récentes</h2>
            <button className="view-all">Voir tout</button>
          </div>
          <div className="activity-list">
            {activities.map(activity => (
              <div key={activity.id} className="activity-item">
                <div className={`activity-icon ${activity.type}`}>
                  {activity.type === 'new' ? '🆕' : activity.result === 'Positif' ? '⚠️' : '✅'}
                </div>
                <div className="activity-details">
                  <p>
                    <strong>{activity.action || 'Analyse réalisée'}</strong> - {activity.patient}
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
              </div>
            ))}
          </div>
        </div>

        {/* Calendar Card */}
        <div className="dashboard-card calendar-card">
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
                  {day === 8 && <div className="event-marker"></div>}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Tasks Card */}
        <div className="dashboard-card tasks-card">
          <div className="card-header">
            <h2>Tâches à venir</h2>
            <button className="add-task">+</button>
          </div>
          <div className="task-list">
            {upcomingTasks.map(task => (
              <div key={task.id} className={`task-item ${task.priority}`}>
                <div className="task-checkbox"></div>
                <div className="task-content">
                  <p>{task.title}</p>
                  <small>{task.time}</small>
                </div>
                <div className="task-actions">
                  <button>⋯</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Health Overview Card */}
        <div className="dashboard-card health-card">
          <div className="card-header">
            <h2>Aperçu santé</h2>
          </div>
          <div className="health-stats">
            <div className="health-stat">
              <div className="stat-circle" style={{ '--progress': '75%' }}>
                <span>75%</span>
              </div>
              <p>Cas résolus</p>
            </div>
            <div className="health-stat">
              <div className="stat-circle" style={{ '--progress': '85%' }}>
                <span>85%</span>
              </div>
              <p>Précision</p>
            </div>
            <div className="health-stat">
              <div className="stat-circle" style={{ '--progress': '92%' }}>
                <span>92%</span>
              </div>
              <p>Satisfaction</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;