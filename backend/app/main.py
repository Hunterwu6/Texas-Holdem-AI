"""FastAPI application entry point"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from .config import settings
from .core.game_engine import GameEngine, GamePhase, PlayerAction
from .core.ai_manager.strategies import AggressiveStrategy, ConservativeStrategy, RandomStrategy
from .core.ai_manager.llm_strategy import (
    LLMStrategy,
    OpenAIStrategy, DeepSeekStrategy, ClaudeStrategy, 
    GeminiStrategy, GrokStrategy
)
import uuid
import os

# Initialize FastAPI app
app = FastAPI(
    title="Texas Hold'em AI Battle Simulator",
    description="Poker simulation platform with AI agent integration",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for MVP (would use database in production)
games: Dict[str, GameEngine] = {}
ai_player_prompts: Dict[str, Dict[str, str]] = {}
GEMINI_DEFAULT_MODEL = "gemini-2.5-flash"

# Load LLM API keys from environment or config file
def load_llm_config():
    """Load LLM API keys from llm_config.env if it exists"""
    config_file = "llm_config.env"
    if os.path.exists(config_file):
        with open(config_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_llm_config()


def _has_active_human(engine: GameEngine) -> bool:
    """Check if any human player can still act"""
    return any(
        (not player.id.startswith("ai_")) and player.can_act()
        for player in engine.players
    )

# Initialize AI strategies
ai_strategies = {
    "aggressive": AggressiveStrategy(),
    "conservative": ConservativeStrategy(),
    "random": RandomStrategy(),
}

# Add LLM strategies if API keys are available
if os.getenv("OPENAI_API_KEY"):
    ai_strategies["gpt4"] = OpenAIStrategy(os.getenv("OPENAI_API_KEY"), "gpt-4o-mini")
    ai_strategies["gpt4o"] = OpenAIStrategy(os.getenv("OPENAI_API_KEY"), "gpt-4o")

if os.getenv("DEEPSEEK_API_KEY"):
    ai_strategies["deepseek"] = DeepSeekStrategy(os.getenv("DEEPSEEK_API_KEY"))

if os.getenv("ANTHROPIC_API_KEY"):
    ai_strategies["claude"] = ClaudeStrategy(os.getenv("ANTHROPIC_API_KEY"))

if os.getenv("GEMINI_API_KEY"):
    ai_strategies["gemini"] = GeminiStrategy(os.getenv("GEMINI_API_KEY"), GEMINI_DEFAULT_MODEL)

if os.getenv("GROK_API_KEY"):
    ai_strategies["grok"] = GrokStrategy(os.getenv("GROK_API_KEY"))

print(f"\n🤖 Available AI strategies: {list(ai_strategies.keys())}\n")


# Pydantic models
class CreateGameRequest(BaseModel):
    player_names: List[str]
    ai_players: List[str] = []  # AI strategy names
    ai_prompts: Optional[List[str]] = None
    ai_names: Optional[List[str]] = None
    small_blind: int = 5
    big_blind: int = 10
    starting_stack: int = 1000


class PlayerActionRequest(BaseModel):
    player_id: str
    action: str  # fold, check, call, bet, raise, all_in
    amount: int = 0


class GameResponse(BaseModel):
    game_id: str
    phase: str
    pot: int
    current_bet: int
    community_cards: List[str]
    players: List[Dict]
    dealer_position: int
    current_player: int
    small_blind: int
    big_blind: int
    hand_history: List[Dict] = []
    current_hand_log: List[Dict] = []


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Texas Hold'em AI Battle Simulator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "create_game": "POST /api/games",
            "get_game": "GET /api/games/{game_id}",
            "start_hand": "POST /api/games/{game_id}/start",
            "player_action": "POST /api/games/{game_id}/action",
            "list_games": "GET /api/games"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_games": len(games),
        "available_ai": list(ai_strategies.keys())
    }


@app.post("/api/games", response_model=GameResponse)
async def create_game(request: CreateGameRequest):
    """Create a new game"""
    try:
        print(f"[API] Creating game with request: {request}")
        
        # Create list of players (humans + AIs)
        all_players = []
        
        # Add human players
        for name in request.player_names:
            player_id = str(uuid.uuid4())
            all_players.append((player_id, name))
            print(f"[API] Added human player: {name} ({player_id})")
        
        ai_prompts = request.ai_prompts or []
        ai_names = request.ai_names or []
        game_prompts: Dict[str, str] = {}
        
        # Add AI players
        for idx, ai_strategy in enumerate(request.ai_players):
            if ai_strategy not in ai_strategies:
                print(f"[API] ERROR: Unknown AI strategy: {ai_strategy}")
                raise HTTPException(400, f"Unknown AI strategy: {ai_strategy}")
            player_id = f"ai_{ai_strategy}_{uuid.uuid4().hex[:8]}"
            ai_name = f"AI-{ai_strategy.title()}"
            if idx < len(ai_names):
                name_override = ai_names[idx].strip()
                if name_override:
                    ai_name = name_override
            all_players.append((player_id, ai_name))
            print(f"[API] Added AI player: {ai_strategy} ({player_id}) as {ai_name}")
            prompt = ""
            if idx < len(ai_prompts):
                prompt = ai_prompts[idx].strip()
            game_prompts[player_id] = prompt
        
        if len(all_players) < 2:
            print(f"[API] ERROR: Not enough players: {len(all_players)}")
            raise HTTPException(400, "Need at least 2 players")
        if len(all_players) > 9:
            print(f"[API] ERROR: Too many players: {len(all_players)}")
            raise HTTPException(400, "Maximum 9 players")
        
        print(f"[API] Creating game engine with {len(all_players)} players")
        
        # Create game engine
        engine = GameEngine(
            players=all_players,
            small_blind=request.small_blind,
            big_blind=request.big_blind,
            starting_stack=request.starting_stack
        )
        
        games[engine.game_id] = engine
        ai_player_prompts[engine.game_id] = game_prompts
        state = engine.get_state()
        
        print(f"[API] Game created successfully: {engine.game_id}")
        
        return GameResponse(**state.to_dict())
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] ERROR: Unexpected error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Internal server error: {str(e)}")


@app.get("/api/games/{game_id}", response_model=GameResponse)
async def get_game(game_id: str):
    """Get game state"""
    if game_id not in games:
        raise HTTPException(404, "Game not found")
    
    engine = games[game_id]
    state = engine.get_state()
    return GameResponse(**state.to_dict())


@app.post("/api/games/{game_id}/start", response_model=GameResponse)
async def start_hand(game_id: str):
    """Start a new hand"""
    if game_id not in games:
        raise HTTPException(404, "Game not found")
    
    engine = games[game_id]
    
    try:
        state = engine.start_hand()
        
        # Only auto-run AI if at least one human is still active
        if _has_active_human(engine):
            state = await _process_ai_turns(engine)
        else:
            state = engine.get_state()
        
        return GameResponse(**state.to_dict())
    
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/api/games/{game_id}/action", response_model=GameResponse)
async def player_action(game_id: str, request: PlayerActionRequest):
    """Process player action"""
    if game_id not in games:
        raise HTTPException(404, "Game not found")
    
    engine = games[game_id]
    
    try:
        # Find player index
        player_index = None
        for i, player in enumerate(engine.players):
            if player.id == request.player_id:
                player_index = i
                break
        
        if player_index is None:
            raise HTTPException(404, "Player not found")
        
        # Validate it's their turn
        if engine.current_player_index != player_index:
            raise HTTPException(400, "Not your turn")
        
        # Convert action string to enum
        try:
            action = PlayerAction(request.action.lower())
        except ValueError:
            raise HTTPException(400, f"Invalid action: {request.action}")
        
        # Process action
        state = engine.process_action(player_index, action, request.amount)
        
        # Process AI turns until it's human's turn again (within same betting round)
        # This allows AI to act but stops before advancing to next phase
        if _has_active_human(engine):
            state = await _process_ai_turns_until_human(engine)
        else:
            state = engine.get_state()
        
        return GameResponse(**state.to_dict())
    
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get("/api/games")
async def list_games():
    """List all active games"""
    return {
        "games": [
            {
                "game_id": game_id,
                "phase": engine.phase.value,
                "num_players": len(engine.players),
                "pot": sum(p.total_bet for p in engine.players)
            }
            for game_id, engine in games.items()
        ]
    }


@app.get("/api/ai/strategies")
async def list_ai_strategies():
    """List available AI strategies"""
    return {
        "strategies": list(ai_strategies.keys())
    }


class LLMKeysRequest(BaseModel):
    openai: str = ""
    deepseek: str = ""
    anthropic: str = ""
    gemini: str = ""
    grok: str = ""


@app.post("/api/llm/configure")
async def configure_llm_keys(request: LLMKeysRequest):
    """Configure LLM API keys dynamically"""
    global ai_strategies
    
    # Remove old LLM strategies
    llm_keys = ["gpt4", "gpt4o", "deepseek", "claude", "gemini", "grok"]
    for key in llm_keys:
        if key in ai_strategies:
            del ai_strategies[key]
    
    # Add new LLM strategies if keys provided
    if request.openai:
        ai_strategies["gpt4"] = OpenAIStrategy(request.openai, "gpt-4o-mini")
        ai_strategies["gpt4o"] = OpenAIStrategy(request.openai, "gpt-4o")
    
    if request.deepseek:
        ai_strategies["deepseek"] = DeepSeekStrategy(request.deepseek)
    
    if request.anthropic:
        ai_strategies["claude"] = ClaudeStrategy(request.anthropic)
    
    if request.gemini:
        ai_strategies["gemini"] = GeminiStrategy(request.gemini, GEMINI_DEFAULT_MODEL)
    
    if request.grok:
        ai_strategies["grok"] = GrokStrategy(request.grok)
    
    print(f"\n🔄 LLM strategies updated: {list(ai_strategies.keys())}\n")
    
    return {
        "success": True,
        "strategies": list(ai_strategies.keys())
    }


class ValidateAPIKeyRequest(BaseModel):
    provider: str
    apiKey: str


@app.post("/api/llm/validate")
async def validate_llm_api_key(request: ValidateAPIKeyRequest):
    """Validate an LLM API key"""
    try:
        provider = request.provider.lower()
        api_key = request.apiKey
        
        if not api_key:
            return {"valid": False, "error": "API key is required"}
        
        # Create a test strategy and try to make a simple call
        import httpx
        
        if provider == "openai":
            # Test OpenAI API
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"}
                )
                if response.status_code == 200:
                    return {"valid": True}
                else:
                    return {"valid": False, "error": f"API returned {response.status_code}"}
        
        elif provider == "deepseek":
            # Test DeepSeek API
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 1
                    }
                )
                if response.status_code == 200:
                    return {"valid": True}
                elif response.status_code == 401:
                    return {"valid": False, "error": "Invalid API key"}
                elif response.status_code == 402:
                    return {"valid": False, "error": "Payment required - Add credits to your account"}
                elif response.status_code == 400:
                    # 400 might be ok if it's just a bad request format but auth worked
                    return {"valid": True}
                else:
                    return {"valid": False, "error": f"API returned {response.status_code}"}
        
        elif provider == "anthropic":
            # Test Anthropic API
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "claude-3-5-sonnet-20241022",
                        "max_tokens": 1,
                        "messages": [{"role": "user", "content": "test"}]
                    }
                )
                if response.status_code in [200, 400]:
                    return {"valid": True}
                elif response.status_code == 401:
                    return {"valid": False, "error": "Invalid API key"}
                else:
                    return {"valid": False, "error": f"API returned {response.status_code}"}
        
        elif provider == "gemini":
            # Test Gemini API
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_DEFAULT_MODEL}:generateContent?key={api_key}",
                    headers={"Content-Type": "application/json"},
                    json={
                        "contents": [{"parts": [{"text": "test"}]}],
                        "generationConfig": {"maxOutputTokens": 1}
                    }
                )
                if response.status_code == 200:
                    return {"valid": True}
                elif response.status_code == 400:
                    try:
                        error_data = response.json()
                        if "API key not valid" in str(error_data):
                            return {"valid": False, "error": "Invalid API key"}
                        else:
                            return {"valid": True}
                    except:
                        return {"valid": True}
                elif response.status_code == 403:
                    return {"valid": False, "error": "Invalid API key or quota exceeded"}
                elif response.status_code == 404:
                    return {"valid": False, "error": f"Model {GEMINI_DEFAULT_MODEL} not available"}
                else:
                    return {"valid": False, "error": f"API returned {response.status_code}"}
        
        elif provider == "grok":
            # Test Grok API
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={
                        "model": "grok-beta",
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 1
                    }
                )
                if response.status_code in [200, 400]:
                    return {"valid": True}
                elif response.status_code == 401:
                    return {"valid": False, "error": "Invalid API key"}
                else:
                    return {"valid": False, "error": f"API returned {response.status_code}"}
        
        else:
            return {"valid": False, "error": f"Unknown provider: {provider}"}
    
    except httpx.TimeoutException:
        return {"valid": False, "error": "Request timed out"}
    except Exception as e:
        print(f"[API] Validation error: {e}")
        return {"valid": False, "error": str(e)}


@app.post("/api/games/{game_id}/advance", response_model=GameResponse)
async def advance_ai_action(game_id: str):
    """Advance game by one AI action (for watch mode)"""
    if game_id not in games:
        raise HTTPException(404, "Game not found")
    
    engine = games[game_id]
    
    try:
        # Process only ONE AI turn
        state = await _process_ai_turns(engine, process_all=False)
        return GameResponse(**state.to_dict())
    except Exception as e:
        print(f"[API] ERROR in advance_ai_action: {type(e).__name__}: {str(e)}")
        raise HTTPException(500, f"Failed to advance game: {str(e)}")


# Helper functions

async def _process_ai_turns_until_human(engine: GameEngine):
    """Process AI turns until it's a human player's turn
    
    Key behavior:
    - Processes AI turns in the current betting round
    - When phase changes (e.g., pre-flop → flop):
      * Checks who acts first in new phase
      * If AI acts first: continues processing
      * If human acts first: stops
    - Always stops when it's a human's turn
    
    This ensures humans get to act in every betting round where they're supposed to act.
    """
    max_iterations = 100
    iterations = 0
    starting_phase = engine.phase
    phase_just_changed = False
    prompts_for_game = ai_player_prompts.get(engine.game_id, {})
    
    print(f"[AI] Processing AI turns starting in {starting_phase.value} phase")
    
    while iterations < max_iterations:
        iterations += 1
        
        # Check if game is over
        if engine.phase in [GamePhase.SHOWDOWN, GamePhase.COMPLETE]:
            print(f"[AI] Game over at {engine.phase.value}, stopping")
            break
        
        # Detect phase change
        if engine.phase != starting_phase:
            print(f"[AI] Phase changed from {starting_phase.value} to {engine.phase.value}")
            starting_phase = engine.phase
            phase_just_changed = True
            
            # Check who acts first in new phase
            current_player = engine.players[engine.current_player_index]
            if not current_player.id.startswith("ai_"):
                print(f"[AI] Human ({current_player.name}) acts first in {engine.phase.value}, stopping")
                break
            else:
                print(f"[AI] AI ({current_player.name}) acts first in {engine.phase.value}, continuing")
                phase_just_changed = False
        
        current_player = engine.players[engine.current_player_index]
        
        # If current player is human, stop
        if not current_player.id.startswith("ai_"):
            print(f"[AI] Current player is human ({current_player.name}), stopping")
            break
        
        # If player can't act, move to next
        if not current_player.can_act():
            engine._next_player()
            continue
        
        # Determine AI strategy from player ID
        strategy_name = "random"
        if "_" in current_player.id:
            parts = current_player.id.split("_")
            if len(parts) >= 2:
                strategy_name = parts[1]
        
        strategy = ai_strategies.get(strategy_name, ai_strategies["random"])
        
        # Get valid actions
        state = engine.get_state()
        valid_actions = engine._get_valid_actions(engine.current_player_index)
        
        # Get AI decision
        try:
            custom_prompt = prompts_for_game.get(current_player.id, "").strip()
            if isinstance(strategy, LLMStrategy):
                action, amount = strategy.decide(
                    state,
                    current_player.id,
                    valid_actions,
                    custom_prompt if custom_prompt else None
                )
            else:
                action, amount = strategy.decide(state, current_player.id, valid_actions)
            print(f"[AI] {current_player.name} ({strategy_name}): {action.value} ${amount}")
            state = engine.process_action(engine.current_player_index, action, amount)
        except Exception as e:
            # If AI makes invalid move, fold
            print(f"[AI] Error with {current_player.name}: {e}, folding")
            state = engine.process_action(engine.current_player_index, PlayerAction.FOLD, 0)
    
    return engine.get_state()


async def _process_ai_turns(engine: GameEngine, process_all: bool = True):
    """Process AI player turns automatically
    
    Args:
        engine: Game engine instance
        process_all: If True, process all AI turns until human or end.
                    If False, process only ONE AI turn.
    """
    max_iterations = 100 if process_all else 1
    iterations = 0
    prompts_for_game = ai_player_prompts.get(engine.game_id, {})
    
    while iterations < max_iterations:
        iterations += 1
        
        # Check if game is over or no one can act
        if engine.phase in [GamePhase.SHOWDOWN, GamePhase.COMPLETE]:
            break
        
        current_player = engine.players[engine.current_player_index]
        
        # If current player is not AI, stop
        if not current_player.id.startswith("ai_"):
            break
        
        # If player can't act, move to next
        if not current_player.can_act():
            engine._next_player()
            continue
        
        # Determine AI strategy
        strategy_name = current_player.id.split("_")[1]
        if strategy_name not in ai_strategies:
            # Default to random
            strategy = RandomStrategy()
        else:
            strategy = ai_strategies[strategy_name]
        
        # Get valid actions
        valid_actions = engine.get_valid_actions(engine.current_player_index)
        
        # Get AI decision
        state = engine.get_state()
        custom_prompt = prompts_for_game.get(current_player.id, "").strip()
        if isinstance(strategy, LLMStrategy):
            action, amount = strategy.decide(
                state,
                current_player.id,
                valid_actions,
                custom_prompt if custom_prompt else None
            )
        else:
            action, amount = strategy.decide(state, current_player.id, valid_actions)
        
        # Process action
        try:
            state = engine.process_action(engine.current_player_index, action, amount)
        except Exception as e:
            # If AI makes invalid move, fold
            state = engine.process_action(engine.current_player_index, PlayerAction.FOLD, 0)
        
        # If not processing all, break after one action
        if not process_all:
            break
    
    return engine.get_state()


if __name__ == "__main__":
    import uvicorn
    print(f"\n🚀 Starting server on {settings.API_HOST}:{settings.API_PORT}")
    print(f"📚 API Docs: http://localhost:{settings.API_PORT}/docs")
    print(f"❤️  Health: http://localhost:{settings.API_PORT}/health\n")
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)

