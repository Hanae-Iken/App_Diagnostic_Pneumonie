// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import axios from 'axios';

// const NewAnalysis = () => {
//   const [formData, setFormData] = useState({
//     fullName: '',
//     age: '',
//     cin: '',
//     symptoms: '',
//     notes: '',
//     file: null
//   });
  
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState('');
//   const [analysisResult, setAnalysisResult] = useState(null);
  
//   const navigate = useNavigate();

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setFormData(prev => ({ ...prev, [name]: value }));
//   };

//   const handleFileChange = (e) => {
//     setFormData(prev => ({ ...prev, file: e.target.files[0] }));
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setIsLoading(true);
//     setError('');
//     setAnalysisResult(null);

//     try {
//       const token = localStorage.getItem('token');
      
//       // Étape 1: Upload du fichier
//       const formDataToSend = new FormData();
//       formDataToSend.append('file', formData.file);
//       formDataToSend.append('fullName', formData.fullName);
//       formDataToSend.append('age', formData.age);
//       formDataToSend.append('cin', formData.cin);
//       formDataToSend.append('symptoms', formData.symptoms);
//       formDataToSend.append('notes', formData.notes);

//       console.log('📤 Upload en cours...');
//       const uploadResponse = await axios.post('http://localhost:5000/upload', formDataToSend, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//           'Authorization': `Bearer ${token}`
//         }
//       });

//       if (uploadResponse.status === 200) {
//         const fileId = uploadResponse.data.fileId;
//         console.log('✅ Upload réussi, ID:', fileId);

//         // Étape 2: Lancer l'analyse IA
//         console.log('🔍 Lancement de l\'analyse IA...');
//         const analysisResponse = await axios.post(
//           `http://localhost:5000/api/analyze/${fileId}`,
//           {},
//           {
//             headers: {
//               'Authorization': `Bearer ${token}`
//             }
//           }
//         );

