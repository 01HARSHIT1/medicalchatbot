# 🏠 Local Deployment Guide

Deploy and run everything on your own machine or server - **no external services needed!**

## 🚀 Quick Start

### Windows:
```bash
run-local.bat
```

### Linux/Mac:
```bash
chmod +x run-local.sh
./run-local.sh
```

## 📋 Manual Setup

### Step 1: Install Dependencies

**Python Backend:**
```bash
cd backend-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Node.js Frontend:**
```bash
npm install
```

### Step 2: Start Services

**Terminal 1 - Backend:**
```bash
cd backend-api
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```
Backend runs on: http://localhost:5000

**Terminal 2 - Frontend:**
```bash
npm run dev
```
Frontend runs on: http://localhost:5173

## 🐳 Docker Deployment (Recommended)

### Option 1: Docker Compose (Easiest)

```bash
docker-compose up
```

This starts both frontend and backend automatically!

### Option 2: Individual Containers

**Build and run backend:**
```bash
cd backend-api
docker build -t medical-backend .
docker run -p 5000:5000 medical-backend
```

**Build and run frontend:**
```bash
docker build -f Dockerfile.frontend -t medical-frontend .
docker run -p 3000:3000 medical-frontend
```

## 🌐 Self-Hosted Server Deployment

### Using PM2 (Process Manager)

**Install PM2:**
```bash
npm install -g pm2
```

**Start Backend:**
```bash
cd backend-api
source venv/bin/activate
pm2 start main.py --name "medical-backend" --interpreter python
```

**Start Frontend:**
```bash
npm run build
pm2 serve dist 3000 --name "medical-frontend" --spa
```

**Save PM2 configuration:**
```bash
pm2 save
pm2 startup
```

### Using Systemd (Linux)

**Create backend service:**
```bash
sudo nano /etc/systemd/system/medical-backend.service
```

```ini
[Unit]
Description=Medical Prediction Backend
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/backend-api
Environment="PATH=/path/to/backend-api/venv/bin"
ExecStart=/path/to/backend-api/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable medical-backend
sudo systemctl start medical-backend
```

## 🔧 Configuration

### Update Frontend API URL

Edit `src/components/Logo1.jsx`:
```javascript
const apiUrl = "http://localhost:5000";  // For local
// or
const apiUrl = "http://your-server-ip:5000";  // For remote server
```

### Production Build

**Frontend:**
```bash
npm run build
# Serves static files from dist/ folder
```

**Backend:**
```bash
cd backend-api
source venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## 🌍 Access from Other Devices

### On Local Network:

1. Find your local IP:
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig` or `ip addr`

2. Update frontend to use your IP:
   ```javascript
   const apiUrl = "http://YOUR_LOCAL_IP:5000";
   ```

3. Access from other devices:
   - Frontend: `http://YOUR_LOCAL_IP:5173`
   - Backend: `http://YOUR_LOCAL_IP:5000`

### Make Publicly Accessible:

Use **ngrok** or **localtunnel**:
```bash
# Install ngrok
# Then run:
ngrok http 5000  # For backend
ngrok http 5173  # For frontend
```

## ✅ Benefits of Local Deployment

- ✅ **No external dependencies**
- ✅ **Full control**
- ✅ **No usage limits**
- ✅ **Works offline**
- ✅ **Free (except server costs if self-hosting)**
- ✅ **Privacy - data stays on your machine**

## 🆘 Troubleshooting

**Port already in use?**
- Change ports in `main.py` (backend) and `vite.config.js` (frontend)

**Python dependencies fail?**
- Make sure you're using Python 3.8+
- Try: `pip install --upgrade pip`

**Frontend can't connect to backend?**
- Check CORS settings in `backend-api/main.py`
- Verify backend is running on correct port
- Check firewall settings

---

**You're all set! Run everything locally without any external services!** 🎉

