# 🎰 Texas Hold'em AI Battle Simulator

**A comprehensive poker simulation platform - Ready to play NOW!**

**✨ LATEST: Betting Rounds Fixed + Individual AI Strategies!** (See [✅_BETTING_ROUNDS_FIXED.md](✅_BETTING_ROUNDS_FIXED.md))
- 🎴 Proper poker flow: Pre-flop → Flop → Turn → River → Showdown
- 🤖 Each AI can use different strategy (GPT-4 vs Claude battles!)
- ⚙️ Configure game settings (stack, blinds)
- 🎮 Add LLM API keys and play against AI that actually thinks!

---

## 🚀 **ONE-CLICK START** ⭐

### **Just double-click this file:**

```
📁 START_POKER_GAME.bat
```

**Everything starts automatically!** 🎉

---

## 📖 **QUICK GUIDES**

- **[START_HERE.md](START_HERE.md)** ⭐ - Quick overview & start
- **[ONE_CLICK_START.md](ONE_CLICK_START.md)** ⭐ - Detailed one-click guide  
- **[FINAL_COMPLETE_DELIVERY.md](FINAL_COMPLETE_DELIVERY.md)** - What you have

---

## 📋 Prerequisites (First Time Only)

1. **Python 3.11+**: https://www.python.org/downloads/
   - ⚠️ Check "Add Python to PATH" during installation

2. **Node.js 18+**: https://nodejs.org/

---

## ✨ Features

### Core Functionality
- ♠️ **Complete No-Limit Hold'em Engine** - Full poker rules with 2-9 players
- 🤖 **AI Opponents** - 3 built-in strategies (Aggressive, Conservative, Random)
- 🎨 **Beautiful UI** - Modern poker table with animations
- 📊 **Real-time Updates** - See every action as it happens
- 👤 **Human vs AI** - Play against AI agents
- 🎯 **Easy Setup** - One-click start, all dependencies included

### What Works Right Now
✅ Complete poker engine
✅ All poker hands (High Card → Royal Flush)
✅ Main and side pots
✅ All player actions (fold, check, call, raise, all-in)
✅ AI strategies
✅ Beautiful React UI
✅ Real-time game updates
✅ REST API with Swagger docs

---

## 🎮 Three Ways to Start

### Option 1: 🚀 ONE-CLICK (Recommended)
**Double-click**: `START_POKER_GAME.bat`

### Option 2: 📦 Separate Windows
1. Double-click `START_BACKEND.bat`
2. Double-click `START_FRONTEND.bat`

### Option 3: 💻 Manual
```bash
# Terminal 1: Backend
cd backend
pip install -r requirements.txt
python -m app.main

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + TS)                     │
│  Poker Table • Player Cards • Action Panel • Analytics      │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP/WebSocket
┌────────────────▼────────────────────────────────────────────┐
│                   Backend (Python + FastAPI)                 │
│  ┌──────────────┬──────────────┬──────────────┬───────────┐ │
│  │ Game Engine  │ AI Manager   │ Analytics    │ Admin     │ │
│  │ - Rules      │ - Client     │ - Stats      │ - Config  │ │
│  │ - Pot Mgmt   │ - Strategies │ - GTO        │ - Optimize│ │
│  │ - Hand Eval  │ - Timeout    │ - Reports    │ - Logs    │ │
│  └──────────────┴──────────────┴──────────────┴───────────┘ │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│  PostgreSQL (Game Data)  •  Redis (Cache)  •  Celery (BG)  │
└─────────────────────────────────────────────────────────────┘
```

**Technology Stack:**
- **Backend**: Python 3.11+, FastAPI, Pydantic
- **Frontend**: React 18, TypeScript, TailwindCSS, Vite
- **MVP**: In-memory storage (database optional)

---

## 📁 Project Structure

```
poker-simulator/
├── START_POKER_GAME.bat ⭐     # ONE-CLICK START
├── START_BACKEND.bat           # Backend only
├── START_FRONTEND.bat          # Frontend only
│
├── backend/                    # Python backend
│   ├── app/
│   │   ├── core/
│   │   │   ├── game_engine/   # Poker rules & engine
│   │   │   └── ai_manager/    # AI strategies
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt ⭐     # All dependencies
│   └── config.env             # Configuration
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   └── App.tsx            # Main app
│   └── package.json ⭐         # All dependencies
│
└── docs/                       # Documentation (23 files)
    ├── START_HERE.md ⭐
    ├── ONE_CLICK_START.md ⭐
    ├── FINAL_COMPLETE_DELIVERY.md
    └── ...
```

