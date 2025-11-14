# CLAUDE.md - AI Development Context

**Project**: Texas Hold'em AI Battle Simulator  
**Version**: 1.0  
**Last Updated**: 2025-11-13

---

## 📋 Project Overview

This is a **Texas Hold'em Poker Simulator** where AI agents compete against each other via standardized REST/WebSocket APIs. The system supports:

- **Full No-Limit Hold'em rules** (2-9 players)
- **AI agent integration** via external APIs
- **Built-in AI strategies** (Aggressive, Conservative, Balanced, Random, Adaptive)
- **Human player support** for human vs AI matches
- **Real-time game visualization** with React frontend
- **Comprehensive analytics** and strategy optimization
- **Admin dashboard** for AI configuration and data analysis

---

## 🎯 Core Objectives

1. **Game Engine**: Accurate poker rules implementation with pot management and hand evaluation
2. **AI Integration**: Flexible system for external AI agents to connect and play
3. **Analytics**: Deep statistical analysis and strategy optimization
4. **User Experience**: Beautiful, real-time poker interface
5. **Admin Tools**: Comprehensive AI management and performance monitoring

---

## 🏗️ System Architecture

### Technology Stack

**Backend** (Python):
- FastAPI - Web framework + WebSocket
- SQLAlchemy + Alembic - ORM + migrations
- PostgreSQL - Primary database
- Redis - Caching and real-time data
- Celery - Background tasks
- Pydantic - Data validation

**Frontend** (TypeScript):
- React 18 - UI framework
- TailwindCSS - Styling
- Zustand - State management
- Socket.io - WebSocket client
- Framer Motion - Animations

### Architecture Pattern
**Monolithic Modular** with clear service boundaries:
- Game Engine Service
- AI Manager Service
- Analytics Service
- Admin Service

---

## 📁 Project Structure

```
poker-simulator/
├── backend/
│   ├── app/
│   │   ├── api/              # REST endpoints + WebSocket
│   │   ├── core/             # Business logic
│   │   │   ├── game_engine/  # Poker game logic
│   │   │   ├── ai_manager/   # AI integration
│   │   │   ├── analytics/    # Stats & analysis
│   │   │   └── admin/        # Admin functions
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business services
│   │   ├── repositories/     # Data access
│   │   └── utils/            # Helpers
│   ├── tests/
│   └── pyproject.toml
├── frontend/
│   └── src/
│       ├── components/       # React components
│       ├── hooks/            # Custom hooks
│       ├── stores/           # Zustand stores
│       └── services/         # API clients
└── docs/
```

---

## 🗄️ Database Configuration

### PostgreSQL Connection
```
Host: localhost
Port: 5432
Database: postgres
Username: postgres
Password: Admin@123
```

### Key Tables
- `ai_configurations` - AI agent configs and strategies
- `games` - Game sessions
- `game_players` - Players in each game
- `hands` - Individual hand history
- `actions` - Player actions in each hand
- `hand_results` - Hand outcomes
- `ai_statistics` - Performance metrics
- `audit_logs` - System audit trail

### Redis Cache
- Game state caching (fast access)
- AI health status
- Real-time statistics
- Session management

---

## 🎮 Game Engine Core

### Game Flow
```
1. Create Game → 2. Players Join → 3. Deal Cards
      ↓
4. Betting Rounds (Pre-flop, Flop, Turn, River)
      ↓
5. Showdown → 6. Determine Winners → 7. Distribute Pot
```

### Key Components

**1. Deck Management**
- 52-card deck shuffling
- Card dealing and burning
- Deck reset between hands

**2. Hand Evaluator**
- 7-card hand evaluation (2 hole + 5 community)
- Lookup table optimization (O(1) evaluation)
- Supports all hand rankings

**3. Pot Manager**
- Main pot calculation
- Side pot creation (multi-way all-ins)
- Pot distribution to multiple winners

**4. Betting Logic**
- Action validation (fold, check, call, bet, raise, all-in)
- Bet sizing rules (min/max)
- Position-based action order

---

## 🤖 AI Integration System

