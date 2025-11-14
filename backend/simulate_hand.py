from app.core.game_engine.engine import GameEngine, GamePhase
from app.core.game_engine.deck import Card


def simulate():
    engine = GameEngine(
        players=[("p1", "Hero"), ("p2", "Villain")],
        small_blind=5,
        big_blind=10,
        starting_stack=1000,
    )
    engine.start_hand()

    hero = engine.players[0]
    villain = engine.players[1]

    hero.cards = [Card("A", "s"), Card("K", "s")]
    villain.cards = [Card("2", "h"), Card("2", "d")]
    engine.community_cards = [
        Card("2", "s"),
        Card("9", "d"),
        Card("Q", "h"),
        Card("3", "c"),
        Card("7", "d"),
    ]
    hero.total_bet = 1000
    villain.total_bet = 1000
    engine.phase = GamePhase.RIVER
    engine._determine_winners()
    print(engine.hand_history[-1])


if __name__ == "__main__":
    simulate()

