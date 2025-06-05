import MedcStats from './MedcStats';
import PatientQueue from '../components/PatientQueue'; // Exemple de composant réutilisé
import RecentDiagnoses from './RecentDiagnoses';

export default function MedcDashboard() {
  return (
    <div className="medc-dashboard">
      <h2>Tableau de Bord Médical</h2>
      <MedcStats />
      <div className="medc-grid">
        <PatientQueue />
        <RecentDiagnoses />
      </div>
    </div>
  );
}