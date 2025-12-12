import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Logo3 = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);

  const startChatbot = () => {
    setError(null);
    
    // Check if we're in production
    const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';
    const chatbotUrl = import.meta.env.VITE_CHATBOT_URL || "http://localhost:5002";
    
    // Check if URL is configured in production
    if (isProduction && !import.meta.env.VITE_CHATBOT_URL) {
      setError(
        "🔧 Chatbot Service Configuration Required\n\n" +
        "To use this feature, please:\n" +
        "1. Deploy chatbot to Railway (railway.app) or Render (render.com)\n" +
        "2. Set VITE_CHATBOT_URL in Vercel Settings → Environment Variables\n" +
        "3. Redeploy your Vercel app\n\n" +
        "See BACKEND_SETUP.md in the repository for detailed instructions."
      );
      return;
    }
    
    // Try to open the URL
    try {
      const newWindow = window.open(chatbotUrl, "_blank");
      if (!newWindow || newWindow.closed || typeof newWindow.closed === 'undefined') {
        setError(
          "❌ Could not open Chatbot. " +
          "Please check:\n" +
          "1. The service is deployed and accessible\n" +
          "2. VITE_CHATBOT_URL is set correctly in Vercel\n" +
          "3. Pop-up blockers are disabled"
        );
      }
    } catch (err) {
      setError("Error opening Chatbot: " + err.message);
    }
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
        <p><strong>Local Development:</strong> Make sure the Flask chatbot server is running on port 5002.</p>
        <p><strong>Production:</strong> Set VITE_CHATBOT_URL in Vercel environment variables with your deployed chatbot URL.</p>
      </div>
    </div>
  );
};

export default Logo3;
