# 🎰 Texas Hold'em AI Battle Simulator

<div align="center">

**A full-stack, production-ready poker simulation platform with AI opponents**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2+-61dafb.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Why I Built This](#why-i-built-this)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Project Structure](#project-structure)
- [Game Rules & Features](#game-rules--features)
- [AI Strategies](#ai-strategies)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

Texas Hold'em AI Battle Simulator is a comprehensive poker platform that combines a robust game engine with multiple AI strategies and a beautiful modern UI. Whether you want to practice poker, test AI strategies, or just have fun playing against computer opponents, this simulator has you covered.

**Key Highlights:**
- 🎮 Full No-Limit Texas Hold'em implementation
- 🤖 Multiple AI strategies (rule-based + LLM-powered) with full customization
- 🎨 Beautiful, responsive poker table UI with auto-advance spectating
- 🚀 One-click start for Windows
- 📊 Real-time game state updates with complete hand tracking
- 🔌 RESTful API with WebSocket support
- 🧪 Comprehensive test coverage
- ⚡ Smart betting logic following Texas Hold'em rules
- 🎭 Custom AI personalities with individual names and prompts

## 🆕 Latest Features (v2.0)

### AI Customization
- **Custom AI Names**: Give each AI opponent a unique nickname (e.g., "Phil Ivey Bot", "The Shark")
- **Individual Strategies**: Mix and match different AI strategies at the same table
- **Personality Prompts**: Define custom playing styles for LLM-powered AIs
- **Strategy Display**: See each AI's name and strategy on the table

### Improved Game Logic
- **Flexible Hand Evaluation**: Handles any card combination (5, 6, 7+ cards) correctly
- **Texas Hold'em Compliant Betting**: Minimum raise equals last raise amount (not just double)
- **Smart Betting Rounds**: Won't auto-advance until all players have acted
- **Accurate Profit/Loss**: Calculated from stack difference before/after hand

### Enhanced UX
- **Auto-Advance Mode**: Watch AI games progress at natural pace
- **Smart Action Panel**: Raise controls dynamically enable/disable based on valid actions
- **Complete Hand History**: See all actions, board cards, and stack changes
- **Hand Replay**: Review any previous hand with full details

---

## 💡 Why I Built This

I created this project to:

1. **Master Full-Stack Development**: Build a complete application from database to UI, using modern technologies like FastAPI, React, and TypeScript.

2. **Explore AI & Strategy**: Experiment with different poker strategies, from rule-based algorithms to LLM-powered decision making. Compare how GPT-4, Claude, DeepSeek, and other AI models play poker.

3. **Learn Game Theory**: Implement complex game logic including pot management, side pots, hand evaluation, and multi-phase betting rounds.

4. **Create a Learning Tool**: Provide a platform where developers can study poker algorithms, practice against AI, and understand game theory concepts in action.

5. **Have Fun**: Build something entertaining that combines programming, poker, and artificial intelligence.

---

## ✨ Features

### 🎲 Complete Poker Engine
- **Full No-Limit Hold'em** implementation (2-9 players)
- **All betting rounds**: Pre-flop, Flop, Turn, River, Showdown
- **Complex pot management**: Main pot and unlimited side pots
- **Accurate hand evaluation**: Handles any combination of 5+ cards (fixes AI comparison with 6-card scenarios)
- **All player actions**: Fold, Check, Call, Bet, Raise, All-In
- **Position-based gameplay**: Dealer button, Small Blind, Big Blind rotation
- **Texas Hold'em compliant betting**: Minimum raise must equal the last raise amount or big blind
- **Smart betting round logic**: Won't advance phases until all pending player actions complete

### 🤖 AI Opponents

**Built-in Rule-Based Strategies:**
- **Aggressive (LAG)**: Loose-aggressive play style, high VPIP/PFR
- **Conservative (TAG)**: Tight-aggressive play style, selective hands
- **Random**: Random valid actions for testing

**LLM-Powered Strategies** (requires API keys):
- **GPT-4o / GPT-4o-mini** (OpenAI)
- **Claude 3.5 Sonnet** (Anthropic)
- **DeepSeek Chat** (DeepSeek)
- **Gemini 2.5 Flash** (Google)
- **Grok Beta** (xAI)

**Full AI Customization:**
- **Custom names**: Give each AI a unique nickname (e.g., "Phil Bot", "Aggressive Alice")
- **Individual strategies**: Mix different AI strategies at the same table
- **Personality prompts**: Define how each AI should play with custom instructions
- **Strategy display**: AI names and strategies shown on table and in hand history

Each LLM agent makes contextual decisions based on:
- Current cards and position
- Community cards and pot odds
- Opponent betting patterns
- Stack sizes and pot size
- Custom personality prompts

### 🎨 Modern Frontend
- **Beautiful poker table UI** with green felt design
- **Real-time updates** with automatic state refresh
- **Responsive design** works on desktop and tablets
- **Smooth animations** for cards and chips
- **Comprehensive hand history panel** with complete action logs, board cards, and profit/loss
- **Advanced settings panel** for game configuration, LLM API keys, and AI customization
- **Watch mode** with auto-advance pacing for observing AI-only games
- **Smart action controls**: Raise/Bet buttons dynamically enable/disable based on valid actions
- **Hand replay**: Review any previous hand by hand number with full details

### 🔌 Robust Backend
- **FastAPI framework** with async/await support
- **RESTful API** with automatic Swagger documentation
- **Input validation** using Pydantic models
- **CORS enabled** for frontend integration
- **Error handling** with detailed error messages
- **Extensible architecture** for easy feature additions

### 📊 Advanced Features
- **Game state persistence** (in-memory for MVP)
- **Complete hand tracking**: Every action (fold, all-in, etc.) recorded with timestamps
- **Accurate profit/loss calculation**: Based on stack difference before/after each hand
- **Multiple concurrent games** support
- **Configurable blinds and stacks**
- **API key validation** for LLM providers
- **Health check endpoints**
- **Auto-advance mode**: AI actions progress at natural pace in watch mode or when player inactive
- **Betting round intelligence**: Won't auto-advance phases if players haven't acted yet

---

## 🛠 Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Core language |
| **FastAPI** | 0.104+ | Web framework |
| **Pydantic** | 2.5+ | Data validation |
| **Uvicorn** | 0.24+ | ASGI server |
| **httpx** | 0.25+ | Async HTTP client |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.2+ | UI framework |
| **TypeScript** | 5.0+ | Type safety |
| **Vite** | 5.0+ | Build tool |
| **TailwindCSS** | 3.3+ | Styling |
| **Axios** | 1.6+ | HTTP client |

### Development Tools
- **Poetry** - Python dependency management (optional)
- **ESLint** - JavaScript linting
- **Prettier** - Code formatting
- **Git** - Version control

---

## 🚀 Quick Start

### Windows (Recommended)

**Just double-click this file:**
```
START_POKER_GAME.bat
```

This will:
1. ✅ Install all Python dependencies
2. ✅ Install all Node.js dependencies
3. ✅ Start the backend server (port 8000)
4. ✅ Start the frontend dev server (port 3000)
5. ✅ Open your browser automatically

**That's it!** Your poker game will be running in ~30 seconds.

### Manual Start (All Platforms)

**Prerequisites:**
- Python 3.11 or higher
- Node.js 18 or higher

**Step 1: Backend**
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

**Step 2: Frontend** (in a new terminal)
```bash
cd frontend
npm install
npm run dev
```

**Step 3: Play**
- Open http://localhost:3000 in your browser
- Enter your name
- Select AI opponents
- Click "Create Game"
- Start playing! 🎰

---

## 📦 Detailed Setup

### Prerequisites Installation

#### Python 3.11+
1. Download from [python.org](https://www.python.org/downloads/)
2. **Important**: Check "Add Python to PATH" during installation
3. Verify: `python --version` should show 3.11 or higher

#### Node.js 18+
1. Download from [nodejs.org](https://nodejs.org/)
2. Install the LTS version
3. Verify: `node --version` should show 18 or higher

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Option 1: Using pip
pip install -r requirements.txt

# Option 2: Using Poetry (recommended)
poetry install

# Start the server
python -m app.main

# Or with Poetry
poetry run python -m app.main
```

The backend will start on `http://localhost:8000`

**API Documentation:** http://localhost:8000/docs

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
pnpm install
# or
yarn install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:3000`

### Optional: LLM API Keys

To enable LLM-powered AI opponents:

1. Click the **Settings** (⚙️) button in the app
2. Enter your API keys for:
   - OpenAI (for GPT-4o, GPT-4o-mini)
   - Anthropic (for Claude)
   - DeepSeek (for DeepSeek Chat)
   - Google (for Gemini)
   - xAI (for Grok)
3. Click "Save Settings"
4. The AI strategies will automatically become available

**Note:** API keys are stored locally in your browser and sent to your local backend. They are never committed to the repository or sent to external servers (except the respective LLM providers).

---

## 📁 Project Structure

```
Texas-Holdem-AI/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── config.py          # Configuration settings
│   │   └── core/              # Core game logic
│   │       ├── game_engine/   # Poker engine implementation
│   │       │   ├── engine.py        # Main game engine
│   │       │   ├── deck.py          # Card deck management
│   │       │   ├── hand_evaluator.py # Hand ranking logic
│   │       │   └── pot_manager.py    # Pot calculation
│   │       └── ai_manager/    # AI strategy implementations
│   │           ├── strategies.py     # Rule-based strategies
│   │           └── llm_strategy.py   # LLM-powered strategies
│   ├── requirements.txt       # Python dependencies
│   ├── test_api.py           # API tests
│   ├── test_game.py          # Game engine tests
│   └── simulate_hand.py      # Hand simulation script
│
├── frontend/                  # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx           # Main application component
│   │   ├── api.ts            # API client
│   │   ├── types.ts          # TypeScript type definitions
│   │   └── components/       # React components
│   │       ├── PokerTable.tsx      # Main poker table
│   │       ├── PlayerSeat.tsx      # Individual player display
│   │       ├── Card.tsx            # Playing card component
│   │       ├── ActionPanel.tsx     # Player action controls
│   │       ├── Settings.tsx        # Settings modal
│   │       ├── HandHistoryPanel.tsx # Hand history display
│   │       └── HandResultsCard.tsx  # Results display
│   ├── package.json          # Node dependencies
│   ├── vite.config.ts        # Vite configuration
│   ├── tailwind.config.js    # TailwindCSS configuration
│   └── index.html            # HTML entry point
│
├── database_schema.sql       # Database schema (future use)
├── ARCHITECTURE.md           # Architecture documentation
├── START_POKER_GAME.bat      # One-click Windows launcher
├── START_BACKEND.bat         # Backend launcher
├── START_FRONTEND.bat        # Frontend launcher
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

## 🎮 Game Rules & Features

### Texas Hold'em Rules

This simulator implements standard **No-Limit Texas Hold'em** rules:

1. **Setup**:
   - 2-9 players
   - Each player starts with the same stack (default: 1000 chips)
   - Small blind (default: 5) and Big blind (default: 10) are posted

2. **Betting Rounds**:
   - **Pre-flop**: 2 hole cards dealt to each player
   - **Flop**: 3 community cards revealed
   - **Turn**: 4th community card revealed
   - **River**: 5th community card revealed
   - **Showdown**: Remaining players reveal hands

3. **Actions**:
   - **Fold**: Give up the hand
   - **Check**: Pass action (when no bet to call)
   - **Call**: Match the current bet
   - **Bet**: Make the first bet in a round
   - **Raise**: Increase the current bet
   - **All-In**: Bet all remaining chips

4. **Hand Rankings** (highest to lowest):
   - Royal Flush (A-K-Q-J-10, same suit)
   - Straight Flush
   - Four of a Kind
   - Full House
   - Flush
   - Straight
   - Three of a Kind
   - Two Pair
   - One Pair
   - High Card

### Advanced Features

- **Side Pots**: Automatic creation when players go all-in with different stack sizes
- **Position Rotation**: Dealer button moves clockwise after each hand
- **Blind Posting**: Small and big blinds are automatically posted
- **Action Validation**: Invalid actions are prevented with smart UI controls
- **Hand History**: Complete log of all actions with timestamps, profit/loss tracking, and hand summaries
- **Flexible Hand Evaluation**: Correctly evaluates any combination of 5+ cards (handles edge cases)
- **Auto-Advance Gameplay**: Watch mode or inactive players trigger gradual AI action progression
- **Texas Hold'em Compliant Betting**: Minimum raises follow standard poker rules

---

## 🤖 AI Strategies

### Rule-Based Strategies

#### Aggressive (LAG - Loose Aggressive)
- Plays many hands (high VPIP)
- Bets and raises frequently
- Applies pressure on opponents
- Good for building big pots

#### Conservative (TAG - Tight Aggressive)
- Plays fewer, stronger hands
- Bets aggressively when playing
- Folds weak hands early
- Good for steady, low-risk play

#### Random
- Makes random valid actions
- Useful for testing and unpredictability
- No strategic decision making

### LLM-Powered Strategies

Each LLM strategy receives comprehensive game context:
- Your hole cards and position
- Community cards (flop, turn, river)
- Current pot size and pot odds
- All players' stacks and bets
- Betting history for the hand
- Valid actions available

**Supported LLM Providers:**

| Provider | Models | Strengths |
|----------|--------|-----------|
| **OpenAI** | GPT-4o, GPT-4o-mini | Strong reasoning, strategic play |
| **Anthropic** | Claude 3.5 Sonnet | Excellent analysis, nuanced decisions |
| **DeepSeek** | DeepSeek Chat | Fast, cost-effective |
| **Google** | Gemini 2.5 Flash | Quick responses, good balance |
| **xAI** | Grok Beta | Creative, aggressive play |

**Custom Prompts:**
You can provide custom personality prompts for each LLM agent:
- "Play like a professional poker player"
- "Be extremely aggressive and bluff often"
- "Only play premium hands"
- "Mimic Phil Ivey's playing style"

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Key Endpoints

#### Create Game
```http
POST /api/games
Content-Type: application/json

{
  "player_names": ["Alice"],
  "ai_players": ["aggressive", "claude"],
  "small_blind": 5,
  "big_blind": 10,
  "starting_stack": 1000,
  "ai_prompts": ["", "Play aggressively and bluff often"]
}

Response: GameState object
```

#### Get Game State
```http
GET /api/games/{game_id}

Response: GameState object
```

#### Start Hand
```http
POST /api/games/{game_id}/start

Response: GameState object
```

#### Player Action
```http
POST /api/games/{game_id}/action
Content-Type: application/json

{
  "player_id": "player_uuid",
  "action": "raise",
  "amount": 50
}

Response: GameState object
```

#### List AI Strategies
```http
GET /api/ai/strategies

Response: {
  "strategies": ["aggressive", "conservative", "random", "gpt4", "claude", ...]
}
```

### Interactive API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation where you can test all endpoints.

---

## 🖼 Screenshots

### Main Poker Table
![Poker Table](docs/screenshots/poker-table.png)
*Beautiful poker table with player seats, community cards, and action panel*

### Settings Panel
![Settings](docs/screenshots/settings.png)
*Configure game settings and add LLM API keys*

### Hand Results
![Hand Results](docs/screenshots/hand-results.png)
*Detailed hand results showing winner and all players' cards*

---

## 👨‍💻 Development

### Running Tests

**Backend Tests:**
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest test_game.py
```

**Frontend Tests:**
```bash
cd frontend

# Run tests (when available)
npm test
```

### Code Quality

**Backend:**
```bash
# Format code
black app/

# Sort imports
isort app/

# Lint
flake8 app/
pylint app/
```

**Frontend:**
```bash
# Lint and format
npm run lint
npm run format
```

### Development Mode

Both backend and frontend support hot-reload during development:

- **Backend**: Changes to Python files automatically reload the server
- **Frontend**: Changes to React components instantly update in the browser

---

## 🧪 Testing

### Test the Game Engine

```bash
cd backend
python test_game.py
```

This will:
- Create a sample game with multiple players
- Deal cards and simulate betting rounds
- Test hand evaluation and pot distribution
- Verify all game rules are working correctly

### Test the API

```bash
cd backend
python test_api.py
```

This will:
- Test game creation endpoint
- Test starting hands
- Test player actions
- Verify API responses

### Simulate a Complete Hand

```bash
cd backend
python simulate_hand.py
```

This runs a complete poker hand simulation with multiple AI players.

---

## 🐛 Troubleshooting

### Common Issues

#### "Python not found" or "Node not found"
**Solution:** Make sure Python and Node.js are installed and added to your PATH. Restart your terminal after installation.

#### Port Already in Use
**Problem:** Error saying port 8000 or 3000 is already in use.

**Solution:**
```bash
# Windows - Kill process on port
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

#### Dependencies Won't Install
**Problem:** `pip install` or `npm install` fails

**Solution:**
```bash
# Backend - Try upgrading pip
python -m pip install --upgrade pip
pip install -r requirements.txt

# Frontend - Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### LLM Strategy Not Working
**Problem:** LLM strategy doesn't appear in the list

**Solution:**
1. Verify API key is valid
2. Check Settings panel shows "Valid ✓" for the API key
3. Restart backend after adding API keys
4. Check browser console for errors

#### Game Freezes or Doesn't Update
**Problem:** Game state doesn't update after actions

**Solution:**
1. Check browser console for errors
2. Verify backend is running (check http://localhost:8000/health)
3. Refresh the page
4. Clear browser cache

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit**: `git commit -m 'Add some AmazingFeature'`
6. **Push**: `git push origin feature/AmazingFeature`
7. **Open a Pull Request**

### Ideas for Contributions

- 🎨 UI/UX improvements
- 🤖 New AI strategies
- 📊 Analytics and statistics
- 🎮 Tournament mode
- 💾 Database integration
- 📱 Mobile responsive design
- 🌍 Internationalization
- 🧪 More comprehensive tests

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **React** for the powerful UI library
- **TailwindCSS** for the beautiful styling system
- **OpenAI, Anthropic, DeepSeek, Google, and xAI** for their amazing LLM APIs
- The poker community for game rules and strategy insights

---

## 📞 Contact & Support

- **Issues**: Use the [GitHub Issues](https://github.com/Hunterwu6/Texas-Holdem-AI/issues) page
- **Discussions**: Use [GitHub Discussions](https://github.com/Hunterwu6/Texas-Holdem-AI/discussions)

---

## 🎰 Start Playing!

Ready to play? Just run:

```bash
# Windows
START_POKER_GAME.bat

# Linux/Mac
cd backend && python -m app.main &
cd frontend && npm run dev
```

**Enjoy the game! ♠️ ♥️ ♣️ ♦️**

---

<div align="center">

**Made with ❤️ by Hunter Wu**

⭐ Star this repo if you found it helpful!

</div>
