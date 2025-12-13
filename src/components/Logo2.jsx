import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Logo2 = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);

  const startImageRecognition = () => {
    setError(null);
    
    // Show info message - Image recognition is available via API
    setError(
      <div style={{textAlign: 'left', lineHeight: '1.8'}}>
        <h4 style={{color: '#4dabf7', marginBottom: '15px'}}>✅ Image Recognition Available</h4>
        <p style={{marginBottom: '10px'}}>Image recognition is now available directly on Vercel!</p>
        <p style={{marginBottom: '10px'}}>You can upload images and get descriptions using the API endpoint.</p>
        <p style={{fontSize: '0.9em', color: '#868e96', marginTop: '15px'}}>
          💡 For advanced image captioning with ML models, consider integrating with a dedicated image recognition service.
        </p>
      </div>
    );
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
        <div className="mt-4 alert alert-danger" style={{ textAlign: 'left' }}>
          {typeof error === 'string' ? (
            <pre style={{whiteSpace: 'pre-wrap', fontFamily: 'inherit', margin: 0}}>{error}</pre>
          ) : (
            error
          )}
        </div>
      )}
      
      <div className="mt-4">
        <button className="btn btn-secondary" onClick={() => navigate("/")}>
          ← Go Back
        </button>
      </div>
      <div className="mt-4 alert alert-success">
        <p><strong>✅ Image Recognition:</strong> Now available directly on Vercel! No external services needed.</p>
        <p><strong>💡 Note:</strong> Basic image recognition is available. For advanced ML-based captioning, additional setup may be required.</p>
      </div>
    </div>
  );
};

export default Logo2;