### AI Communication Flow

```
Game Engine → AI Manager → HTTP/WebSocket → External AI
                ↓
           (5s timeout)
                ↓
    AI Response → Validate → Execute Action
```

### AI Request Format
```json
{
  "gameId": "uuid",
  "round": "flop",
  "pot": 1500,
  "communityCards": ["As", "Kh", "9d"],
  "playerHand": ["Ac", "Kd"],
  "position": 3,
  "stack": 4500,
  "players": [...],
  "currentBet": 500,
  "minRaise": 1000,
  "availableActions": ["fold", "call", "raise", "all-in"]
}
```

### AI Response Format
```json
{
  "action": "raise",
  "amount": 1500,
  "thinkingTime": 2.3
}
```

### Built-in AI Strategies

| Strategy | VPIP | PFR | 3-Bet | Style |
|----------|------|-----|-------|-------|
| **Aggressive (LAG)** | 45% | 35% | 12% | Loose-Aggressive |
| **Conservative (TAG)** | 18% | 15% | 5% | Tight-Aggressive |
| **Balanced (GTO)** | 27% | 21% | 8% | Game Theory Optimal |
| **Random** | Varies | Varies | Varies | Unpredictable |
| **Adaptive** | Dynamic | Dynamic | Dynamic | Adjusts to opponents |

### Timeout Handling
- Default: 5 seconds per decision
- Action: Auto-fold on timeout
- Retry: 3 attempts with exponential backoff
- Logging: All timeouts recorded for analysis

---

## 📊 Analytics & Statistics

### Real-time Metrics
- **VPIP**: Voluntarily Put In Pot (entry rate)
- **PFR**: Pre-Flop Raise rate
- **3-Bet**: 3-Bet percentage
- **C-Bet**: Continuation bet frequency
- **AF**: Aggression Factor = (Bet + Raise) / Call
- **WTSD**: Went To Showdown rate
- **W$SD**: Won money at showdown

### Analysis Features
1. **Hand Analysis**: Starting hand profitability
2. **Position Analysis**: Profit by position (BTN, CO, MP, etc.)
3. **GTO Deviation**: Compare to optimal strategy
4. **Opponent Modeling**: Profile opponent tendencies
5. **Equity Calculations**: Win probability estimation

### Reports
- Game session reports
- AI performance comparisons
- Strategy effectiveness analysis
- Long-term profitability trends
- Export to PDF/CSV

---

## 🛠️ Development Guidelines

### Code Style
- **Python**: Black formatter, isort, flake8, mypy
- **TypeScript**: ESLint, Prettier
- **Naming**: snake_case (Python), camelCase (TypeScript)
- **Comments**: Docstrings for all public functions
- **Type hints**: Required for all Python functions

### Git Workflow
```bash
# Feature development
git checkout -b feature/feature-name
git commit -m "feat: description"
git push origin feature/feature-name

# Commit prefixes: feat, fix, docs, refactor, test, chore
```

### Testing Requirements
- **Unit tests**: >80% coverage
- **Integration tests**: API endpoints
- **E2E tests**: Complete game flows
- **Test database**: Separate from development

### Environment Setup
```bash
# Backend
cd backend
poetry install
cp .env.example .env
# Edit .env with database credentials
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
pnpm install
cp .env.example .env
pnpm dev
```

---

## 🔐 Security Considerations

### API Security
- **Authentication**: API key + JWT tokens
- **Rate Limiting**: 100 req/min per IP
- **Input Validation**: Pydantic models
- **SQL Injection**: ORM with parameterized queries
- **XSS Protection**: Input sanitization

### AI Agent Security
- **API Key Required**: For AI registration
- **Request Validation**: Verify all inputs
- **Timeout Enforcement**: Prevent hanging
- **Error Isolation**: AI errors don't crash system

---

## 🚀 API Endpoints Reference

### Game Management
```
POST   /api/v1/games              # Create game
GET    /api/v1/games/{game_id}    # Get game details
PUT    /api/v1/games/{game_id}/start  # Start game
POST   /api/v1/games/{game_id}/join   # Join game
POST   /api/v1/games/{game_id}/action # Submit action
```

