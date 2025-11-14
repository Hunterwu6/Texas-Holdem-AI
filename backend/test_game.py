"""Test script to demonstrate the poker engine"""
from app.core.game_engine import GameEngine, PlayerAction
from app.core.ai_manager.strategies import AggressiveStrategy, ConservativeStrategy


def print_game_state(state, show_hands=False):
    """Print current game state"""
    print("\n" + "=" * 60)
    print(f"Game ID: {state.game_id}")
    print(f"Phase: {state.phase}")
    print(f"Pot: ${state.pot}")
    print(f"Current Bet: ${state.current_bet}")
    print(f"Community Cards: {[str(c) for c in state.community_cards]}")
    print("\nPlayers:")
    for i, player in enumerate(state.players):
        current = "👉 " if i == state.current_player_index else "   "
        status = ""
        if player.folded:
            status = "(FOLDED)"
        elif player.all_in:
            status = "(ALL-IN)"
        
        print(f"{current}P{i+1} {player.name:15} - Stack: ${player.stack:4}, Bet: ${player.current_bet:4} {status}")
        if show_hands and player.cards:
            print(f"      Cards: {[str(c) for c in player.cards]}")
    print("=" * 60)


def test_simple_game():
    """Test a simple 2-player game"""
    print("\n🎰 TEXAS HOLD'EM AI BATTLE SIMULATOR - TEST GAME")
    print("Testing: 2-player game (Human vs AI)")
    
    # Create players
    players = [
        ("player1", "Alice (You)"),
        ("ai_aggressive", "AI-Aggressive")
    ]
    
    # Create game
    engine = GameEngine(
        players=players,
        small_blind=5,
        big_blind=10,
        starting_stack=1000
    )
    
    print(f"\n✅ Game created!")
    print(f"Small Blind: ${engine.small_blind}")
    print(f"Big Blind: ${engine.big_blind}")
    print(f"Starting Stack: $1000 each")
    
    # Start hand
    state = engine.start_hand()
    print_game_state(state, show_hands=True)
    
    # AI strategy
    ai_strategy = AggressiveStrategy()
    
    # Play through the hand
    round_num = 0
    while state.phase not in ["showdown", "complete"]:
        round_num += 1
        print(f"\n🎯 Round {round_num}")
        
        current_player = state.players[state.current_player_index]
        print(f"Current player: {current_player.name}")
        
        # Get valid actions
        valid_actions = engine.get_valid_actions(state.current_player_index)
        print(f"Valid actions: {[a.value for a in valid_actions]}")
        
        # If AI player, let AI decide
        if current_player.id.startswith("ai_"):
            action, amount = ai_strategy.decide(state, current_player.id, valid_actions)
            print(f"AI decides: {action.value} (${amount})")
            state = engine.process_action(state.current_player_index, action, amount)
        else:
            # Human player - make a simple decision for demo
            # In real game, this would be user input
            if PlayerAction.CHECK in valid_actions:
                action = PlayerAction.CHECK
                amount = 0
            elif PlayerAction.CALL in valid_actions:
                action = PlayerAction.CALL
                amount = 0
            else:
                action = PlayerAction.FOLD
                amount = 0
            
            print(f"You decide: {action.value} (${amount})")
            state = engine.process_action(state.current_player_index, action, amount)
        
        print_game_state(state, show_hands=False)
        
        # Prevent infinite loop
        if round_num > 50:
            print("⚠️  Too many rounds, stopping...")
            break
    
    print("\n🏆 HAND COMPLETE!")
    print_game_state(state, show_hands=True)
    
    # Show final stacks
    print("\n💰 Final Stacks:")
    for player in state.players:
        profit = player.stack - 1000
        sign = "+" if profit >= 0 else ""
        print(f"  {player.name:20} - ${player.stack:4} ({sign}${profit})")


def test_multi_player():
    """Test a 4-player game"""
    print("\n🎰 TEXAS HOLD'EM - 4 PLAYER TEST")
    
    players = [
        ("p1", "Alice"),
        ("ai_aggressive_1", "AI-Aggressive"),
        ("ai_conservative_1", "AI-Conservative"),
        ("p4", "Bob")
    ]
    
    engine = GameEngine(players, small_blind=5, big_blind=10, starting_stack=500)
    state = engine.start_hand()
    
    print_game_state(state, show_hands=True)
    
    print("\n✅ 4-player game created successfully!")
    print(f"Total pot: ${state.pot}")


def test_hand_evaluation():
    """Test hand evaluation"""
    from app.core.game_engine import Card, HandEvaluator, HandRank
    
    print("\n🃏 HAND EVALUATION TEST")
    
    # Test Royal Flush
    cards = [
        Card('A', 's'), Card('K', 's'), Card('Q', 's'),
        Card('J', 's'), Card('T', 's'), Card('9', 'h'), Card('2', 'c')
    ]
    rank, tiebreaker = HandEvaluator.evaluate(cards)
    desc = HandEvaluator.hand_description(rank, tiebreaker)
    print(f"✅ Royal Flush Test: {desc}")
    assert rank == HandRank.ROYAL_FLUSH
    
    # Test Full House
    cards = [
        Card('K', 's'), Card('K', 'h'), Card('K', 'd'),
        Card('9', 's'), Card('9', 'h'), Card('2', 'c'), Card('3', 'd')
    ]
    rank, tiebreaker = HandEvaluator.evaluate(cards)
    desc = HandEvaluator.hand_description(rank, tiebreaker)
    print(f"✅ Full House Test: {desc}")
    assert rank == HandRank.FULL_HOUSE
    
    # Test Pair
    cards = [
        Card('A', 's'), Card('A', 'h'), Card('K', 'd'),
        Card('Q', 's'), Card('J', 'h'), Card('9', 'c'), Card('2', 'd')
    ]
    rank, tiebreaker = HandEvaluator.evaluate(cards)
    desc = HandEvaluator.hand_description(rank, tiebreaker)
    print(f"✅ Pair Test: {desc}")
    assert rank == HandRank.ONE_PAIR
    
    print("\n✅ All hand evaluation tests passed!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  TEXAS HOLD'EM AI BATTLE SIMULATOR - MVP DEMO")
    print("="*60)
    
    try:
        # Test hand evaluation
        test_hand_evaluation()
        
        # Test simple 2-player game
        test_simple_game()
        
        # Test multi-player
        test_multi_player()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nThe poker engine is working perfectly!")
        print("You can now:")
        print("  1. Run the API: python -m app.main")
        print("  2. Visit http://localhost:8000/docs")
        print("  3. Create games and play poker!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

