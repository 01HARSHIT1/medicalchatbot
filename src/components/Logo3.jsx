import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Logo3.css";

const Logo3 = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [chatId] = useState(1);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim()) {
      return;
    }

    const userMessage = inputMessage.trim();
    setInputMessage("");
    setError(null);
    setLoading(true);

    // Add user message to chat
    const newUserMessage = { text: `User: ${userMessage}`, sender: 'user' };
    setMessages(prev => [...prev, newUserMessage]);

    try {
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const apiUrl = isLocal ? "http://localhost:5002" : "/api";
      
      const response = await axios.post(`${apiUrl}/chatbot`, {
        input: userMessage,
        chat_id: chatId
      }, {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 30000 // 30 second timeout
      });
      
      if (response.data && response.data.response) {
        const aiMessage = { text: `AI: ${response.data.response}`, sender: 'ai' };
        setMessages(prev => [...prev, aiMessage]);
        setError(null);
      } else {
        setError("Invalid response from server");
      }
    } catch (err) {
      console.error("Chatbot error:", err);
      const errorMessage = { 
        text: `AI: Sorry, I encountered an error. Please try again.`, 
        sender: 'ai',
        error: true 
      };
      setMessages(prev => [...prev, errorMessage]);
      
      if (err.response) {
        setError(`Server error: ${err.response.data?.error || err.response.statusText}`);
      } else if (err.request) {
        setError("Cannot connect to API. Please try again or check your internet connection.");
      } else {
        setError("Failed to send message: " + err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className="container mt-4" style={{ maxWidth: '800px' }}>
      <div className="text-center mb-4">
        <h1>💬 AI Chatbot</h1>
        <p>Chat with our AI assistant</p>
      </div>

      {/* Chat Container */}
      <div 
        className="border rounded p-3 mb-3" 
        style={{ 
          height: '500px', 
          overflowY: 'auto', 
          backgroundColor: '#f8f9fa',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        {messages.length === 0 ? (
          <div className="text-center text-muted mt-5">
            <p>Start a conversation by typing a message below!</p>
            <p className="small">Try: "Hello" or "What can you help me with?"</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`mb-3 d-flex ${msg.sender === 'user' ? 'justify-content-end' : 'justify-content-start'}`}
            >
              <div
                className={`p-3 rounded ${
                  msg.sender === 'user' 
                    ? 'bg-primary text-white' 
                    : msg.error 
                    ? 'bg-danger text-white'
                    : 'bg-light'
                }`}
                style={{ maxWidth: '70%', wordWrap: 'break-word' }}
              >
                <strong>{msg.sender === 'user' ? 'You' : 'AI'}:</strong> {msg.text.replace(/^(User|AI):\s*/, '')}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="text-center text-muted">
            <small>AI is typing...</small>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Type your message..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
        />
        <button
          className="btn btn-success"
          onClick={sendMessage}
          disabled={loading || !inputMessage.trim()}
        >
          {loading ? "⏳" : "📤 Send"}
        </button>
        <button
          className="btn btn-secondary"
          onClick={clearChat}
          disabled={loading}
        >
          🗑️ Clear
        </button>
      </div>

      {error && (
        <div className="alert alert-danger" style={{ textAlign: 'left' }}>
          {typeof error === 'string' ? (
            <pre style={{whiteSpace: 'pre-wrap', fontFamily: 'inherit', margin: 0}}>{error}</pre>
          ) : (
            error
          )}
        </div>
      )}

      <div className="text-center mb-3">
        <button className="btn btn-secondary" onClick={() => navigate("/")}>
          ← Go Back
        </button>
      </div>

      <div className="alert alert-success" style={{ maxWidth: '600px', margin: '20px auto' }}>
        <p><strong>✅ Chatbot:</strong> Now available directly on Vercel! No external services needed.</p>
        <p><strong>💡 Note:</strong> Basic chatbot is available. For advanced AI features, you can enhance the API endpoint.</p>
      </div>
    </div>
  );
};

export default Logo3;
