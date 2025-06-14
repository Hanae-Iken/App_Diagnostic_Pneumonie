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

        try {
            const formDataToSend = new FormData();
            formDataToSend.append('file', formData.file);
            formDataToSend.append('fullName', formData.fullName);
            formDataToSend.append('age', formData.age);
            formDataToSend.append('cin', formData.cin);
            formDataToSend.append('symptoms', formData.symptoms);
            formDataToSend.append('notes', formData.notes);

            const token = localStorage.getItem('token');
            const response = await axios.post('http://localhost:5000/upload', formDataToSend, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.status === 200) {
                navigate('/image-library', { state: { success: 'Analyse créée avec succès!' } });
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Erreur lors de l\'envoi du fichier');
            console.error('Upload error:', err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container mx-auto p-6">
            <h1 className="text-2xl font-bold mb-6">Nouvelle Analyse Médicale</h1>
            
            {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">{error}</div>}

            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label className="block mb-2">Nom Complet</label>
                        <input
                            type="text"
                            name="fullName"
                            value={formData.fullName}
                            onChange={handleChange}
                            className="w-full p-2 border rounded"
                            required
                        />
                    </div>

                    <div>
                        <label className="block mb-2">Âge</label>
                        <input
                            type="number"
                            name="age"
                            value={formData.age}
                            onChange={handleChange}
                            className="w-full p-2 border rounded"
                            min="1"
                            max="120"
                            required
                        />
                    </div>

                    <div>
                        <label className="block mb-2">CIN</label>
                        <input
                            type="text"
                            name="cin"
                            value={formData.cin}
                            onChange={handleChange}
                            className="w-full p-2 border rounded"
                            pattern="[A-Za-z]{1,2}[0-9]{6}"
                            title="Format CIN: 1-2 lettres suivies de 6 chiffres"
                            required
                        />
                    </div>

                    <div>
                        <label className="block mb-2">Image Médicale</label>
                        <input
                            type="file"
                            name="file"
                            onChange={handleFileChange}
                            className="w-full p-2 border rounded"
                            accept=".png,.jpg,.jpeg,.dcm"
                            required
                        />
                    </div>
                </div>

                <div>
                    <label className="block mb-2">Symptômes</label>
                    <textarea
                        name="symptoms"
                        value={formData.symptoms}
                        onChange={handleChange}
                        className="w-full p-2 border rounded"
                        rows="3"
                        required
                    />
                </div>

                <div>
                    <label className="block mb-2">Notes supplémentaires</label>
                    <textarea
                        name="notes"
                        value={formData.notes}
                        onChange={handleChange}
                        className="w-full p-2 border rounded"
                        rows="2"
                    />
                </div>

                <button
                    type="submit"
                    disabled={isLoading}
                    className={`bg-blue-600 text-white px-4 py-2 rounded ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'}`}
                >
                    {isLoading ? 'Envoi en cours...' : 'Soumettre l\'analyse'}
                </button>
            </form>
        </div>
    );
};

export default NewAnalysis;