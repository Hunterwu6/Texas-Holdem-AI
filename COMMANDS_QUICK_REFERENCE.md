# ⚡ Quick Reference Card

**Texas Hold'em AI Battle Simulator - Essential Commands**

---

## 🚀 Start the Server

```bash
# Navigate to backend
cd backend

# Install dependencies (first time only)
pip install fastapi uvicorn pydantic pydantic-settings

# Run the server
python -m app.main

# Alternative: with uvicorn
uvicorn app.main:app --reload --port 8000
```

**Server will start at:** http://localhost:8000

---

## 🧪 Test the Engine

```bash
# Run test script
cd backend
python test_game.py
```

---

## 🌐 Access Points

| Resource | URL | Description |
|----------|-----|-------------|
| **API Root** | http://localhost:8000 | API information |
| **Interactive Docs** | http://localhost:8000/docs | Swagger UI - Test API |
| **ReDoc** | http://localhost:8000/redoc | Alternative API docs |
| **Health Check** | http://localhost:8000/health | Server status |

---

## 📡 API Endpoints Cheat Sheet

### Create Game
```bash
curl -X POST "http://localhost:8000/api/games" \
  -H "Content-Type: application/json" \
  -d '{"player_names":["Alice"],"ai_players":["aggressive","conservative"],"small_blind":5,"big_blind":10,"starting_stack":1000}'
```

### Start Hand
```bash
curl -X POST "http://localhost:8000/api/games/GAME_ID/start"
```

### Get Game State
```bash
curl "http://localhost:8000/api/games/GAME_ID"
```

### Submit Action
```bash
curl -X POST "http://localhost:8000/api/games/GAME_ID/action" \
  -H "Content-Type: application/json" \
  -d '{"player_id":"PLAYER_ID","action":"call","amount":0}'
```

### List All Games
```bash
curl "http://localhost:8000/api/games"
```

### List AI Strategies
```bash
curl "http://localhost:8000/api/ai/strategies"
```

---

## 🎮 Player Actions

| Action | When to Use | Amount Needed |
|--------|-------------|---------------|
| `fold` | Give up hand | 0 |
| `check` | No bet to call | 0 |
| `call` | Match current bet | 0 (auto-calculated) |
| `bet` | First to bet | Bet amount |
| `raise` | Increase bet | Total raise amount |
| `all_in` | Bet everything | 0 (uses all chips) |

---

## 🤖 AI Strategies

| Strategy | Style | VPIP | Description |
|----------|-------|------|-------------|
| `aggressive` | LAG | 45% | Plays many hands, bets/raises often |
| `conservative` | TAG | 18% | Plays tight, careful with money |
| `random` | Mixed | Varies | Makes random valid moves (for testing) |

---

## 💾 File Locations

| File | Path | Purpose |
|------|------|---------|
| **Main App** | `backend/app/main.py` | API endpoints |
| **Game Engine** | `backend/app/core/game_engine/engine.py` | Poker logic |
| **Hand Evaluator** | `backend/app/core/game_engine/hand_evaluator.py` | Hand ranking |
| **AI Strategies** | `backend/app/core/ai_manager/strategies.py` | AI logic |
| **Config** | `backend/app/config.py` | Settings |
| **Test Script** | `backend/test_game.py` | Test the engine |

---

## 🐍 Python Quick Commands

### Test Hand Evaluation
```python
from app.core.game_engine import Card, HandEvaluator

cards = [
    Card('A', 's'), Card('K', 's'), Card('Q', 's'),
    Card('J', 's'), Card('T', 's'), Card('9', 'h'), Card('2', 'c')
]
rank, tiebreaker = HandEvaluator.evaluate(cards)
print(HandEvaluator.hand_description(rank, tiebreaker))
```

### Create Game Programmatically
```python
from app.core.game_engine import GameEngine

players = [("p1", "Alice"), ("p2", "Bob")]
engine = GameEngine(players, small_blind=5, big_blind=10)
state = engine.start_hand()
print(f"Pot: ${state.pot}")
```

---