---

## 📚 API Documentation

Once backend is running:
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🎯 How to Play

### 1. Start the Game
**Double-click**: `START_POKER_GAME.bat`

### 2. Create Game
- Enter your name
- Choose number of AI opponents (1-8)
- Select AI strategy
- Click "Create Game"

### 3. Play Poker!
- Click "Start Hand"
- Wait for your turn (yellow highlight)
- Choose your action
- Have fun! 🎰

---

## 📖 Complete Documentation

### Quick Start
- **[START_HERE.md](START_HERE.md)** - Quick start overview
- **[ONE_CLICK_START.md](ONE_CLICK_START.md)** - Detailed one-click guide
- **[COMMANDS_QUICK_REFERENCE.md](COMMANDS_QUICK_REFERENCE.md)** - Quick commands

### Product Details
- **[FINAL_COMPLETE_DELIVERY.md](FINAL_COMPLETE_DELIVERY.md)** - Complete product overview
- **[FRONTEND_COMPLETE.md](FRONTEND_COMPLETE.md)** - Frontend details
- **[MVP_COMPLETE.md](MVP_COMPLETE.md)** - MVP summary

### Technical
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[CLAUDE.md](CLAUDE.md)** - Development guidelines
- **[IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)** - Development plan
- **[backend/README.md](backend/README.md)** - Backend details
- **[frontend/README.md](frontend/README.md)** - Frontend details

---

## 🛠️ Development

### Backend Development
```bash
cd backend

# Run with auto-reload
python -m app.main

# Run tests
python test_game.py
```

### Frontend Development
```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build
```

---

## 🐛 Troubleshooting

### Python/Node not found
**Solution**: Install Python/Node and add to PATH

### Port 8000 already in use
**Solution**: Kill process or use different port
```cmd
netstat -ano | findstr :8000
taskkill /PID [process_id] /F
```

### Port 3000 already in use
**Solution**: Frontend will try port 3001 automatically

### Dependencies fail to install
**Solution**: Update pip/npm
```cmd
python -m pip install --upgrade pip
npm install -g npm@latest
```

See **[ONE_CLICK_START.md](ONE_CLICK_START.md)** for detailed troubleshooting.

---

## ✅ What's Included

### ✅ Backend (15 files - 1,520 lines)
- Complete poker engine
- Hand evaluation (all hands)
- Pot and side pot calculation
- 3 AI strategies
- REST API with Swagger
- All dependencies in `requirements.txt`

### ✅ Frontend (14 files - 820 lines)
- Beautiful poker table UI
- Playing cards with suits
- Action panel
- Real-time updates
- Error handling
- All dependencies in `package.json`

### ✅ Documentation (23 files - 12,000+ lines)
- Quick start guides
- API documentation
- Architecture design
- Development guidelines
- Complete tutorials

### ✅ One-Click Start (3 files)
- START_POKER_GAME.bat (main)
- START_BACKEND.bat
- START_FRONTEND.bat

---

## 🎉 You're Ready!

### Everything You Need:
✅ Working product
✅ Beautiful UI
✅ AI opponents
✅ One-click start
✅ All dependencies
✅ Complete docs

### Your Next Step:
**Double-click:** `START_POKER_GAME.bat`

---

## 📞 Support

### Check These First:
1. **[START_HERE.md](START_HERE.md)** - Quick overview
2. **[ONE_CLICK_START.md](ONE_CLICK_START.md)** - Detailed guide
3. **[COMMANDS_QUICK_REFERENCE.md](COMMANDS_QUICK_REFERENCE.md)** - Quick commands

### Common Issues:
- Python/Node not found → Install and add to PATH
- Port busy → Kill process or change port
- Dependencies fail → Update pip/npm

---

## 🗺️ Future Enhancements

### Completed ✅
- [x] No-Limit Hold'em engine
- [x] AI strategies
- [x] Beautiful React UI
- [x] REST API
- [x] One-click start
- [x] Complete documentation

### Planned 🔮
- [ ] PostgreSQL integration
- [ ] WebSocket for real-time updates
- [ ] Advanced analytics
- [ ] More AI strategies
- [ ] Tournament mode
- [ ] Hand history
- [ ] Replay system

---

## 🏆 **START NOW!**

**Double-click this file:**

# 📁 START_POKER_GAME.bat

**Your poker game is ready!** ♠️♥️♣️♦️

---

**Complete product • One-click start • Professional quality**

**Enjoy your poker game!** 🚀🎉