### AI Management
```
POST   /api/v1/ai/register         # Register AI agent
GET    /api/v1/ai                  # List all AIs
GET    /api/v1/ai/{ai_id}          # Get AI details
PUT    /api/v1/ai/{ai_id}          # Update AI config
DELETE /api/v1/ai/{ai_id}          # Delete AI
POST   /api/v1/ai/{ai_id}/health-check  # Health check
```

### Analytics
```
GET    /api/v1/analytics/ai/{ai_id}/stats  # AI statistics
GET    /api/v1/analytics/hands/{hand_id}   # Hand analysis
GET    /api/v1/analytics/comparison        # Compare AIs
```

### WebSocket Events
```javascript
// Client → Server
socket.emit('join_game', { gameId, playerId });
socket.emit('player_action', { action, amount });

// Server → Client
socket.on('game_started', { ... });
socket.on('player_action', { ... });
socket.on('phase_changed', { ... });
socket.on('hand_complete', { ... });
```

---

## 📐 Data Models

### Game State
```python
{
  "game_id": "uuid",
  "phase": "flop",  # waiting, pre_flop, flop, turn, river, showdown
  "pot": 1500,
  "community_cards": ["As", "Kh", "9d"],
  "dealer_position": 0,
  "current_player": 2,
  "current_bet": 500,
  "min_raise": 1000,
  "players": [
    {
      "id": "p1",
      "name": "AlphaBot",
      "position": 0,
      "stack": 5000,
      "current_bet": 500,
      "status": "active",  # active, folded, all_in
      "cards": ["hidden", "hidden"]  # Only visible to owner
    }
  ]
}
```

### Player Action
```python
{
  "action": "raise",  # fold, check, call, bet, raise, all_in
  "amount": 1500,     # Required for bet/raise
  "player_id": "uuid",
  "timestamp": "2025-11-13T10:30:00Z"
}
```

### AI Configuration
```python
{
  "ai_id": "uuid",
  "name": "AggressiveBot",
  "version": "1.0",
  "connection_type": "REST",  # REST, WebSocket, Local
  "endpoint": "http://localhost:5000/decision",
  "timeout": 5000,
  "strategy_config": {
    "type": "LAG",
    "vpip": 45,
    "pfr": 35,
    "three_bet": 12,
    "cbet": 75,
    "aggression_factor": 4.0
  }
}
```

---

## 🎨 Frontend Design

### Color Scheme
- **Background**: `#0F172A` (Dark slate)
- **Poker Table**: `#065F46` (Green felt)
- **Primary Actions**: `#10B981` (Emerald)
- **Danger Actions**: `#EF4444` (Red)

### Key Components
1. **PokerTable**: Main game table with 9 positions
2. **PlayerCard**: Player info, chips, status
3. **CommunityCards**: Flop, turn, river display
4. **ActionPanel**: Bet controls and action buttons
5. **PotDisplay**: Current pot and side pots
6. **GameLog**: Real-time action feed

### Animations
- Card dealing: 0.3s slide-in
- Chip movement: Bezier curve animation
- Player actions: Fade + scale effects
- Thinking indicator: Pulsing animation

---

## 🧪 Testing Strategy

### Unit Tests
```python
# Test hand evaluation
def test_royal_flush_detection():
    cards = parse_cards(["As", "Ks", "Qs", "Js", "Ts", "9h", "8h"])
    rank = evaluate_hand(cards)
    assert rank == HandRank.ROYAL_FLUSH

# Test pot calculation
def test_side_pot_calculation():
    players = [
        Player(stack=100, bet=100),  # All-in
        Player(stack=1000, bet=500),
        Player(stack=1000, bet=500)
    ]
    pots = calculate_pots(players)
    assert len(pots) == 2  # Main pot + side pot
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_complete_game_flow():
    # Create game
    game = await create_game(...)
    
    # Add players
    await add_player(game.id, player1)
    await add_player(game.id, ai1)
    
    # Start and play
    await start_game(game.id)
    
    # Verify results
    assert game.status == "complete"
```

