import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './Nouvel_diagno/Layout';
import Dashboard from './ESPmedc/MEDC';
import NewAnalysis from './Nouvel_diagno/NOVANALY';
import ImageLibrary from './Bibliotheque/BiblioIMG';
import Patients from './MesPatients/MesPats';
import History from './Historique/Historic';
import Statistics from './Statistique/Statistic';
import Settings from './Parametres/Parametr';
import SignIn from './SingIn/SignIn'; // Ajoutez ces imports
import SignUp from './SignUp/Singup';
import ProtectedRoute from './page/ProtecteRoute';

// ... dans vos Routes
<Route path="/" element={
  <ProtectedRoute>
    <Layout />
  </ProtectedRoute>
}>
  {/* routes protégées */}
</Route>

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/signin" element={<SignIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="new-analysis" element={<NewAnalysis />} />
          <Route path="image-library" element={<ImageLibrary />} />
          <Route path="patients" element={<Patients />} />
          <Route path="history" element={<History />} />
          <Route path="statistics" element={<Statistics />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;