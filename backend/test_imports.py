"""Test if all imports work correctly"""
print("Testing imports...")

try:
    from app.main import app
    print("✅ Main app imports successfully!")
    
    from app.core.game_engine import GameEngine, GamePhase, PlayerAction
    print("✅ Game engine imports successfully!")
    
    from app.core.ai_manager.strategies import AggressiveStrategy, ConservativeStrategy, RandomStrategy
    print("✅ AI strategies import successfully!")
    
    print("\n🎉 All imports work correctly!")
    print("\nYou can now start the server with:")
    print("  python -m app.main")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()

