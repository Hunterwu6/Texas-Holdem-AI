"""Built-in AI strategies"""
from abc import ABC, abstractmethod
from typing import List, Dict
from ..game_engine.engine import GameState, PlayerAction, GamePlayer
from ..game_engine.deck import Card
import random


class AIStrategy(ABC):
    """Base class for AI strategies"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def decide(
        self,
        game_state: GameState,
        player_id: str,
        valid_actions: List[PlayerAction]
    ) -> tuple[PlayerAction, int]:
        """
        Decide what action to take
        Returns (action, amount) tuple
        """
        pass
    
    def _get_player(self, game_state: GameState, player_id: str) -> GamePlayer:
        """Get player from game state"""
        for player in game_state.players:
            if player.id == player_id:
                return player
        raise ValueError(f"Player {player_id} not found")


class AggressiveStrategy(AIStrategy):
    """
    Aggressive (LAG) strategy
    - Plays many hands (VPIP 45%)
    - Raises frequently (PFR 35%)
    - Aggressive post-flop
    """
    
    def __init__(self):
        super().__init__("Aggressive")
        self.vpip = 0.45  # 45% of hands
        self.pfr = 0.35   # 35% raise pre-flop
        self.aggression = 0.7  # 70% aggressive actions
    
    def decide(
        self,
        game_state: GameState,
        player_id: str,
        valid_actions: List[PlayerAction]
    ) -> tuple[PlayerAction, int]:
        """Make aggressive decision"""
        player = self._get_player(game_state, player_id)
        
        # Can't do anything if no valid actions
        if not valid_actions:
            return PlayerAction.FOLD, 0
        
        # Pre-flop: Play aggressively
        if game_state.phase == "pre_flop":
            if PlayerAction.RAISE in valid_actions and random.random() < self.pfr:
                # Raise 3x big blind
                raise_amount = game_state.big_blind * 3
                return PlayerAction.RAISE, min(raise_amount, player.stack)
            elif PlayerAction.BET in valid_actions:
                bet_amount = game_state.big_blind * 3
                return PlayerAction.BET, min(bet_amount, player.stack)
            elif PlayerAction.CALL in valid_actions and random.random() < self.vpip:
                return PlayerAction.CALL, 0
            elif PlayerAction.CHECK in valid_actions:
                return PlayerAction.CHECK, 0
            else:
                return PlayerAction.FOLD, 0
        
        # Post-flop: Continue aggression
        else:
            if random.random() < self.aggression:
                # Be aggressive
                if PlayerAction.RAISE in valid_actions:
                    raise_amount = int(game_state.pot * 0.75)  # 3/4 pot raise
                    return PlayerAction.RAISE, min(raise_amount, player.stack)
                elif PlayerAction.BET in valid_actions:
                    bet_amount = int(game_state.pot * 0.75)
                    return PlayerAction.BET, min(bet_amount, player.stack)
                elif PlayerAction.CALL in valid_actions:
                    return PlayerAction.CALL, 0
                elif PlayerAction.CHECK in valid_actions:
                    return PlayerAction.CHECK, 0
            else:
                # Sometimes check or call
                if PlayerAction.CHECK in valid_actions:
                    return PlayerAction.CHECK, 0
                elif PlayerAction.CALL in valid_actions and random.random() < 0.5:
                    return PlayerAction.CALL, 0
                else:
                    return PlayerAction.FOLD, 0
        
        return PlayerAction.FOLD, 0


class ConservativeStrategy(AIStrategy):
    """
    Conservative (TAG) strategy
    - Plays tight (VPIP 18%)
    - Raises with strong hands (PFR 15%)
    - Cautious post-flop
    """
    
    def __init__(self):
        super().__init__("Conservative")
        self.vpip = 0.18  # 18% of hands
        self.pfr = 0.15   # 15% raise pre-flop
        self.aggression = 0.3  # 30% aggressive actions
    
    def decide(
        self,
        game_state: GameState,
        player_id: str,
        valid_actions: List[PlayerAction]
    ) -> tuple[PlayerAction, int]:
        """Make conservative decision"""
        player = self._get_player(game_state, player_id)
        
        if not valid_actions:
            return PlayerAction.FOLD, 0
        
        # Pre-flop: Play tight
        if game_state.phase == "pre_flop":
            # Only play strong hands
            play_hand = random.random() < self.vpip
            
            if not play_hand:
                if PlayerAction.CHECK in valid_actions:
                    return PlayerAction.CHECK, 0
                return PlayerAction.FOLD, 0
            
            # With strong hands, raise
            if PlayerAction.RAISE in valid_actions and random.random() < (self.pfr / self.vpip):
                raise_amount = game_state.big_blind * 3
                return PlayerAction.RAISE, min(raise_amount, player.stack)
            elif PlayerAction.BET in valid_actions:
                bet_amount = game_state.big_blind * 2
                return PlayerAction.BET, min(bet_amount, player.stack)
            elif PlayerAction.CALL in valid_actions:
                return PlayerAction.CALL, 0
            elif PlayerAction.CHECK in valid_actions:
                return PlayerAction.CHECK, 0
        
        # Post-flop: Play cautiously
        else:
            # Only continue with aggression sometimes
            if random.random() < self.aggression:
                if PlayerAction.BET in valid_actions:
                    bet_amount = int(game_state.pot * 0.5)  # 1/2 pot bet
                    return PlayerAction.BET, min(bet_amount, player.stack)
                elif PlayerAction.RAISE in valid_actions:
                    raise_amount = int(game_state.pot * 0.5)
                    return PlayerAction.RAISE, min(raise_amount, player.stack)
            
            # Otherwise check or fold
            if PlayerAction.CHECK in valid_actions:
                return PlayerAction.CHECK, 0
            elif PlayerAction.CALL in valid_actions and game_state.current_bet < game_state.pot * 0.3:
                return PlayerAction.CALL, 0
            else:
                return PlayerAction.FOLD, 0
        
        return PlayerAction.FOLD, 0


class RandomStrategy(AIStrategy):
    """
    Random strategy for testing
    Makes random valid moves
    """
    
    def __init__(self):
        super().__init__("Random")
    
    def decide(
        self,
        game_state: GameState,
        player_id: str,
        valid_actions: List[PlayerAction]
    ) -> tuple[PlayerAction, int]:
        """Make random decision"""
        if not valid_actions:
            return PlayerAction.FOLD, 0
        
        action = random.choice(valid_actions)
        player = self._get_player(game_state, player_id)
        
        amount = 0
        if action in [PlayerAction.BET, PlayerAction.RAISE]:
            # Random amount between min and max
            min_amount = game_state.big_blind
            max_amount = player.stack
            amount = random.randint(min_amount, max(min_amount, max_amount // 2))
        
        return action, amount

