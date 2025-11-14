# Texas Hold'em AI Battle Simulator

## Overview
A full-stack Texas Hold'em Poker game featuring AI opponents, a modern React UI, and a robust backend engine. Play against built-in AI strategies, simulate hands, and enjoy a complete poker experience.

## Why I Wrote This Project
I created this project to:
- Learn and experiment with AI strategies in a real-world game setting
- Build a fun, interactive poker platform for friends and developers
- Explore full-stack development with Python (FastAPI) and React (TypeScript)
- Challenge myself to implement a complete poker engine and beautiful UI

## Features
- Complete No-Limit Hold'em engine (2-9 players)
- Multiple AI strategies (Aggressive, Conservative, Random)
- Modern, animated poker table UI
- Real-time game state updates
- REST API with Swagger docs
- Easy setup scripts for quick start

## Prerequisites
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd Texas-Holdem-AI-Battle-Simulator
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```
API will be available at: http://localhost:8000

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend will be available at: http://localhost:3000

### 4. One-Click Start (Windows)
Double-click `START_POKER_GAME.bat` to launch both backend and frontend automatically.

## Usage
- Open your browser to http://localhost:3000
- Create a game, choose AI opponents, and start playing!
- For API usage, see http://localhost:8000/docs

## Excluded Files
**No LLM API keys or configs are included in this repository.**
- Do NOT commit any files containing API keys, secrets, or proprietary LLM configurations.
- Example config files are provided for reference only.

## Credits
Created by [Your Name].

## License
MIT (or your preferred license)