//         if (analysisResponse.status === 200) {
//           console.log('✅ Analyse terminée:', analysisResponse.data.analysis);
//           setAnalysisResult(analysisResponse.data.analysis);
//         }
//       }
//     } catch (err) {
//       console.error('Erreur:', err);
//       setError(err.response?.data?.error || 'Erreur lors de l\'analyse');
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const resetForm = () => {
//     setFormData({
//       fullName: '',
//       age: '',
//       cin: '',
//       symptoms: '',
//       notes: '',
//       file: null
//     });
//     setAnalysisResult(null);
//     setError('');
//   };

//   return (
//     <div className="container mx-auto p-6 max-w-4xl">
//       <h1 className="text-3xl font-bold mb-6 text-center text-blue-800">
//         📊 Nouvelle Analyse Médicale
//       </h1>

//       {/* Affichage des erreurs */}
//       {error && (
//         <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
//           <strong>Erreur:</strong> {error}
//         </div>
//       )}

//       {/* Formulaire */}
//       {!analysisResult && (
//         <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
//           <form onSubmit={handleSubmit} className="space-y-4">
//             <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
//               {/* Nom Complet */}
//               <div>
//                 <label className="block text-sm font-medium text-gray-700 mb-1">
//                   Nom Complet *
//                 </label>
//                 <input
//                   type="text"
//                   name="fullName"
//                   value={formData.fullName}
//                   onChange={handleChange}
//                   className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                   required
//                 />
//               </div>

//               {/* Âge */}
//               <div>
//                 <label className="block text-sm font-medium text-gray-700 mb-1">
//                   Âge *
//                 </label>
//                 <input
//                   type="number"
//                   name="age"
//                   value={formData.age}
//                   onChange={handleChange}
//                   className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                   min="1"
//                   max="120"
//                   required
//                 />
//               </div>

//               {/* CIN */}
//               <div>
//                 <label className="block text-sm font-medium text-gray-700 mb-1">
//                   CIN *
//                 </label>
//                 <input
//                   type="text"
//                   name="cin"
//                   value={formData.cin}
//                   onChange={handleChange}
//                   className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                   required
//                 />
//               </div>

//               {/* Fichier */}
//               <div>
//                 <label className="block text-sm font-medium text-gray-700 mb-1">
//                   Image Médicale * (.png, .jpg, .jpeg, .dcm)
//                 </label>
//                 <input
//                   type="file"
//                   name="file"
//                   onChange={handleFileChange}
//                   className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                   accept=".png,.jpg,.jpeg,.dcm"
//                   required
//                 />
//               </div>
//             </div>

//             {/* Symptômes */}
//             <div>
//               <label className="block text-sm font-medium text-gray-700 mb-1">
//                 Symptômes *
//               </label>
//               <textarea
//                 name="symptoms"
//                 value={formData.symptoms}
//                 onChange={handleChange}
//                 className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                 rows="3"
//                 placeholder="Décrivez les symptômes du patient..."
//                 required
//               />
//             </div>

//             {/* Notes */}
//             <div>
//               <label className="block text-sm font-medium text-gray-700 mb-1">
//                 Notes supplémentaires
//               </label>
//               <textarea
//                 name="notes"
//                 value={formData.notes}
//                 onChange={handleChange}
//                 className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                 rows="2"
//                 placeholder="Notes additionnelles (optionnel)..."
//               />
//             </div>

//             {/* Bouton Submit */}
//             <div className="flex justify-center">
//               <button
//                 type="submit"
//                 disabled={isLoading}
//                 className={`px-8 py-3 rounded-lg font-medium text-white ${
//                   isLoading
//                     ? 'bg-gray-400 cursor-not-allowed'
//                     : 'bg-blue-600 hover:bg-blue-700'
//                 }`}
//               >
//                 {isLoading ? (
//                   <div className="flex items-center">
//                     <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
//                     Analyse en cours...
//                   </div>
//                 ) : (
//                   '🔍 Analyser l\'image'
//                 )}
//               </button>
//             </div>
//           </form>
//         </div>
//       )}

//       {/* Résultats de l'analyse */}
//       {analysisResult && (
//         <div className="bg-white shadow-lg rounded-lg p-6">
//           <h2 className="text-2xl font-bold mb-4 text-center">
//             🎯 Résultats de l'Analyse IA
//           </h2>

//           {/* Patient Info */}
//           <div className="bg-gray-50 p-4 rounded-lg mb-4">
//             <h3 className="font-semibold text-gray-700 mb-2">👤 Informations Patient</h3>
//             <p><strong>Nom:</strong> {analysisResult.patient?.nomComplet}</p>
//             <p><strong>Âge:</strong> {analysisResult.patient?.age} ans</p>
//             <p><strong>CIN:</strong> {analysisResult.patient?.cin}</p>
//           </div>

//           {/* Diagnostic */}
//           <div className={`p-6 rounded-lg border-2 mb-4 text-center ${
//             analysisResult.resultat === 'NORMAL' 
//               ? 'bg-green-50 border-green-200 text-green-800' 
//               : 'bg-red-50 border-red-200 text-red-800'
//           }`}>
//             <h3 className="text-2xl font-bold mb-2">
//               {analysisResult.resultat === 'NORMAL' ? '✅ NORMAL' : '⚠️ PNEUMONIE DÉTECTÉE'}
//             </h3>
//             <p className="text-lg font-semibold">
//               Confiance: {(analysisResult.confiance * 100).toFixed(1)}%
//             </p>
//           </div>

//           {/* Détails */}
//           {analysisResult.details && (
//             <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
//               {/* Probabilités */}
//               <div className="bg-blue-50 p-4 rounded-lg">
//                 <h4 className="font-semibold mb-2 text-blue-800">📊 Probabilités</h4>
//                 <div className="space-y-1 text-sm">
//                   <div>Normal: {(analysisResult.details.probabilite_normale * 100).toFixed(1)}%</div>
//                   <div>Pneumonie: {(analysisResult.details.probabilite_pneumonie * 100).toFixed(1)}%</div>
//                 </div>
//               </div>

//               {/* Informations supplémentaires */}
//               <div className="bg-gray-50 p-4 rounded-lg">
//                 <h4 className="font-semibold mb-2 text-gray-800">ℹ️ Détails</h4>
//                 <div className="space-y-1 text-sm">
//                   <div><strong>Sévérité:</strong> {analysisResult.details.severite}</div>
//                   <div><strong>Zone:</strong> {analysisResult.details.zone_affectee}</div>
//                   <div><strong>Modèle:</strong> {analysisResult.details.modele_utilise}</div>
//                 </div>
//               </div>
//             </div>
//           )}

//           {/* Recommandations */}
//           {analysisResult.details?.recommendations && (
//             <div className="bg-yellow-50 p-4 rounded-lg mb-4">
//               <h4 className="font-semibold mb-3 text-yellow-800">💡 Recommandations</h4>
//               <ul className="list-disc list-inside space-y-1 text-sm text-yellow-700">
//                 {analysisResult.details.recommendations.map((rec, index) => (
//                   <li key={index}>{rec}</li>
//                 ))}
//               </ul>
//             </div>
//           )}

//           {/* Date d'analyse */}
//           <div className="text-center text-sm text-gray-500 mb-4">
//             Analysé le: {new Date(analysisResult.dateAnalyse).toLocaleString('fr-FR')}
//           </div>

//           {/* Actions */}
//           <div className="flex justify-center space-x-4">
//             <button
//               onClick={resetForm}
//               className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg"
//             >
//               📋 Nouvelle Analyse
//             </button>
//             {/* <button
//               onClick={() => navigate('/image-library')}
//               className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg"
//             >
//               📚 Voir Bibliothèque
//             </button> */}
//             <button
//               onClick={() => window.print()}
//               className="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg"
//             >
//               🖨️ Imprimer
//             </button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default NewAnalysis;import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import axios from 'axios';

// const NewAnalysis = () => {
//   const [formData, setFormData] = useState({
//     fullName: '',
//     age: '',
//     cin: '',
//     symptoms: '',
//     notes: '',
//     file: null
//   });
  
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState('');
//   const [analysisResult, setAnalysisResult] = useState(null);
  
//   const navigate = useNavigate();

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setFormData(prev => ({ ...prev, [name]: value }));
//   };

//   const handleFileChange = (e) => {
//     setFormData(prev => ({ ...prev, file: e.target.files[0] }));
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setIsLoading(true);
//     setError('');
//     setAnalysisResult(null);

//     try {
//       const token = localStorage.getItem('token');
      
//       // Étape 1: Upload du fichier
//       const formDataToSend = new FormData();
//       formDataToSend.append('file', formData.file);
//       formDataToSend.append('fullName', formData.fullName);
//       formDataToSend.append('age', formData.age);
//       formDataToSend.append('cin', formData.cin);
//       formDataToSend.append('symptoms', formData.symptoms);
//       formDataToSend.append('notes', formData.notes);

//       console.log('📤 Upload en cours...');
//       const uploadResponse = await axios.post('http://localhost:5000/upload', formDataToSend, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//           'Authorization': `Bearer ${token}`
//         }
//       });

//       if (uploadResponse.status === 200) {
//         const fileId = uploadResponse.data.fileId;
//         console.log('✅ Upload réussi, ID:', fileId);

//         // Étape 2: Lancer l'analyse IA
//         console.log('🔍 Lancement de l\'analyse IA...');
//         const analysisResponse = await axios.post(
//           `http://localhost:5000/api/analyze/${fileId}`,
//           {},
//           {
//             headers: {
//               'Authorization': `Bearer ${token}`
//             }
//           }
//         );

//         if (analysisResponse.status === 200) {
//           console.log('✅ Analyse terminée:', analysisResponse.data.analysis);
//           setAnalysisResult(analysisResponse.data.analysis);
//         }
//       }
//     } catch (err) {
//       console.error('Erreur:', err);
//       setError(err.response?.data?.error || 'Erreur lors de l\'analyse');
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const resetForm = () => {
//     setFormData({
//       fullName: '',
//       age: '',
//       cin: '',
//       symptoms: '',
//       notes: '',
//       file: null
//     });
//     setAnalysisResult(null);
//     setError('');
//   };

//   return (
//     <div className="container mx-auto p-6 max-w-4xl">
//       <h1 className="text-3xl font-bold mb-6 text-center text-blue-800">
//         📊 Nouvelle Analyse Médicale
//       </h1>

//       {/* Affichage des erreurs */}
//       {error && (
//         <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
//           <strong>Erreur:</strong> {error}
//         </div>
//       )}

//       {/* Formulaire */}
//       {!analysisResult && (
//         <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
//           <form onSubmit={handleSubmit} className="space-y-4">
//             <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
//               {/* Nom Complet */}
//               <div>
//                 <label className="block text-sm font-medium text-gray-700 mb-1">
//                   Nom Complet *
//                 </label>
//                 <input
//                   type="text"
//                   name="fullName"
//                   value={formData.fullName}
//                   onChange={handleChange}
//                   className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                   required
//                 />
//               </div>

//               {/* Âge */}
//               <div>
//                 <label className="block text-sm font-medium text-gray-700 mb-1">
//                   Âge *
//                 </label>
//                 <input
//                   type="number"
//                   name="age"
//                   value={formData.age}
//                   onChange={handleChange}
//                   className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                   min="1"
//                   max="120"
//                   required
//                 />
//               </div>

//               {/* CIN */}
//               <div>
//                 <label className="block text-sm font-medium text-gray-700 mb-1">
//                   CIN *
//                 </label>
//                 <input
//                   type="text"
//                   name="cin"
//                   value={formData.cin}
//                   onChange={handleChange}
//                   className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                   required
//                 />
//               </div>

//               {/* Fichier */}
//               <div>
//                 <label className="block text-sm font-medium text-gray-700 mb-1">
//                   Image Médicale * (.png, .jpg, .jpeg, .dcm)
//                 </label>
//                 <input
//                   type="file"
//                   name="file"
//                   onChange={handleFileChange}
//                   className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                   accept=".png,.jpg,.jpeg,.dcm"
//                   required
//                 />
//               </div>
//             </div>

//             {/* Symptômes */}
//             <div>
//               <label className="block text-sm font-medium text-gray-700 mb-1">
//                 Symptômes *
//               </label>
//               <textarea
//                 name="symptoms"
//                 value={formData.symptoms}
//                 onChange={handleChange}
//                 className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                 rows="3"
//                 placeholder="Décrivez les symptômes du patient..."
//                 required
//               />
//             </div>

//             {/* Notes */}
//             <div>
//               <label className="block text-sm font-medium text-gray-700 mb-1">
//                 Notes supplémentaires
//               </label>
//               <textarea
//                 name="notes"
//                 value={formData.notes}
//                 onChange={handleChange}
//                 className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
//                 rows="2"
//                 placeholder="Notes additionnelles (optionnel)..."
//               />
//             </div>

//             {/* Bouton Submit */}
//             <div className="flex justify-center">
//               <button
//                 type="submit"
//                 disabled={isLoading}
//                 className={`px-8 py-3 rounded-lg font-medium text-white ${
//                   isLoading
//                     ? 'bg-gray-400 cursor-not-allowed'
//                     : 'bg-blue-600 hover:bg-blue-700'
//                 }`}
//               >
//                 {isLoading ? (
//                   <div className="flex items-center">
//                     <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
//                     Analyse en cours...
//                   </div>
//                 ) : (
//                   '🔍 Analyser l\'image'
//                 )}
//               </button>
//             </div>
//           </form>
//         </div>
//       )}

//       {/* Résultats de l'analyse */}
//       {analysisResult && (
//         <div className="bg-white shadow-lg rounded-lg p-6">
//           <h2 className="text-2xl font-bold mb-4 text-center">
//             🎯 Résultats de l'Analyse IA
//           </h2>

//           {/* Patient Info */}
//           <div className="bg-gray-50 p-4 rounded-lg mb-4">
//             <h3 className="font-semibold text-gray-700 mb-2">👤 Informations Patient</h3>
//             <p><strong>Nom:</strong> {analysisResult.patient?.nomComplet}</p>
//             <p><strong>Âge:</strong> {analysisResult.patient?.age} ans</p>
//             <p><strong>CIN:</strong> {analysisResult.patient?.cin}</p>
//           </div>

//           {/* Diagnostic */}
//           <div className={`p-6 rounded-lg border-2 mb-4 text-center ${
//             analysisResult.resultat === 'NORMAL' 
//               ? 'bg-green-50 border-green-200 text-green-800' 
//               : 'bg-red-50 border-red-200 text-red-800'
//           }`}>
//             <h3 className="text-2xl font-bold mb-2">
//               {analysisResult.resultat === 'NORMAL' ? '✅ NORMAL' : '⚠️ PNEUMONIE DÉTECTÉE'}
//             </h3>
//             <p className="text-lg font-semibold">
//               Confiance: {(analysisResult.confiance * 100).toFixed(1)}%
//             </p>
//           </div>

//           {/* Détails */}
//           {analysisResult.details && (
//             <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
//               {/* Probabilités */}
//               <div className="bg-blue-50 p-4 rounded-lg">
//                 <h4 className="font-semibold mb-2 text-blue-800">📊 Probabilités</h4>
//                 <div className="space-y-1 text-sm">
//                   <div>Normal: {(analysisResult.details.probabilite_normale * 100).toFixed(1)}%</div>
//                   <div>Pneumonie: {(analysisResult.details.probabilite_pneumonie * 100).toFixed(1)}%</div>
//                 </div>
//               </div>

//               {/* Informations supplémentaires */}
//               <div className="bg-gray-50 p-4 rounded-lg">
//                 <h4 className="font-semibold mb-2 text-gray-800">ℹ️ Détails</h4>
//                 <div className="space-y-1 text-sm">
//                   <div><strong>Sévérité:</strong> {analysisResult.details.severite}</div>
//                   <div><strong>Zone:</strong> {analysisResult.details.zone_affectee}</div>
//                   <div><strong>Modèle:</strong> {analysisResult.details.modele_utilise}</div>
//                 </div>
//               </div>
//             </div>
//           )}

//           {/* Recommandations */}
//           {analysisResult.details?.recommendations && (
//             <div className="bg-yellow-50 p-4 rounded-lg mb-4">
//               <h4 className="font-semibold mb-3 text-yellow-800">💡 Recommandations</h4>
//               <ul className="list-disc list-inside space-y-1 text-sm text-yellow-700">
//                 {analysisResult.details.recommendations.map((rec, index) => (
//                   <li key={index}>{rec}</li>
//                 ))}
//               </ul>
//             </div>
//           )}

//           {/* Date d'analyse */}
//           <div className="text-center text-sm text-gray-500 mb-4">
//             Analysé le: {new Date(analysisResult.dateAnalyse).toLocaleString('fr-FR')}
//           </div>

//           {/* Actions */}
//           <div className="flex justify-center space-x-4">
//             <button
//               onClick={resetForm}
//               className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg"
//             >
//               📋 Nouvelle Analyse
//             </button>
//             {/* <button
//               onClick={() => navigate('/image-library')}
//               className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg"
//             >
//               📚 Voir Bibliothèque
//             </button> */}
//             <button
//               onClick={() => window.print()}
//               className="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg"
//             >
//               🖨️ Imprimer
//             </button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default NewAnalysis;


import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const NewAnalysis = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    age: '',
    cin: '',
    symptoms: '',
    notes: '',
    file: null
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    setFormData(prev => ({ ...prev, file: e.target.files[0] }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setAnalysisResult(null);

    try {
      const token = localStorage.getItem('token');
      
      // Étape 1: Upload du fichier
      const formDataToSend = new FormData();
      formDataToSend.append('file', formData.file);
      formDataToSend.append('fullName', formData.fullName);
      formDataToSend.append('age', formData.age);
      formDataToSend.append('cin', formData.cin);
      formDataToSend.append('symptoms', formData.symptoms);
      formDataToSend.append('notes', formData.notes);

      console.log('📤 Upload en cours...');
      const uploadResponse = await axios.post('http://localhost:5000/upload', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      });

      if (uploadResponse.status === 200) {
        const fileId = uploadResponse.data.fileId;
        console.log('✅ Upload réussi, ID:', fileId);

        // Étape 2: Lancer l'analyse IA
        console.log('🔍 Lancement de l\'analyse IA...');
        const analysisResponse = await axios.post(
          `http://localhost:5000/api/analyze/${fileId}`,
          {},
          {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          }
        );

        if (analysisResponse.status === 200) {
          console.log('✅ Analyse terminée:', analysisResponse.data.analysis);
          setAnalysisResult(analysisResponse.data.analysis);
        }
      }
    } catch (err) {
      console.error('Erreur:', err);
      setError(err.response?.data?.error || 'Erreur lors de l\'analyse');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      fullName: '',
      age: '',
      cin: '',
      symptoms: '',
      notes: '',
      file: null
    });
    setAnalysisResult(null);
    setError('');
  };

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <h1 className="text-3xl font-bold mb-6 text-center text-blue-800">
        📊 Nouvelle Analyse Médicale
      </h1>

      {/* Affichage des erreurs */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <strong>Erreur:</strong> {error}
        </div>
      )}

      {/* Formulaire */}
      {!analysisResult && (
        <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Nom Complet */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nom Complet *
                </label>
                <input
                  type="text"
                  name="fullName"
                  value={formData.fullName}
                  onChange={handleChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              {/* Âge */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Âge *
                </label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  min="1"
                  max="120"
                  required
                />
              </div>

              {/* CIN */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  CIN *
                </label>
                <input
                  type="text"
                  name="cin"
                  value={formData.cin}
                  onChange={handleChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              {/* Fichier */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Image Médicale * (.png, .jpg, .jpeg, .dcm)
                </label>
                <input
                  type="file"
                  name="file"
                  onChange={handleFileChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  accept=".png,.jpg,.jpeg,.dcm"
                  required
                />
              </div>
            </div>

            {/* Symptômes */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Symptômes *
              </label>
              <textarea
                name="symptoms"
                value={formData.symptoms}
                onChange={handleChange}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                rows="3"
                placeholder="Décrivez les symptômes du patient..."
                required
              />
            </div>

            {/* Notes */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Notes supplémentaires
              </label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                rows="2"
                placeholder="Notes additionnelles (optionnel)..."
              />
            </div>

            {/* Bouton Submit */}
            <div className="flex justify-center">
              <button
                type="submit"
                disabled={isLoading}
                className={`px-8 py-3 rounded-lg font-medium text-white ${
                  isLoading
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700'
                }`}
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Analyse en cours...
                  </div>
                ) : (
                  '🔍 Analyser l\'image'
                )}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Résultats de l'analyse */}
      {analysisResult && (
        <div className="bg-white shadow-lg rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-6 text-center">
            🎯 Résultats de l'Analyse IA
          </h2>

          {/* Patient Info */}
          <div className="bg-gray-50 p-4 rounded-lg mb-6">
            <h3 className="font-semibold text-gray-700 mb-2">👤 Informations Patient</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <p><strong>Nom:</strong> {analysisResult.patient?.nomComplet}</p>
              <p><strong>Âge:</strong> {analysisResult.patient?.age} ans</p>
              <p><strong>CIN:</strong> {analysisResult.patient?.cin}</p>
            </div>
          </div>

          {/* Diagnostic */}
          <div className={`p-6 rounded-lg border-2 mb-6 text-center ${
            analysisResult.resultat === 'NORMAL'
              ? 'bg-green-50 border-green-200 text-green-800'
              : 'bg-red-50 border-red-200 text-red-800'
          }`}>
            <h3 className="text-2xl font-bold mb-2">
              {analysisResult.resultat === 'NORMAL' ? '✅ NORMAL' : '⚠️ PNEUMONIE'}
            </h3>
            <p className="text-lg font-semibold">
              Confiance: {(analysisResult.confiance * 100).toFixed(1)}%
            </p>
          </div>

          {/* Image originale et heatmap côte à côte */}
          {analysisResult.heatmap && (
            <div className="mb-6">
              <h3 className="text-xl font-semibold mb-4 text-center">🔥 Analyse Visuelle avec Heatmap</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Heatmap */}
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold mb-3 text-center text-red-600">
                    Heatmap - Zones d'influence IA
                  </h4>
                  <div className="flex justify-center">
                    <img 
                      src={analysisResult.heatmap} 
                      alt="Heatmap de l'analyse" 
                      className="max-w-full h-auto rounded-lg shadow-lg border border-gray-200"
                      style={{ maxHeight: '400px' }}
                    />
                  </div>
                  <p className="text-sm text-gray-600 mt-2 text-center">
                    Les zones rouges indiquent les régions qui ont le plus influencé la prédiction "{analysisResult.resultat}"
                  </p>
                </div>

                {/* Détails et probabilités */}
                <div className="space-y-4">
                  {/* Probabilités */}
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-semibold mb-3 text-blue-800">📊 Probabilités</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Normal:</span>
                        <span className="font-semibold">
                          {(analysisResult.details.probabilite_normale * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-green-500 h-2 rounded-full" 
                          style={{ width: `${analysisResult.details.probabilite_normale * 100}%` }}
                        ></div>
                      </div>
                      
                      <div className="flex justify-between">
                        <span>Pneumonie:</span>
                        <span className="font-semibold">
                          {(analysisResult.details.probabilite_pneumonie * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-red-500 h-2 rounded-full" 
                          style={{ width: `${analysisResult.details.probabilite_pneumonie * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>

                  {/* Informations supplémentaires */}
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h4 className="font-semibold mb-3 text-gray-800">ℹ️ Détails</h4>
                    <div className="space-y-2 text-sm">
                      <div><strong>Sévérité:</strong> {analysisResult.details.severite}</div>
                      <div><strong>Zone:</strong> {analysisResult.details.zone_affectee}</div>
                      <div><strong>Modèle:</strong> {analysisResult.details.modele_utilise}</div>
                    </div>
                  </div>

                  {/* Recommandations */}
                  {analysisResult.details?.recommendations && (
                    <div className="bg-yellow-50 p-4 rounded-lg">
                      <h4 className="font-semibold mb-3 text-yellow-800">💡 Recommandations</h4>
                      <ul className="list-disc list-inside space-y-1 text-sm text-yellow-700">
                        {analysisResult.details.recommendations.map((rec, index) => (
                          <li key={index}>{rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Date d'analyse */}
          <div className="text-center text-sm text-gray-500 mb-6">
            Analysé le: {new Date(analysisResult.dateAnalyse).toLocaleString('fr-FR')}
          </div>

          {/* Actions */}
          <div className="flex justify-center space-x-4">
            <button
              onClick={resetForm}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
            >
              📋 Nouvelle Analyse
            </button>
            <button
              onClick={() => window.print()}
              className="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg transition-colors"
            >
              🖨️ Imprimer
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default NewAnalysis;