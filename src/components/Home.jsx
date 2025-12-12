import React from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <header className="home-header">
        <div className="header-content">
          <h1 className="main-title">
            <span className="title-icon">🤖</span>
            AI-Powered Healthcare Platform
          </h1>
          <p className="subtitle">Advanced Machine Learning Solutions for Medical Diagnosis, Image Recognition & AI Chatbot</p>
        </div>
      </header>

      <div className="services-grid">
        <div
          className="service-card medical-card"
          onClick={() => navigate("/logo1")}
        >
          <div className="card-icon">🏥</div>
          <div className="card-content">
            <h3>Medical Disease Prediction</h3>
            <p>AI-powered symptom analysis for accurate disease diagnosis</p>
            <ul className="feature-list">
              <li>✓ Symptom-based prediction</li>
              <li>✓ Treatment recommendations</li>
              <li>✓ Diet & workout plans</li>
            </ul>
          </div>
          <div className="card-footer">
            <span className="card-arrow">→</span>
          </div>
        </div>

        <div
          className="service-card image-card"
          onClick={() => navigate("/logo2")}
        >
          <div className="card-icon">🖼️</div>
          <div className="card-content">
            <h3>Image Recognition</h3>
            <p>Advanced AI image captioning with text-to-speech</p>
            <ul className="feature-list">
              <li>✓ VGG16 + LSTM model</li>
              <li>✓ Automatic captioning</li>
              <li>✓ Audio output</li>
            </ul>
          </div>
          <div className="card-footer">
            <span className="card-arrow">→</span>
          </div>
        </div>

        <div
          className="service-card chatbot-card"
          onClick={() => navigate("/logo3")}
        >
          <div className="card-icon">💬</div>
          <div className="card-content">
            <h3>AI Chatbot</h3>
            <p>Intelligent conversation powered by Google Gemini</p>
            <ul className="feature-list">
              <li>✓ Natural language processing</li>
              <li>✓ Context-aware responses</li>
              <li>✓ Multi-turn conversations</li>
            </ul>
          </div>
          <div className="card-footer">
            <span className="card-arrow">→</span>
          </div>
        </div>
      </div>

      <footer className="home-footer">
        <p>Built with React, Flask, Streamlit & Machine Learning</p>
      </footer>
    </div>
  );
};

export default Home;

