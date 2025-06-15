import React, { useState, useEffect } from 'react';
import { FiCalendar, FiChevronDown, FiEye, FiUser, FiClock } from 'react-icons/fi';

const Historic = () => {
  const [timeFilter, setTimeFilter] = useState('week');
  const [historyItems, setHistoryItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState(null);
  const [error, setError] = useState(null);

  // Charger l'historique
  const loadHistory = async (filter = 'week') => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('token');
      
      if (!token) {
        setError('Token d\'authentification manquant');
        return;
      }
      
      console.log(`Chargement historique avec filtre: ${filter}`);
      
      const response = await fetch(`http://localhost:5000/api/history?filter=${filter}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      console.log('Réponse reçue:', response.status);

      if (response.ok) {
        const data = await response.json();
        console.log('Données reçues:', data);
        setHistoryItems(data.historique || []);
      } else {
        const errorData = await response.json();
        console.error('Erreur API:', errorData);
        setError(errorData.error || 'Erreur chargement historique');
        setHistoryItems([]);
      }
    } catch (error) {
      console.error('Erreur réseau:', error);
      setError('Erreur de connexion au serveur');
      setHistoryItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory(timeFilter);
  }, [timeFilter]);

  const handleTimeFilterChange = (newFilter) => {
    setTimeFilter(newFilter);
  };

  const openDetails = (item) => {
    setSelectedItem(item);
  };

  const closeDetails = () => {
    setSelectedItem(null);
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '400px',
        fontSize: '18px'
      }}>
        Chargement de l'historique...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ 
        display: 'flex', 
        flexDirection: 'column',
        alignItems: 'center', 
        padding: '40px',
        color: '#e74c3c'
      }}>
        <h3>Erreur</h3>
        <p>{error}</p>
        <button 
          onClick={() => loadHistory(timeFilter)}
          style={{
            padding: '10px 20px',
            backgroundColor: '#3498db',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            marginTop: '20px'
          }}
        >
          Réessayer
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '30px',
        paddingBottom: '20px',
        borderBottom: '2px solid #ecf0f1'
      }}>
        <h1 style={{ color: '#2c3e50', fontSize: '28px' }}>
          Historique des analyses
        </h1>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <FiCalendar style={{ color: '#7f8c8d' }} />
          <select 
            value={timeFilter} 
            onChange={(e) => handleTimeFilterChange(e.target.value)}
            style={{
              padding: '10px 15px',
              border: '2px solid #bdc3c7',
              borderRadius: '8px',
              fontSize: '16px',
              backgroundColor: 'white'
            }}
          >
            <option value="day">Aujourd'hui</option>
            <option value="week">Cette semaine</option>
            <option value="month">Ce mois</option>
            <option value="all">Tout l'historique</option>
          </select>
        </div>
      </div>

      {/* Liste des analyses */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {historyItems.length > 0 ? (
          historyItems.map(item => (
            <div 
              key={item.id} 
              style={{
                display: 'flex',
                backgroundColor: 'white',
                border: '1px solid #e0e0e0',
                borderRadius: '12px',
                padding: '20px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                transition: 'transform 0.2s',
                cursor: 'pointer'
              }}
              onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
              onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}
            >
              {/* Image */}
              <div style={{ marginRight: '20px', flexShrink: 0 }}>
                {item.image ? (
                  <img 
                    src={item.image} 
                    alt="Radiographie" 
                    style={{
                      width: '80px',
                      height: '80px',
                      objectFit: 'cover',
                      borderRadius: '8px',
                      border: '2px solid #ecf0f1'
                    }}
                  />
                ) : (
                  <div style={{
                    width: '80px',
                    height: '80px',
                    backgroundColor: '#f8f9fa',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    borderRadius: '8px',
                    color: '#6c757d',
                    fontSize: '12px'
                  }}>
                    Pas d'image
                  </div>
                )}
              </div>
              
              {/* Date et heure */}
              <div style={{ 
                display: 'flex', 
                flexDirection: 'column',
                alignItems: 'center',
                marginRight: '20px',
                minWidth: '100px'
              }}>
                <div style={{ 
                  fontSize: '16px', 
                  fontWeight: 'bold',
                  color: '#2c3e50'
                }}>
                  {item.date}
                </div>
                <div style={{ 
                  fontSize: '14px', 
                  color: '#7f8c8d',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px'
                }}>
                  <FiClock size={12} />
                  {item.time}
                </div>
              </div>
              
              {/* Contenu principal */}
              <div style={{ flex: 1 }}>
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center',
                  marginBottom: '10px',
                  gap: '10px'
                }}>
                  <FiUser style={{ color: '#3498db' }} />
                  <h3 style={{ 
                    margin: 0, 
                    color: '#2c3e50',
                    fontSize: '18px'
                  }}>
                    {item.patient.nomComplet}
                  </h3>
                  <span style={{ 
                    backgroundColor: '#ecf0f1',
                    padding: '4px 8px',
                    borderRadius: '4px',
                    fontSize: '12px',
                    color: '#7f8c8d'
                  }}>
                    {item.patient.age} ans
                  </span>
                </div>
                
                <div style={{ marginBottom: '10px' }}>
                  <p style={{ margin: '5px 0', fontSize: '14px', color: '#7f8c8d' }}>
                    <strong>CIN:</strong> {item.patient.cin}
                  </p>
                  <p style={{ margin: '5px 0', fontSize: '14px', color: '#7f8c8d' }}>
                    <strong>Symptômes:</strong> {item.patient.symptomes}
                  </p>
                </div>
                
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center',
                  gap: '15px'
                }}>
                  <span style={{
                    padding: '6px 12px',
                    borderRadius: '20px',
                    fontSize: '14px',
                    fontWeight: 'bold',
                    backgroundColor: item.resultat === 'PNEUMONIA' ? '#e74c3c' : '#27ae60',
                    color: 'white'
                  }}>
                    {item.resultat === 'PNEUMONIA' ? 'Pneumonie détectée' : 'Normal'}
                  </span>
                  <span style={{ 
                    fontSize: '14px',
                    color: '#7f8c8d'
                  }}>
                    Confiance: {item.confiance}%
                  </span>
                </div>
              </div>
              
              {/* Actions */}
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <button 
                  onClick={() => openDetails(item)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '12px 20px',
                    backgroundColor: '#3498db',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontSize: '14px',
                    transition: 'background-color 0.2s'
                  }}
                  onMouseOver={(e) => e.target.style.backgroundColor = '#2980b9'}
                  onMouseOut={(e) => e.target.style.backgroundColor = '#3498db'}
                >
                  <FiEye /> Détails
                </button>
              </div>
            </div>
          ))
        ) : (
          <div style={{
            textAlign: 'center',
            padding: '60px 20px',
            backgroundColor: '#f8f9fa',
            borderRadius: '12px',
            color: '#6c757d'
          }}>
            <h3>Aucune analyse trouvée</h3>
            <p>Aucune analyse n'a été trouvée pour cette période</p>
          </div>
        )}
      </div>

      {/* Modal pour les détails */}
      {selectedItem && (
        <div 
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000
          }}
          onClick={closeDetails}
        >
          <div 
            style={{
              backgroundColor: 'white',
              borderRadius: '12px',
              padding: '30px',
              maxWidth: '800px',
              width: '90%',
              maxHeight: '90%',
              overflow: 'auto'
            }}
            onClick={e => e.stopPropagation()}
          >
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '20px',
              paddingBottom: '15px',
              borderBottom: '1px solid #ecf0f1'
            }}>
              <h2 style={{ color: '#2c3e50' }}>
                Détails de l'analyse - {selectedItem.patient.nomComplet}
              </h2>
              <button 
                onClick={closeDetails}
                style={{
                  background: 'none',
                  border: 'none',
                  fontSize: '24px',
                  cursor: 'pointer',
                  color: '#7f8c8d'
                }}
              >
                ×
              </button>
            </div>
            
            <div>
              {/* Images */}
              <div style={{ 
                display: 'grid',
                gridTemplateColumns: selectedItem.heatmap ? '1fr 1fr' : '1fr',
                gap: '20px',
                marginBottom: '30px'
              }}>
                <div>
                  <h3 style={{ color: '#2c3e50', marginBottom: '10px' }}>
                    Image originale
                  </h3>
                  {selectedItem.image && (
                    <img 
                      src={selectedItem.image} 
                      alt="Radiographie originale"
                      style={{
                        width: '100%',
                        height: '300px',
                        objectFit: 'contain',
                        border: '1px solid #ecf0f1',
                        borderRadius: '8px'
                      }}
                    />
                  )}
                </div>
                
                {selectedItem.heatmap && (
                  <div>
                    <h3 style={{ color: '#2c3e50', marginBottom: '10px' }}>
                      Zones d'analyse IA
                    </h3>
                    <img 
                      src={selectedItem.heatmap} 
                      alt="Heatmap"
                      style={{
                        width: '100%',
                        height: '300px',
                        objectFit: 'contain',
                        border: '1px solid #ecf0f1',
                        borderRadius: '8px'
                      }}
                    />
                  </div>
                )}
              </div>
              
              {/* Détails de l'analyse */}
              <div>
                <h3 style={{ color: '#2c3e50', marginBottom: '15px' }}>
                  Résultats de l'analyse
                </h3>
                
                <div style={{ 
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '15px',
                  marginBottom: '20px'
                }}>
                  <p><strong>Résultat:</strong> {selectedItem.resultat}</p>
                  <p><strong>Confiance:</strong> {selectedItem.confiance}%</p>
                  <p><strong>Date:</strong> {selectedItem.date}</p>
                  <p><strong>Heure:</strong> {selectedItem.time}</p>
                </div>
                
                {selectedItem.details?.recommendations && (
                  <div>
                    <h4 style={{ color: '#2c3e50', marginBottom: '10px' }}>
                      Recommandations:
                    </h4>
                    <ul style={{ 
                      backgroundColor: '#f8f9fa',
                      padding: '15px',
                      borderRadius: '8px',
                      marginBottom: '0'
                    }}>
                      {selectedItem.details.recommendations.map((rec, index) => (
                        <li key={index} style={{ marginBottom: '5px' }}>
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Historic;