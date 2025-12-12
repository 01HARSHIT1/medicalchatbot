import React, { useState } from "react";
import axios from "axios";  // Import axios
import "./Logo1.css"; // Import the Logo1.css file

const Logo1 = () => {
  const [transcription, setTranscription] = useState("");
  const [predictedDisease, setPredictedDisease] = useState(null);
  const [error, setError] = useState(null);
  const [showDiseaseModal, setShowDiseaseModal] = useState(false);
  const [diseaseData, setDiseaseData] = useState(null);
  const [loading, setLoading] = useState(false);

  const startSpeechRecognition = () => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";

    recognition.onresult = (event) => {
      const result = event.results[0][0].transcript;
      setTranscription(result);
    };

    recognition.onend = () => {
      console.log("Speech recognition ended.");
    };

    recognition.start();
  };

  const handlePrediction = async () => {
    if (!transcription.trim()) {
      setError("Please enter symptoms first");
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      // Clean and split symptoms
      const symptoms = transcription.split(",").map(s => s.trim()).filter(s => s);
      
      // Get API URL from environment or use default
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:5000";
      
      // Check if we're in production and no API URL is configured
      const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';
      
      if (isProduction && !import.meta.env.VITE_API_URL) {
        setError(
          <div style={{textAlign: 'left', lineHeight: '1.8'}}>
            <h4 style={{color: '#ff6b6b', marginBottom: '15px'}}>🔧 Backend API Configuration Required</h4>
            <p style={{marginBottom: '10px'}}><strong>Quick Setup (5 minutes):</strong></p>
            <ol style={{marginLeft: '20px', marginBottom: '15px'}}>
              <li>Deploy backend to <a href="https://railway.app/new" target="_blank" rel="noopener noreferrer" style={{color: '#4dabf7'}}>Railway</a> (free tier available)</li>
              <li>Set <code style={{background: '#f1f3f5', padding: '2px 6px', borderRadius: '3px'}}>VITE_API_URL</code> in Vercel Settings → Environment Variables</li>
              <li>Redeploy your Vercel app</li>
            </ol>
            <p style={{marginTop: '15px', fontSize: '0.9em', color: '#868e96'}}>
              📖 See <code style={{background: '#f1f3f5', padding: '2px 6px'}}>backend-api/DEPLOY_NOW.md</code> for step-by-step instructions
            </p>
          </div>
        );
        setLoading(false);
        return;
      }
      
      const response = await axios.post(`${apiUrl}/predict`, {
        symptoms: symptoms,
      }, {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 10000 // 10 second timeout
      });
      
      if (response.data && response.data.predicted_disease) {
        setPredictedDisease(response.data);
        setError(null);
      } else {
        setError("Invalid response from server");
      }
    } catch (error) {
      console.error("Prediction error:", error);
      if (error.code === 'ECONNABORTED') {
        setError("Request timeout. The server is taking too long to respond.");
      } else if (error.response) {
        setError(`Server error: ${error.response.data?.error || error.response.statusText} (Status: ${error.response.status})`);
      } else if (error.request) {
        const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';
        if (isProduction) {
          setError(
            "❌ Cannot connect to backend API. " +
            "Please ensure:\n" +
            "1. Backend is deployed and accessible\n" +
            "2. VITE_API_URL is set in Vercel environment variables\n" +
            "3. CORS is enabled on the backend\n" +
            "4. Backend URL is correct"
          );
        } else {
          setError("Cannot connect to server. Make sure the backend is running on port 5000.");
        }
      } else {
        setError("Failed to fetch prediction: " + error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCheckDisease = async () => {
    if (!predictedDisease) return;

    setLoading(true);
    try {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:5000";
      const response = await axios.post(`${apiUrl}/check_disease`, {
        disease_name: predictedDisease.predicted_disease,
      }, {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });
      setDiseaseData(response.data);
      setShowDiseaseModal(true);
    } catch (error) {
      setError("Failed to fetch disease details");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const closeDiseaseModal = () => {
    setShowDiseaseModal(false);
    setDiseaseData(null);
  };

  // Back button functionality
  const goBack = () => {
    window.history.back();
  };

  return (
    <div>
      {/* Navbar with back button */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <button
            className="btn btn-light"
            onClick={goBack}
            style={{ marginLeft: "-15px" }}
          >
            &#8592; Back
          </button>
          <div className="logo">
            <img src="/img/logo1.png" alt="Logo" />
          </div>
          <a className="navbar-brand" href="#">
            Health Center
          </a>
        </div>
      </nav>

      {/* Main Content */}
      <div className="medical-page-container">
        <div className="medical-header">
          <h1 className="medical-title">
            <span className="medical-icon">🏥</span>
            AI-Powered Medical Disease Prediction
          </h1>
          <p className="medical-subtitle">Enter your symptoms to get an AI-powered diagnosis and treatment recommendations</p>
        </div>

        <div className="container my-4 mt-4">
        <form action="/predict" method="post">
          <div className="form-group">
            <label htmlFor="symptoms">Select Symptoms:</label>
            <input
              type="text"
              className="form-control"
              id="symptoms"
              name="symptoms"
              placeholder="Type symptoms such as itching, sleeping, aching etc."
              value={transcription}
              onChange={(e) => setTranscription(e.target.value)}
            />
          </div>
          <button
            type="button"
            id="startSpeechRecognition"
            className="btn btn-primary"
            onClick={startSpeechRecognition}
          >
            Start Speech Recognition
          </button>
          <div id="transcription">{transcription}</div>
          <button 
            type="button" 
            className="btn btn-danger btn-lg" 
            onClick={handlePrediction}
            disabled={loading}
          >
            {loading ? "Predicting..." : "Predict"}
          </button>
        </form>

        {/* Display Prediction Results */}
        {predictedDisease && (
          <div className="prediction-results">
            <div className="result-card">
              <h3 className="result-title">
                <span className="result-icon">🎯</span>
                Predicted Disease: {predictedDisease.predicted_disease}
              </h3>
              <div className="result-content">
                <div className="result-section">
                  <h4>📋 Description</h4>
                  <p>{predictedDisease.description}</p>
                </div>
                <div className="result-section">
                  <h4>⚠️ Precautions</h4>
                  <ul>
                    {predictedDisease.precautions && predictedDisease.precautions.map((precaution, index) => (
                      <li key={index}>{precaution}</li>
                    ))}
                  </ul>
                </div>
                <div className="result-section">
                  <h4>💊 Medications</h4>
                  <ul>
                    {predictedDisease.medications && predictedDisease.medications.map((medication, index) => (
                      <li key={index}>{medication}</li>
                    ))}
                  </ul>
                </div>
                <div className="result-section">
                  <h4>🥗 Diet Recommendations</h4>
                  <ul>
                    {predictedDisease.diet && predictedDisease.diet.map((diet, index) => (
                      <li key={index}>{diet}</li>
                    ))}
                  </ul>
                </div>
                <div className="result-section">
                  <h4>💪 Workout Recommendations</h4>
                  <ul>
                    {predictedDisease.workout && predictedDisease.workout.map((workout, index) => (
                      <li key={index}>{workout}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Check Disease Button */}
              <div className="check-disease-btn-container">
                <button
                  type="button"
                  className="btn btn-info btn-lg check-disease-btn"
                  onClick={handleCheckDisease}
                  disabled={loading}
                >
                  {loading ? "Loading..." : "🔍 Check Disease Details"}
                </button>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            <div className="error-content">
              {typeof error === 'string' ? (
                <pre style={{whiteSpace: 'pre-wrap', fontFamily: 'inherit'}}>{error}</pre>
              ) : (
                error
              )}
            </div>
          </div>
        )}
      </div>

      {/* Disease Details Modal */}
      {showDiseaseModal && diseaseData && (
        <div className="modal-overlay" onClick={closeDiseaseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>🏥 Disease Details: {diseaseData.disease_name}</h2>
              <button className="modal-close" onClick={closeDiseaseModal}>
                ✕
              </button>
            </div>
            <div className="modal-body">
              <div className="disease-info">
                <h4>📊 All Possible Symptoms ({diseaseData.symptom_count})</h4>
                <div className="symptoms-table-container">
                  <table className="symptoms-table">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Symptom</th>
                      </tr>
                    </thead>
                    <tbody>
                      {diseaseData.all_symptoms.map((symptom, index) => (
                        <tr key={index}>
                          <td>{index + 1}</td>
                          <td>{symptom}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-primary" onClick={closeDiseaseModal}>
                OK, Got it!
              </button>
            </div>
          </div>
        </div>
      )}
      </div>
    </div>
  );
};

export default Logo1;









