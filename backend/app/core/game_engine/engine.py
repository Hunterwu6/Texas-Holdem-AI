"""Main game engine for Texas Hold'em"""
from enum import Enum
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from .deck import Deck, Card
from .hand_evaluator import HandEvaluator, HandRank
from .pot_manager import PotManager, Player, Pot
import uuid


class GamePhase(str, Enum):
    """Game phases"""
    WAITING = "waiting"
    PRE_FLOP = "pre_flop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"
    COMPLETE = "complete"


class PlayerAction(str, Enum):
    """Player actions"""
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all_in"


@dataclass
class GamePlayer:
    """Player in a game"""
    id: str
    name: str
    stack: int
    position: int
    current_bet: int = 0
    total_bet: int = 0
    folded: bool = False
    all_in: bool = False
    cards: List[Card] = field(default_factory=list)
    
    def can_act(self) -> bool:
        """Check if player can take action"""
        return not self.folded and not self.all_in and self.stack > 0


@dataclass
class GameState:
    """Current state of the game"""
    game_id: str
    phase: GamePhase
    pot: int
    current_bet: int
    community_cards: List[Card]
    players: List[GamePlayer]
    dealer_position: int
    current_player_index: int
    small_blind: int
    big_blind: int
    hand_history: List[Dict] = field(default_factory=list)
    current_hand_log: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API"""
        return {
            "game_id": self.game_id,
            "phase": self.phase.value,
            "pot": self.pot,
            "current_bet": self.current_bet,
            "community_cards": [str(c) for c in self.community_cards],
            "players": [
                {
                    "id": p.id,
                    "name": p.name,
                    "stack": p.stack,
                    "position": p.position,
                    "current_bet": p.current_bet,
                    "folded": p.folded,
                    "all_in": p.all_in,
                    "cards": [str(c) for c in p.cards] if p.cards else [],
                }
                for p in self.players
            ],
            "dealer_position": self.dealer_position,
            "current_player": self.current_player_index,
            "small_blind": self.small_blind,
            "big_blind": self.big_blind,
            "hand_history": self.hand_history,
            "current_hand_log": self.current_hand_log,
        }


class GameEngine:
    """Main game engine for No-Limit Texas Hold'em"""
    
    def __init__(
        self,
        players: List[Tuple[str, str]],  # (player_id, player_name)
        small_blind: int = 5,
        big_blind: int = 10,
        starting_stack: int = 1000
    ):
        if len(players) < 2 or len(players) > 9:
            raise ValueError("Must have 2-9 players")
        
        self.game_id = str(uuid.uuid4())
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.deck = Deck()
        self.community_cards: List[Card] = []
        
        # Initialize players
        self.players: List[GamePlayer] = [
            GamePlayer(
                id=pid,
                name=pname,
                stack=starting_stack,
                position=i
            )
            for i, (pid, pname) in enumerate(players)
        ]
        
        self.dealer_position = len(self.players) - 1
        self.current_player_index = 0
        self.phase = GamePhase.WAITING
        self.current_bet = 0
        self.last_raiser_index: Optional[int] = None
        self.pending_actions: set[str] = set()
        self.hand_history: List[Dict] = []
        self.current_hand_log: List[Dict] = []
        self.hand_number = 0
        self.hand_starting_stacks: Dict[str, int] = {}
    
    def start_hand(self) -> GameState:
        """Start a new hand"""
        active_with_chips = [p for p in self.players if p.stack > 0]
        if len(active_with_chips) < 2:
            raise ValueError("Need at least 2 players with chips to start a hand")
        
        self.hand_number += 1
        self.current_hand_log = []
        
        # Reset for new hand
        self.deck.reset()
        self.deck.shuffle()
        self.community_cards = []
        self.current_bet = 0
        self.last_raiser_index = None
        
        # Reset players
        for player in self.players:
            player.current_bet = 0
            player.total_bet = 0
            player.folded = False
            player.all_in = False
            player.cards = []
        
        self._advance_dealer_button()
        
        # Post blinds
        sb_pos, bb_pos = self._post_blinds()
        
        # Deal hole cards
        self._deal_hole_cards()
        
        # Set phase to pre-flop
        self.phase = GamePhase.PRE_FLOP
        
        # First to act is after big blind
        self.current_player_index = (bb_pos + 1) % len(self.players)
        safety_counter = 0
        while not self.players[self.current_player_index].can_act():
            self._next_player()
            safety_counter += 1
            if safety_counter > len(self.players):
                break
        
        self._initialize_pending_actions()
        self.hand_starting_stacks = {
            player.id: player.stack for player in self.players
        }
        
        return self.get_state()
    
    def _post_blinds(self) -> Tuple[int, int]:
        """Post small and big blinds"""
        sb_pos = self._next_player_with_stack(self.dealer_position)
        bb_pos = self._next_player_with_stack(sb_pos)
        
        # Small blind
        sb_player = self.players[sb_pos]
        self._commit_chips(sb_player, self.small_blind)
        
        # Big blind
        bb_player = self.players[bb_pos]
        self._commit_chips(bb_player, self.big_blind)
        
        self.current_bet = max(sb_player.current_bet, bb_player.current_bet)
        return sb_pos, bb_pos
    
    def _deal_hole_cards(self) -> None:
        """Deal 2 cards to each player"""
        for _ in range(2):
            for player in self.players:
                if not player.folded:
                    card = self.deck.deal_one()
                    if card:
                        player.cards.append(card)
    
    def get_state(self) -> GameState:
        """Get current game state"""
        return GameState(
            game_id=self.game_id,
            phase=self.phase,
            pot=sum(p.total_bet for p in self.players),
            current_bet=self.current_bet,
            community_cards=self.community_cards.copy(),
            players=self.players.copy(),
            dealer_position=self.dealer_position,
            current_player_index=self.current_player_index,
            small_blind=self.small_blind,
            big_blind=self.big_blind,
            hand_history=self.hand_history.copy(),
            current_hand_log=self.current_hand_log.copy(),
        )
    
    def get_valid_actions(self, player_index: int) -> List[PlayerAction]:
        """Get valid actions for a player"""
        player = self.players[player_index]
        
        if not player.can_act():
            return []
        
        actions = [PlayerAction.FOLD]
        
        # Can check if no bet to match
        if player.current_bet == self.current_bet:
            actions.append(PlayerAction.CHECK)
        
        # Can call if there's a bet to match and player has chips
        if player.current_bet < self.current_bet and player.stack > 0:
            actions.append(PlayerAction.CALL)
        
        # Can bet if no current bet
        if self.current_bet == 0 and player.stack > 0:
            actions.append(PlayerAction.BET)
        
        # Can raise if there's a current bet and player has chips
        if self.current_bet > 0 and player.stack > 0:
            call_amount = self.current_bet - player.current_bet
            if player.stack > call_amount:
                actions.append(PlayerAction.RAISE)
        
        # Can always go all-in if have chips
        if player.stack > 0:
            actions.append(PlayerAction.ALL_IN)
        
        return actions
    
    def _get_valid_actions(self, player_index: int) -> List[PlayerAction]:
        """Get list of valid actions for a player"""
        player = self.players[player_index]
        valid_actions = []
        
        if not player.can_act():
            return valid_actions
        
        # Can always fold
        valid_actions.append(PlayerAction.FOLD)
        
        # Check if can check (no bet to call)
        if self.current_bet == player.current_bet:
            valid_actions.append(PlayerAction.CHECK)
        else:
            # Can call if there's a bet
            valid_actions.append(PlayerAction.CALL)
        
        # Can raise/bet if has enough chips
        min_raise = self.current_bet + self.big_blind
        if player.stack > min_raise:
            if self.current_bet == 0:
                valid_actions.append(PlayerAction.BET)
            else:
                valid_actions.append(PlayerAction.RAISE)
        
        # Can always go all-in if has chips
        if player.stack > 0:
            valid_actions.append(PlayerAction.ALL_IN)
        
        return valid_actions
    
    def process_action(
        self,
        player_index: int,
        action: PlayerAction,
        amount: int = 0
    ) -> GameState:
        """Process a player action"""
        player = self.players[player_index]
        
        if not player.can_act():
            raise ValueError(f"Player {player.name} cannot act")
        
        log_entry = {
            "hand_number": self.hand_number,
            "player_id": player.id,
            "player_name": player.name,
            "action": action.value,
            "amount": amount,
            "phase": self.phase.value,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        if action == PlayerAction.FOLD:
            player.folded = True
            self._remove_from_pending(player_index)
            log_entry["amount"] = 0
        
        elif action == PlayerAction.CHECK:
            if player.current_bet != self.current_bet:
                raise ValueError("Cannot check, must call or raise")
            self._remove_from_pending(player_index)
        
        elif action == PlayerAction.CALL:
            call_amount = min(self.current_bet - player.current_bet, player.stack)
            self._commit_chips(player, call_amount)
            self._remove_from_pending(player_index)
            log_entry["amount"] = call_amount
        
        elif action == PlayerAction.BET:
            if self.current_bet != 0:
                raise ValueError("Cannot bet, there is already a bet")
            if amount <= 0:
                raise ValueError("Bet amount must be positive")
            bet_amount = min(amount, player.stack)
            if bet_amount <= 0:
                raise ValueError("Insufficient chips to bet")
            self._commit_chips(player, bet_amount)
            self.current_bet = player.current_bet
            self.last_raiser_index = player_index
            self._initialize_pending_actions(exclude_player_index=player_index)
            log_entry["amount"] = bet_amount
        
        elif action == PlayerAction.RAISE:
            if self.current_bet == 0:
                raise ValueError("Cannot raise, there is no bet to raise")
            min_target = self.current_bet + self.big_blind
            desired_total = max(amount, min_target)
            additional_needed = desired_total - player.current_bet
            if additional_needed <= 0:
                raise ValueError("Raise amount must exceed current bet")
            self._commit_chips(player, additional_needed)
            self.current_bet = max(self.current_bet, player.current_bet)
            self.last_raiser_index = player_index
            self._initialize_pending_actions(exclude_player_index=player_index)
            log_entry["amount"] = additional_needed
        
        elif action == PlayerAction.ALL_IN:
            if player.stack <= 0:
                raise ValueError("Player has no chips to go all-in")
            previous_bet = player.current_bet
            previous_current = self.current_bet
            self._commit_chips(player, player.stack)
            if player.current_bet > previous_current:
                self.current_bet = player.current_bet
                self.last_raiser_index = player_index
                self._initialize_pending_actions(exclude_player_index=player_index)
                log_entry["amount"] = player.current_bet - previous_bet
            else:
                self._remove_from_pending(player_index)
                log_entry["amount"] = player.current_bet - previous_bet
        
        self.current_hand_log.append(log_entry)
        
        # If everyone else folded, hand ends immediately
        if self._check_for_immediate_win():
            return self.get_state()
        
        # Move to next player or next phase
        if self._is_betting_round_complete():
            self._advance_phase()
        else:
            self._next_player()
        
        return self.get_state()
    
    def _next_player(self) -> None:
        """Move to next active player"""
        start_index = self.current_player_index
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            player = self.players[self.current_player_index]
            
            if player.can_act():
                break
            
            # If we've gone full circle, betting round is complete
            if self.current_player_index == start_index:
                self._advance_phase()
                break
    
    def _is_betting_round_complete(self) -> bool:
        """Check if current betting round is complete"""
        active_players = [p for p in self.players if p.can_act()]
        
        # If only one player left, round is complete
        if len(active_players) <= 1:
            return True
        
        return len(self.pending_actions) == 0
    
    def _check_for_immediate_win(self) -> bool:
        """If all but one player have folded, award the pot immediately"""
        active_players = [p for p in self.players if not p.folded]
        if len(active_players) != 1:
            return False
        
        winner = active_players[0]
        total_pot = sum(p.total_bet for p in self.players)
        if total_pot > 0:
            winner.stack += total_pot
        
        winnings = {winner.id: total_pot}
        player_hands: Dict[str, Tuple[HandRank, List[int]]] = {}
        if len(self.community_cards) + len(winner.cards) >= 5:
            player_hands[winner.id] = HandEvaluator.evaluate(winner.cards + self.community_cards)
        
        pots = [Pot(amount=total_pot, eligible_players=[winner.id])]
        self._record_hand_summary(player_hands, winnings, pots)
        
        # Reset player bets since pot awarded
        for player in self.players:
            player.total_bet = 0
            player.current_bet = 0
        
        self.current_bet = 0
        self.phase = GamePhase.COMPLETE
        self.pending_actions.clear()
        self.current_player_index = winner.position
        return True
    
    def _advance_phase(self) -> None:
        """Advance to next game phase"""
        # Reset current bet for new round
        self.current_bet = 0
        for player in self.players:
            player.current_bet = 0
        self.last_raiser_index = None
        
        if self.phase == GamePhase.PRE_FLOP:
            # Deal flop
            self.deck.burn()
            self.community_cards.extend(self.deck.deal(3))
            self.phase = GamePhase.FLOP
            self._set_first_to_act()
            self._initialize_pending_actions()
        
        elif self.phase == GamePhase.FLOP:
            # Deal turn
            self.deck.burn()
            self.community_cards.extend(self.deck.deal(1))
            self.phase = GamePhase.TURN
            self._set_first_to_act()
            self._initialize_pending_actions()
        
        elif self.phase == GamePhase.TURN:
            # Deal river
            self.deck.burn()
            self.community_cards.extend(self.deck.deal(1))
            self.phase = GamePhase.RIVER
            self._set_first_to_act()
            self._initialize_pending_actions()
        
        elif self.phase == GamePhase.RIVER:
            # Go to showdown
            self.phase = GamePhase.SHOWDOWN
            self._determine_winners()
            self.pending_actions.clear()
        
        else:
            self.phase = GamePhase.COMPLETE
            self.pending_actions.clear()
    
    def _set_first_to_act(self) -> None:
        """Set first player to act (first active player after dealer)"""
        self.current_player_index = (self.dealer_position + 1) % len(self.players)
        if not self.players[self.current_player_index].can_act():
            self._next_player()

    def _initialize_pending_actions(self, exclude_player_index: Optional[int] = None) -> None:
        """Initialize pending actions set for current betting round"""
        self.pending_actions = {
            player.id
            for idx, player in enumerate(self.players)
            if player.can_act() and idx != exclude_player_index
        }

    def _remove_from_pending(self, player_index: int) -> None:
        """Remove player from pending actions"""
        player_id = self.players[player_index].id
        self.pending_actions.discard(player_id)
    
    def _determine_winners(self) -> Dict[str, int]:
        """Determine winners and distribute pots"""
        # Evaluate all non-folded players' hands
        player_hands: Dict[str, Tuple[HandRank, List[int]]] = {}
        
        for player in self.players:
            if not player.folded and player.cards:
                all_cards = player.cards + self.community_cards
                rank, tiebreaker = HandEvaluator.evaluate(all_cards)
                player_hands[player.id] = (rank, tiebreaker)
        
        # Calculate pots
        pot_players = [
            Player(
                id=p.id,
                bet=p.total_bet,
                stack=p.stack,
                folded=p.folded
            )
            for p in self.players
        ]
        pots = PotManager.calculate_pots(pot_players)
        
        # Determine winners for each pot
        winnings: Dict[str, int] = {}
        for pot in pots:
            # Find best hand among eligible players
            eligible_hands = {
                pid: player_hands[pid]
                for pid in pot.eligible_players
                if pid in player_hands
            }
            
            if not eligible_hands:
                continue
            
            # Find winners (may be multiple in case of tie)
            best_rank = max(hand[0] for hand in eligible_hands.values())
            best_hands = {
                pid: hand for pid, hand in eligible_hands.items()
                if hand[0] == best_rank
            }
            
            if len(best_hands) == 1:
                winners = list(best_hands.keys())
            else:
                # Compare tiebreakers
                best_tiebreaker = max(hand[1] for hand in best_hands.values())
                winners = [
                    pid for pid, hand in best_hands.items()
                    if hand[1] == best_tiebreaker
                ]
            
            # Distribute pot
            amount_per_winner = pot.amount // len(winners)
            for winner_id in winners:
                winnings[winner_id] = winnings.get(winner_id, 0) + amount_per_winner
        
        self._record_hand_summary(player_hands, winnings, pots)

        # Update player stacks after recording summary
        for player in self.players:
            if player.id in winnings:
                player.stack += winnings[player.id]
            player.total_bet = 0
            player.current_bet = 0
        
        return winnings

    def _record_hand_summary(self, player_hands, winnings, pots):
        """Record summary of completed hand"""
        total_pot = sum(p.amount for p in pots)
        players_summary = []
        for player in self.players:
            rank_desc = ""
            if player.id in player_hands:
                rank_desc = HandEvaluator.hand_description(*player_hands[player.id])
            starting_stack = self.hand_starting_stacks.get(player.id, player.stack)
            ending_stack = player.stack + winnings.get(player.id, 0)
            result = ending_stack - starting_stack
            players_summary.append({
                "player_id": player.id,
                "player_name": player.name,
                "cards": [str(c) for c in player.cards],
                "hand": rank_desc,
                "result": result,
                "stack_start": starting_stack,
                "stack_end": ending_stack,
                "total_bet": player.total_bet
            })
        
        winners_summary = [
            {
                "player_id": pid,
                "player_name": next((p.name for p in self.players if p.id == pid), pid),
                "amount": amount
            }
            for pid, amount in winnings.items()
        ]
        
        hand_summary = {
            "hand_number": self.hand_number,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "board": [str(c) for c in self.community_cards],
            "pot": total_pot,
            "winners": winners_summary,
            "players": players_summary,
            "actions": self.current_hand_log.copy()
        }
        
        self.hand_history.append(hand_summary)
        if len(self.hand_history) > 20:
            self.hand_history.pop(0)

    def _commit_chips(self, player: GamePlayer, amount: int) -> int:
        """Commit chips from a player's stack to the pot"""
        if amount <= 0 or player.stack <= 0:
            return 0
        committed = min(amount, player.stack)
        player.current_bet += committed
        player.total_bet += committed
        player.stack -= committed
        if player.stack == 0:
            player.all_in = True
        return committed
    
    def _next_player_with_stack(self, start_index: int) -> int:
        """Find the next player after start_index who has chips"""
        total_players = len(self.players)
        for offset in range(1, total_players + 1):
            idx = (start_index + offset) % total_players
            if self.players[idx].stack > 0:
                return idx
        raise ValueError("No players with chips remaining")
    
    def _advance_dealer_button(self) -> None:
        """Move dealer button to next player with chips"""
        self.dealer_position = self._next_player_with_stack(self.dealer_position)

