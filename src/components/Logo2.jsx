import React from "react";
import { useNavigate } from "react-router-dom";

const Logo2 = () => {
  const navigate = useNavigate();

  const startImageRecognition = () => {
    // Open the image recognition app in a new window
    const imageUrl = import.meta.env.VITE_IMAGE_URL || "http://localhost:8501";
    window.open(imageUrl, "_blank");
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
      <div className="mt-4">
        <button className="btn btn-secondary" onClick={() => navigate("/")}>
          ← Go Back
        </button>
      </div>
      <div className="mt-4 alert alert-info">
        <p>This will open the Image Recognition app in a new window.</p>
        <p>Make sure the Streamlit server is running on port 8501.</p>
      </div>
    </div>
  );
};

export default Logo2;
