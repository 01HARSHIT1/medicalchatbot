import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Logo2 = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);

  const startImageRecognition = () => {
    setError(null);
    
    // Check if we're in production
    const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';
    const imageUrl = import.meta.env.VITE_IMAGE_URL || "http://localhost:8501";
    
    // Check if URL is configured in production
    if (isProduction && !import.meta.env.VITE_IMAGE_URL) {
      setError(
        <div style={{textAlign: 'left', lineHeight: '1.8'}}>
          <h4 style={{color: '#ff6b6b', marginBottom: '15px'}}>🔧 Image Recognition Service Configuration Required</h4>
          <p style={{marginBottom: '10px'}}><strong>Quick Setup:</strong></p>
          <ol style={{marginLeft: '20px', marginBottom: '15px'}}>
            <li>Deploy Streamlit app to <a href="https://share.streamlit.io" target="_blank" rel="noopener noreferrer" style={{color: '#4dabf7'}}>Streamlit Cloud</a> (free) or <a href="https://railway.app" target="_blank" rel="noopener noreferrer" style={{color: '#4dabf7'}}>Railway</a></li>
            <li>Set <code style={{background: '#f1f3f5', padding: '2px 6px', borderRadius: '3px'}}>VITE_IMAGE_URL</code> in Vercel Settings → Environment Variables</li>
            <li>Redeploy your Vercel app</li>
          </ol>
          <p style={{marginTop: '15px', fontSize: '0.9em', color: '#868e96'}}>
            📖 See deployment guide in repository for detailed instructions
          </p>
        </div>
      );
      return;
    }
    
    // Try to open the URL
    try {
      const newWindow = window.open(imageUrl, "_blank");
      if (!newWindow || newWindow.closed || typeof newWindow.closed === 'undefined') {
        setError(
          "❌ Could not open Image Recognition app. " +
          "Please check:\n" +
          "1. The service is deployed and accessible\n" +
          "2. VITE_IMAGE_URL is set correctly in Vercel\n" +
          "3. Pop-up blockers are disabled"
        );
      }
    } catch (err) {
      setError("Error opening Image Recognition: " + err.message);
    }
  };

  return (
    <div className="container text-center mt-5">
      <h1>🖼️ Image Recognition & Captioning</h1>
      <p>Upload an image and get AI-generated captions with text-to-speech</p>
      <div className="mt-4">
        <button 
          className="btn btn-primary btn-lg" 
          onClick={startImageRecognition}
          style={{ fontSize: '1.2rem', padding: '15px 30px' }}
        >
          🚀 Start Image Recognition Server
        </button>
      </div>
      
      {error && (
        <div className="mt-4 alert alert-danger" style={{ whiteSpace: 'pre-line', textAlign: 'left' }}>
          {error}
        </div>
      )}
      
      <div className="mt-4">
        <button className="btn btn-secondary" onClick={() => navigate("/")}>
          ← Go Back
        </button>
      </div>
      <div className="mt-4 alert alert-info">
        <p><strong>Local Development:</strong> Make sure the Streamlit server is running on port 8501.</p>
        <p><strong>Production:</strong> Set VITE_IMAGE_URL in Vercel environment variables with your deployed Streamlit URL.</p>
      </div>
    </div>
  );
};

export default Logo2;