---

## 📈 Performance Targets

### Response Times
- API: < 100ms (p95)
- WebSocket: < 50ms latency
- Game engine: 1000+ hands/second
- Database queries: < 20ms (p95)

### Scalability
- Concurrent games: 100+
- Players per game: 2-9
- AI agents: Unlimited registrations
- Hands stored: Millions

### Reliability
- AI success rate: > 99%
- System uptime: > 99.5%
- Game completion: > 95%
- Hand accuracy: 100%

---

## 🐛 Common Issues & Solutions

### Issue: AI Timeout
**Cause**: AI agent not responding within 5s  
**Solution**: Auto-fold, log timeout, check AI health

### Issue: Side Pot Calculation Error
**Cause**: Complex all-in scenarios  
**Solution**: Use tested pot manager algorithm

### Issue: WebSocket Disconnection
**Cause**: Network issues or client refresh  
**Solution**: Reconnection logic with state recovery

### Issue: Hand Evaluation Discrepancy
**Cause**: Edge cases in card ranking  
**Solution**: Use verified lookup table

---

## 📚 Key Algorithms

### 1. Hand Evaluation
Uses **perfect hash** with lookup table:
- 7 cards → unique hash → rank lookup
- Time complexity: O(1)
- Space: ~133MB lookup table

### 2. Pot Distribution
```python
def calculate_pots(players):
    # Sort by bet amount
    # Create pots for each all-in level
    # Distribute to eligible players
    # Handle multiple winners (split pot)
```

### 3. GTO Strategy (Balanced AI)
- Range-based decision making
- Pot odds calculation
- Equity estimation
- Mixed strategy (randomization)

### 4. Adaptive AI
- Track opponent statistics
- Identify tendencies
- Exploit weaknesses
- Adjust strategy dynamically

---

## 🔄 State Management

### Backend State
- **PostgreSQL**: Persistent game history
- **Redis**: Current game state (fast access)
- **Memory**: Active game instances

### Frontend State
```typescript
// Zustand store
interface GameStore {
  gameId: string | null;
  gameState: GameState | null;
  players: Player[];
  communityCards: Card[];
  pot: number;
  currentPlayer: number;
  actions: Action[];
  
  // Actions
  joinGame: (gameId: string) => void;
  submitAction: (action: Action) => void;
  updateState: (state: GameState) => void;
}
```

---

## 🎯 MVP Development Phases

### Phase 1: Core Engine (Weeks 1-2)
- [ ] Game engine implementation
- [ ] Hand evaluator
- [ ] Pot manager
- [ ] Basic API endpoints
- [ ] Database schema

### Phase 2: AI Integration (Weeks 3-4)
- [ ] AI client interface
- [ ] Built-in strategies
- [ ] Timeout handling
- [ ] WebSocket events
- [ ] AI management API

### Phase 3: Frontend & UX (Weeks 5-6)
- [ ] React components
- [ ] Real-time updates
- [ ] Animations
- [ ] Admin dashboard
- [ ] Analytics views

### Phase 4: Testing & Polish (Week 7)
- [ ] Comprehensive testing
- [ ] Performance optimization
- [ ] Bug fixes
- [ ] Documentation
- [ ] Deployment preparation

---

## 🔧 Configuration Files

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://postgres:Admin@123@localhost:5432/postgres

# Redis
REDIS_URL=redis://localhost:6379/0

# API
API_HOST=0.0.0.0
API_PORT=8000
API_SECRET_KEY=your-secret-key-here

# CORS
CORS_ORIGINS=http://localhost:3000

# AI Defaults
DEFAULT_AI_TIMEOUT=5000
MAX_AI_RETRIES=3
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

---

## 📖 Additional Resources

