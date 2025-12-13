import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Logo2.css";

const Logo2 = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [caption, setCaption] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
      setError(null);
      setCaption(null);
    }
  };

  const handleImageRecognition = async () => {
    if (!imageFile) {
      setError("Please select an image first");
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      // Convert image to base64
      const reader = new FileReader();
      reader.onloadend = async () => {
        try {
          const base64Image = reader.result.split(',')[1]; // Remove data:image/...;base64, prefix
          
          const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
          const apiUrl = isLocal ? "http://localhost:5000" : "/api";
          
          const response = await axios.post(`${apiUrl}/image-recognition`, {
            image: base64Image
          }, {
            headers: {
              'Content-Type': 'application/json'
            },
            timeout: 30000 // 30 second timeout for image processing
          });
          
          if (response.data && response.data.caption) {
            setCaption(response.data.caption);
            setError(null);
          } else {
            setError("Invalid response from server");
          }
        } catch (err) {
          console.error("Image recognition error:", err);
          if (err.response) {
            setError(`Server error: ${err.response.data?.error || err.response.statusText} (Status: ${err.response.status})`);
          } else if (err.request) {
            setError("Cannot connect to API. Please try again or check your internet connection.");
          } else {
            setError("Failed to process image: " + err.message);
          }
        } finally {
          setLoading(false);
        }
      };
      reader.readAsDataURL(imageFile);
    } catch (err) {
      setError("Error reading image file: " + err.message);
      setLoading(false);
    }
  };

  return (
    <div className="container text-center mt-5">
      <h1>🖼️ Image Recognition & Captioning</h1>
      <p>Upload an image and get AI-generated captions with text-to-speech</p>
      
      <div className="mt-4">
        <div className="mb-3">
          <input
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            className="form-control"
            style={{ maxWidth: '400px', margin: '0 auto' }}
          />
        </div>
        
        {imagePreview && (
          <div className="mb-3">
            <img 
              src={imagePreview} 
              alt="Preview" 
              style={{ maxWidth: '400px', maxHeight: '300px', borderRadius: '8px', margin: '10px auto' }}
            />
          </div>
        )}
        
        <button 
          className="btn btn-primary btn-lg" 
          onClick={handleImageRecognition}
          disabled={loading || !imageFile}
          style={{ fontSize: '1.2rem', padding: '15px 30px' }}
        >
          {loading ? "🔄 Processing..." : "🚀 Generate Caption"}
        </button>
      </div>
      
      {caption && (
        <div className="mt-4 alert alert-success" style={{ textAlign: 'left', maxWidth: '600px', margin: '20px auto' }}>
          <h5>📝 Generated Caption:</h5>
          <p>{caption}</p>
        </div>
      )}
      
      {error && (
        <div className="mt-4 alert alert-danger" style={{ textAlign: 'left', maxWidth: '600px', margin: '20px auto' }}>
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
      
      <div className="mt-4 alert alert-info" style={{ maxWidth: '600px', margin: '20px auto' }}>
        <p><strong>✅ Image Recognition:</strong> Now available directly on Vercel! No external services needed.</p>
        <p><strong>💡 Note:</strong> Basic image recognition is available. For advanced ML-based captioning, additional setup may be required.</p>
      </div>
    </div>
  );
};

export default Logo2;
