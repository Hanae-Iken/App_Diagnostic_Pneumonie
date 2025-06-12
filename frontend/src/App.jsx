import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import APropos from './pages/APropos';
import But from './pages/But';
import Fonctionnement from './pages/Fonctionnement';
import Feedbacks from './pages/Feedbacks';
import Footer from './components/Footer';
// autres imports...

<Routes>
  <Route path="/" element={<Accueil />} />
  <Route path="/apropos" element={<APropos />} />
  <Route path="/but" element={<But />} />
  <Route path="/fonctionnement" element={<Fonctionnement />} />
  <Route path="/feedbacks" element={<Feedbacks />} />
  {/* autres routes */}
</Routes>
function App() {
  return (
    <div className="App">
      <Navbar />
      <div id="hero"><Hero /></div>
      <div id="apropos"><Apropos /></div>
      <div id="but"><But /></div>
      <div id="fonctionnement"><Fonctionnement /></div>
      <div id="feedbacks"><Feedbacks /></div>
      <div id="contact"><Contact /></div>

      <Footer /> {/* ICI */}
    </div>
  );
}

