# Texas Hold'em AI Battle Simulator - Backend MVP

## Quick Start

### 1. Install Dependencies

```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install fastapi uvicorn pydantic pydantic-settings
```

### 2. Run the Server

```bash
# Using Poetry
poetry run python -m app.main

# Or directly with Python
python -m app.main

# Or with uvicorn
uvicorn app.main:app --reload --port 8000
```

The API will be available at: http://localhost:8000

API Documentation: http://localhost:8000/docs

### 3. Test the API

#### Create a game with AI players:
```bash
curl -X POST "http://localhost:8000/api/games" \
  -H "Content-Type: application/json" \
  -d '{
    "player_names": ["Alice"],
    "ai_players": ["aggressive", "conservative"],
    "small_blind": 5,
    "big_blind": 10,
    "starting_stack": 1000
  }'
```

#### Start a hand:
```bash
curl -X POST "http://localhost:8000/api/games/{game_id}/start"
```

#### Make a player action:
```bash
curl -X POST "http://localhost:8000/api/games/{game_id}/action" \
  -H "Content-Type: application/json" \
  -d '{
    "player_id": "player_id_here",
    "action": "call",
    "amount": 0
  }'
```

## Available Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/games` - Create new game
- `GET /api/games/{game_id}` - Get game state
- `POST /api/games/{game_id}/start` - Start new hand
- `POST /api/games/{game_id}/action` - Submit player action
- `GET /api/games` - List all games
- `GET /api/ai/strategies` - List AI strategies

## Available AI Strategies

- `aggressive` - LAG (Loose-Aggressive) style
- `conservative` - TAG (Tight-Aggressive) style
- `random` - Random moves for testing

## Features Included

✅ Complete No-Limit Hold'em engine  
✅ Deck management with shuffling  
✅ Hand evaluation (all poker hands)  
✅ Pot and side pot calculation  
✅ Betting logic with validation  
✅ Game state machine (pre-flop → showdown)  
✅ 3 AI strategies  
✅ REST API with auto-documentation  
✅ Automatic AI turn processing  

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   └── core/
│       └── game_engine/
│           ├── deck.py      # Card & Deck classes
│           ├── hand_evaluator.py  # Hand ranking
│           ├── pot_manager.py     # Pot calculation
│           └── engine.py    # Main game engine
│       └── ai_manager/
│           └── strategies.py      # AI strategies
├── pyproject.toml           # Dependencies
├── config.env               # Environment variables
└── README.md                # This file
```

## Next Steps

1. **Test the API** - Use the Swagger UI at http://localhost:8000/docs
2. **Play a game** - Create a game and make moves
3. **Add more AI strategies** - Extend the AIStrategy class
4. **Add database** - Replace in-memory storage
5. **Add WebSocket** - For real-time updates
6. **Build frontend** - Create React UI

## Example Game Flow

1. **Create Game**: POST `/api/games` with players
2. **Start Hand**: POST `/api/games/{id}/start`
3. **Make Moves**: POST `/api/games/{id}/action` (human players)
4. **AI Auto-plays**: AI players make moves automatically
5. **View State**: GET `/api/games/{id}` anytime
6. **Repeat**: Start new hands with `/start`

## Testing

```python
# Test hand evaluation
from app.core.game_engine import Deck, HandEvaluator, Card

deck = Deck()
cards = deck.deal(7)
rank, tiebreaker = HandEvaluator.evaluate(cards)
print(f"Hand: {rank.name}")

# Test game engine
from app.core.game_engine import GameEngine

players = [("p1", "Alice"), ("p2", "Bob")]
engine = GameEngine(players, small_blind=5, big_blind=10)
state = engine.start_hand()
print(f"Game started! Pot: ${state.pot}")
```

## Troubleshooting

**Port already in use**:
```bash
# Use different port
uvicorn app.main:app --port 8001
```

**Import errors**:
```bash
# Make sure you're in the backend directory
cd backend
python -m app.main
```

**Module not found**:
```bash
# Install dependencies
poetry install
# or
pip install fastapi uvicorn pydantic pydantic-settings
```

## MVP Features Complete! 🎉

This MVP includes:
- Working poker engine
- AI opponents
- REST API
- Interactive API docs

You can now:
- Create games
- Play against AI
- Test all poker scenarios
- Extend with more features

Enjoy your poker simulator!