## 🔧 Troubleshooting Commands

### Check Server Status
```bash
curl http://localhost:8000/health
```

### Kill Process on Port 8000 (if needed)
```bash
# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Reinstall Dependencies
```bash
cd backend
pip uninstall -y fastapi uvicorn pydantic pydantic-settings
pip install fastapi uvicorn pydantic pydantic-settings
```

---

## 📊 Game State Response

```json
{
  "game_id": "uuid",
  "phase": "flop",
  "pot": 150,
  "current_bet": 50,
  "community_cards": ["As", "Kh", "9d"],
  "players": [
    {
      "id": "p1",
      "name": "Alice",
      "stack": 950,
      "position": 0,
      "current_bet": 50,
      "folded": false,
      "all_in": false
    }
  ],
  "dealer_position": 0,
  "current_player": 1,
  "small_blind": 5,
  "big_blind": 10
}
```

---

## 🎯 Common Workflows

### 1. Create AI-Only Game (Watch AI Battle)
```json
POST /api/games
{
  "player_names": [],
  "ai_players": ["aggressive", "conservative", "random"],
  "small_blind": 10,
  "big_blind": 20,
  "starting_stack": 500
}
```

### 2. Create Human vs AI
```json
POST /api/games
{
  "player_names": ["You"],
  "ai_players": ["aggressive", "conservative"],
  "small_blind": 5,
  "big_blind": 10,
  "starting_stack": 1000
}
```

### 3. Full Game Cycle
```bash
# 1. Create game
GAME_ID=$(curl -s -X POST "http://localhost:8000/api/games" \
  -H "Content-Type: application/json" \
  -d '{"player_names":["Alice"],"ai_players":["aggressive"],"small_blind":5,"big_blind":10,"starting_stack":1000}' \
  | jq -r '.game_id')

# 2. Start hand
curl -X POST "http://localhost:8000/api/games/$GAME_ID/start"

# 3. Get state
curl "http://localhost:8000/api/games/$GAME_ID"

# 4. Make action (if your turn)
curl -X POST "http://localhost:8000/api/games/$GAME_ID/action" \
  -H "Content-Type: application/json" \
  -d '{"player_id":"YOUR_PLAYER_ID","action":"call","amount":0}'
```

---

## 📚 Documentation Quick Links

| Document | Purpose |
|----------|---------|
| [MVP_COMPLETE.md](MVP_COMPLETE.md) | What's been delivered |
| [MVP_STARTUP_GUIDE.md](MVP_STARTUP_GUIDE.md) | Detailed startup instructions |
| [backend/README.md](backend/README.md) | Backend documentation |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |

---

## 💡 Pro Tips

1. **Use Swagger UI** - Easiest way to test: http://localhost:8000/docs
2. **Watch AI Play** - Create AI-only games to see strategies in action
3. **Check Health** - Always verify server with `/health` endpoint
4. **Read Responses** - API returns full game state each time
5. **Auto-AI Turns** - AI players automatically make moves

---

## 🎲 Card Notation

| Symbol | Meaning | Example |
|--------|---------|---------|
| **Ranks** | 2-9, T, J, Q, K, A | A = Ace, K = King, T = Ten |
| **Suits** | s, h, d, c | s = Spades, h = Hearts, d = Diamonds, c = Clubs |
| **Format** | `[Rank][Suit]` | "As" = Ace of Spades, "Kh" = King of Hearts |

---

## 🏁 One-Line Starters

```bash
# Install and run
pip install fastapi uvicorn pydantic pydantic-settings && cd backend && python -m app.main

# Test
cd backend && python test_game.py

# Quick game creation (in separate terminal after server starts)
curl -X POST "http://localhost:8000/api/games" -H "Content-Type: application/json" -d '{"player_names":["You"],"ai_players":["aggressive","conservative"],"small_blind":5,"big_blind":10,"starting_stack":1000}'
```

---

**Print this page and keep it handy!** 📄

Or bookmark: `file:///path/to/COMMANDS_QUICK_REFERENCE.md`

**Happy Playing! 🎰**

