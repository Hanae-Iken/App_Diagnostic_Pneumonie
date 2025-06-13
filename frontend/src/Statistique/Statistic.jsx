import React from 'react';
import { FiPieChart, FiBarChart2, FiTrendingUp, FiDownload } from 'react-icons/fi';
import './Statistic.css';

const Statistic = () => {
  const stats = {
    totalPatients: 127,
    positiveCases: 42,
    negativeCases: 85,
    recoveryRate: 68,
    monthlyData: [
      { month: 'Jan', positive: 12, negative: 28 },
      { month: 'Fév', positive: 18, negative: 22 },
      { month: 'Mar', positive: 25, negative: 15 },
      { month: 'Avr', positive: 32, negative: 18 },
      { month: 'Mai', positive: 42, negative: 43 }
    ]
  };

  return (
   <div className="full-page">
    <div className="statistics-container">
      <div className="statistics-header">
        <h1>Statistiques médicales</h1>
        <button className="export-btn">
          <FiDownload size={16} />
          Exporter
        </button>
      </div>

      <div className="stats-overview">
        <div className="stat-card total">
          <div className="stat-icon">
            <FiPieChart size={24} />
          </div>
          <div className="stat-content">
            <h3>Patients total</h3>
            <p>{stats.totalPatients}</p>
          </div>
        </div>
        
        <div className="stat-card positive">
          <div className="stat-icon">
            <FiTrendingUp size={24} />
          </div>
          <div className="stat-content">
            <h3>Cas positifs</h3>
            <p>{stats.positiveCases} <span>({Math.round((stats.positiveCases/stats.totalPatients)*100)}%)</span></p>
          </div>
        </div>
        
        <div className="stat-card negative">
          <div className="stat-icon">
            <FiTrendingUp size={24} />
          </div>
          <div className="stat-content">
            <h3>Cas négatifs</h3>
            <p>{stats.negativeCases} <span>({Math.round((stats.negativeCases/stats.totalPatients)*100)}%)</span></p>
          </div>
        </div>
        
        <div className="stat-card recovery">
          <div className="stat-icon">
            <FiBarChart2 size={24} />
          </div>
          <div className="stat-content">
            <h3>Taux de guérison</h3>
            <p>{stats.recoveryRate}%</p>
          </div>
        </div>
      </div>

      <div className="charts-container">
        <div className="chart-card">
          <div className="chart-header">
            <h2>Répartition des cas</h2>
            <div className="chart-legend">
              <div className="legend-item positive">
                <span></span>
                Positifs
              </div>
              <div className="legend-item negative">
                <span></span>
                Négatifs
              </div>
            </div>
          </div>
          <div className="pie-chart-placeholder">
            {/* Ici vous intégrerez un vrai graphique avec Chart.js ou autre */}
            <div className="pie-chart">
              <div 
                className="pie-segment positive" 
                style={{ '--percentage': `${(stats.positiveCases/stats.totalPatients)*100}%` }}
              ></div>
              <div 
                className="pie-segment negative" 
                style={{ '--percentage': `${(stats.negativeCases/stats.totalPatients)*100}%` }}
              ></div>
              <div className="pie-center">
                <span>{Math.round((stats.positiveCases/stats.totalPatients)*100)}%</span>
                <small>Positifs</small>
              </div>
            </div>
          </div>
        </div>
        
        <div className="chart-card">
          <div className="chart-header">
            <h2>Évolution mensuelle</h2>
            <select defaultValue="2023">
              <option>2023</option>
              <option>2022</option>
              <option>2021</option>
            </select>
          </div>
          <div className="bar-chart-placeholder">
            {/* Ici vous intégrerez un vrai graphique avec Chart.js ou autre */}
            <div className="bar-chart">
              {stats.monthlyData.map((data, index) => (
                <div key={index} className="bar-group">
                  <div className="bar positive" style={{ height: `${(data.positive/50)*100}%` }}></div>
                  <div className="bar negative" style={{ height: `${(data.negative/50)*100}%` }}></div>
                  <span>{data.month}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  );
};

export default Statistic;