### Poker Rules
- [Official Texas Hold'em Rules](https://www.pokerstars.com/poker/games/texas-holdem/)
- [Hand Rankings](https://www.cardplayer.com/rules-of-poker/hand-rankings)

### Game Theory Optimal (GTO)
- [Introduction to GTO Poker](https://upswingpoker.com/gto-poker/)
- [Nash Equilibrium in Poker](https://en.wikipedia.org/wiki/Poker_strategy#Game_theory)

### Technical References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- [Socket.io Protocol](https://socket.io/docs/v4/)

---

## 🤝 Contributing Guidelines

### Before Starting
1. Read this entire CLAUDE.md
2. Review ARCHITECTURE.md
3. Check existing issues/PRs
4. Set up development environment

### Development Process
1. Create feature branch
2. Write tests first (TDD)
3. Implement feature
4. Run linters and tests
5. Update documentation
6. Submit PR with clear description

### Code Review Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] Type hints present
- [ ] Documentation updated
- [ ] No security issues
- [ ] Performance acceptable

---

## 💡 Tips for AI (Claude) Working on This Project

### When Implementing Features
1. **Always check ARCHITECTURE.md** for design patterns
2. **Follow the established structure** in project layout
3. **Use type hints** for all Python functions
4. **Write tests** alongside implementation
5. **Consider edge cases** (all-ins, disconnections, etc.)

### When Fixing Bugs
1. **Reproduce the issue** with a test
2. **Check related code** in the same module
3. **Verify database state** if data-related
4. **Test thoroughly** including edge cases

### When Adding AI Strategies
1. **Extend the base strategy class**
2. **Configure parameters** in strategy_config
3. **Test against other strategies**
4. **Document strategy behavior**

### When Modifying Database
1. **Create Alembic migration**
2. **Update SQLAlchemy models**
3. **Update Pydantic schemas**
4. **Add/update indexes**
5. **Test migration up and down**

---

## 🎓 Poker Domain Knowledge

### Essential Terms
- **Blinds**: Forced bets (small blind, big blind)
- **Position**: Seat relative to dealer button
- **BTN**: Button (dealer position - best position)
- **CO**: Cutoff (one seat before button)
- **MP**: Middle position
- **EP**: Early position
- **SB/BB**: Small blind / Big blind (worst positions)
- **VPIP**: Voluntarily Put money In Pot
- **PFR**: Pre-Flop Raise
- **3-Bet**: Re-raise pre-flop
- **C-Bet**: Continuation bet (bet after raising pre-flop)
- **AF**: Aggression Factor
- **GTO**: Game Theory Optimal
- **LAG**: Loose-Aggressive
- **TAG**: Tight-Aggressive

### Position Importance
**Best to Worst**: BTN > CO > HJ > MP > EP > SB > BB

Acting last (BTN) provides information advantage.

### Pot Odds
```
Pot Odds = Amount to Call / (Pot Size + Amount to Call)
```
Should call if equity > pot odds.

---

## 🔍 Debugging Tips

### Game Engine Issues
- Check game state in Redis
- Verify action sequence
- Log all player actions
- Validate bet amounts

### AI Communication Issues
- Test AI endpoint directly (curl/Postman)
- Check timeout settings
- Verify request format
- Monitor network latency

### Database Issues
- Check connection pool
- Monitor slow queries
- Verify indexes
- Use EXPLAIN ANALYZE

### WebSocket Issues
- Check connection state
- Monitor event flow
- Verify room membership
- Test reconnection logic

---

## 📝 Final Notes

This is a **complex system** with many moving parts:
- Real-time game engine
- External AI integration
- Statistical analysis
- Admin dashboard

**Key Success Factors**:
1. **Accurate poker rules** - No room for errors
2. **Robust AI integration** - Handle failures gracefully
3. **Performance** - Real-time requirements
4. **Data integrity** - Accurate statistics
5. **User experience** - Smooth and engaging

**Development Philosophy**:
- Test-driven development
- Clear separation of concerns
- Comprehensive error handling
- Extensive logging
- Performance monitoring

---

**Good luck building this amazing poker simulator! 🎰🃏**

If you have questions about any aspect of the system, refer to:
1. This CLAUDE.md for context
2. ARCHITECTURE.md for technical details
3. poker-simulator-prd.md for product requirements
4. poker-admin-architecture.md for admin system design

