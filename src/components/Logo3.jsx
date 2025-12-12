import React from "react";
import { useNavigate } from "react-router-dom";

const Logo3 = () => {
  const navigate = useNavigate();

  const startChatbot = () => {
    // Open the chatbot app in a new window
    const chatbotUrl = import.meta.env.VITE_CHATBOT_URL || "http://localhost:5002";
    window.open(chatbotUrl, "_blank");
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
      <div className="mt-4">
        <button className="btn btn-secondary" onClick={() => navigate("/")}>
          ← Go Back
        </button>
      </div>
      <div className="mt-4 alert alert-info">
        <p>This will open the AI Chatbot in a new window.</p>
        <p>Make sure the Flask chatbot server is running on port 5002.</p>
      </div>
    </div>
  );
};

export default Logo3;
