import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Logo3 = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);

  const startChatbot = () => {
    setError(null);
    
    // Show info message - Chatbot is available via API
    setError(
      <div style={{textAlign: 'left', lineHeight: '1.8'}}>
        <h4 style={{color: '#4dabf7', marginBottom: '15px'}}>✅ Chatbot Available</h4>
        <p style={{marginBottom: '10px'}}>Chatbot is now available directly on Vercel!</p>
        <p style={{marginBottom: '10px'}}>You can interact with the chatbot using the API endpoint.</p>
        <p style={{fontSize: '0.9em', color: '#868e96', marginTop: '15px'}}>
          💡 For advanced AI features with OpenAI or Google Gemini, you can enhance the chatbot API endpoint.
        </p>
      </div>
    );
  };

  return (
    <div className="container text-center mt-5">
      <h1>💬 AI Chatbot (Google Gemini)</h1>
      <p>Chat with our AI assistant powered by Google Gemini</p>
      <div className="mt-4">
        <button 
          className="btn btn-success btn-lg" 
          onClick={startChatbot}
          style={{ fontSize: '1.2rem', padding: '15px 30px' }}
        >
          🚀 Start Chatbot Server
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
        <p><strong>✅ Chatbot:</strong> Now available directly on Vercel! No external services needed.</p>
        <p><strong>💡 Note:</strong> Basic chatbot is available. For advanced AI features, you can enhance the API endpoint.</p>
      </div>
    </div>
  );
};

export default Logo3;
