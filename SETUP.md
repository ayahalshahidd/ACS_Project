# Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn
- Git

## Initial Setup

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd Project
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env if needed

# Run the server
# HTTP mode (unencrypted):
USE_HTTP=true python main.py
# OR HTTPS mode (misconfigured certificate):
python main.py
```

Backend will run at:
- **HTTP:** `http://localhost:8000` (when `USE_HTTP=true`)
- **HTTPS:** `https://localhost:8000` (default, misconfigured certificate)

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
# HTTP mode (matches HTTP backend):
npm run dev:http
# OR HTTPS mode (matches HTTPS backend):
npm run dev:https
# OR default (uses USE_HTTP env var):
npm run dev
```

Frontend will run at `http://localhost:3000` and automatically proxy to backend.

**See `LAUNCH_OPTIONS.md` for detailed HTTP/HTTPS configuration.**

## GitHub Repository Setup

### 1. Initialize Git (if not already done)

```bash
git init
```

### 2. Create .gitignore

Already created - includes Python, Node, and environment files.

### 3. Initial Commit

```bash
git add .
git commit -m "Initial commit: Backend and frontend infrastructure"
```

### 4. Create GitHub Repository

1. Go to GitHub and create a new repository
2. Don't initialize with README (we already have one)

### 5. Connect and Push

```bash
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

### 6. Create Baseline Tag

```bash
git tag -a baseline-unpatched -m "Baseline unpatched version for Stage 1"
git push origin baseline-unpatched
```

## Project Structure

```
Project/
├── backend/           # FastAPI backend
│   ├── main.py
│   ├── models/
│   ├── routes/
│   └── requirements.txt
├── frontend/          # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── docs/              # Documentation (to be created)
├── recon/            # Reconnaissance artifacts (to be created)
└── README.md
```

## Next Steps

1. Complete Stage 1: Reconnaissance & Threat Modeling
2. Test the application
3. Document vulnerabilities
4. Create threat model

## Troubleshooting

### Backend Issues

- **Port already in use**: Change port in `main.py` or kill process using port 8000
- **Database errors**: Make sure SQLite file permissions are correct
- **Import errors**: Activate virtual environment and reinstall dependencies

### Frontend Issues

- **Port already in use**: Change port in `vite.config.js`
- **API connection errors**: Check backend is running and CORS is configured
- **Module not found**: Run `npm install` again

