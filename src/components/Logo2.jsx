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
        "⚠️ Image Recognition service not configured. " +
        "Please set VITE_IMAGE_URL environment variable in Vercel settings. " +
        "The Streamlit app needs to be deployed separately (Streamlit Cloud, Railway, or Render)."
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
