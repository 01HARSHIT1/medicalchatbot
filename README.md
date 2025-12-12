# 🤖 AI-Powered Healthcare Platform

A comprehensive healthcare platform featuring AI-powered medical disease prediction, image recognition, and an intelligent chatbot.

## 🌟 Features

### 🏥 Medical Disease Prediction
- AI-powered symptom analysis
- Accurate disease diagnosis
- Treatment recommendations
- Diet and workout plans
- Precautions and medications

### 🖼️ Image Recognition & Captioning
- Advanced VGG16 + LSTM model
- Automatic image captioning
- Text-to-speech output
- Support for JPG, PNG, JPEG formats

### 💬 AI Chatbot
- Powered by Google Gemini
- Natural language processing
- Context-aware responses
- Multi-turn conversations

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.7+
- Git

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ProjectAML
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API URLs
```

4. **Start the development server**
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## 📦 Running All Services

To run all services together (React frontend, Medical backend, Image recognition, Chatbot):

```bash
python runall.py
```

This will start:
- React Frontend: http://localhost:5173
- Medical Backend: http://localhost:5000
- Image Recognition: http://localhost:8501
- AI Chatbot: http://localhost:5002

## 🛠️ Tech Stack

### Frontend
- React 18
- Vite
- React Router
- Axios
- Bootstrap 5

### Backend
- Flask (Medical Prediction)
- Streamlit (Image Recognition)
- Google Gemini API (Chatbot)

### Machine Learning
- scikit-learn
- TensorFlow/Keras
- VGG16
- LSTM

## 📁 Project Structure

```
ProjectAML/
├── src/
│   ├── components/
│   │   ├── Home.jsx          # Main landing page
│   │   ├── Logo1.jsx         # Medical prediction
│   │   ├── Logo2.jsx         # Image recognition
│   │   └── Logo3.jsx         # Chatbot
│   ├── App.jsx
│   └── main.jsx
├── public/
├── package.json
└── README.md
```

## 🌐 Deployment

### Vercel Deployment

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
vercel
```

3. **Set environment variables in Vercel dashboard**
   - `VITE_API_URL`: Your backend API URL

### GitHub Deployment

1. **Initialize git repository**
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Add remote and push**
```bash
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:5000
```

For production, update with your deployed backend URL.

## 📝 API Endpoints

### Medical Prediction API

- **POST** `/predict`
  - Body: `{ "symptoms": ["symptom1", "symptom2"] }`
  - Returns: Disease prediction with recommendations

- **POST** `/check_disease`
  - Body: `{ "disease_name": "Disease Name" }`
  - Returns: All symptoms for the disease

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Built with ❤️ using React, Flask, and Machine Learning

## 🙏 Acknowledgments

- React team for the amazing framework
- Flask for the lightweight backend
- Google Gemini for AI capabilities
- TensorFlow for ML models
