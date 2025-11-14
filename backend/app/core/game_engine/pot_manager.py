"""Pot and side pot calculation"""
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Player:
    """Simple player for pot calculation"""
    id: str
    bet: int
    stack: int
    folded: bool = False
    
    @property
    def total_invested(self) -> int:
        return self.bet


@dataclass
class Pot:
    """Represents a pot (main or side)"""
    amount: int
    eligible_players: List[str]  # player IDs
    
    def __str__(self) -> str:
        return f"Pot(${self.amount}, {len(self.eligible_players)} players)"


class PotManager:
    """Manages pot calculation including side pots"""
    
    @staticmethod
    def calculate_pots(players: List[Player]) -> List[Pot]:
        """
        Calculate main pot and side pots
        Returns list of pots in order (main pot first)
        """
        # Only consider players who have contributed chips
        contributing_players = [p for p in players if p.bet > 0]
        
        if not contributing_players:
            return []
        
        pots: List[Pot] = []
        remaining_bets: Dict[str, int] = {p.id: p.bet for p in contributing_players}
        player_lookup: Dict[str, Player] = {p.id: p for p in players}
        
        while any(bet > 0 for bet in remaining_bets.values()):
            # Find minimum non-zero bet
            min_bet = min(bet for bet in remaining_bets.values() if bet > 0)
            
            # Players eligible for this pot (those who contributed)
            contributing_ids = [pid for pid, bet in remaining_bets.items() if bet > 0]
            
            # Calculate pot amount
            pot_amount = min_bet * len(contributing_ids)
            
            # Only non-folded players can win this pot
            eligible_player_ids = [
                pid for pid in contributing_ids
                if not player_lookup.get(pid, Player(pid, 0, 0, True)).folded
            ]
            
            # Create pot
            pots.append(Pot(
                amount=pot_amount,
                eligible_players=eligible_player_ids
            ))
            
            # Subtract from remaining bets
            for pid in contributing_ids:
                remaining_bets[pid] -= min_bet
        
        return pots
    
    @staticmethod
    def distribute_pot(
        pot: Pot,
        winners: List[str],  # player IDs who won
        all_players: Dict[str, Player]
    ) -> Dict[str, int]:
        """
        Distribute a pot to winners
        Returns dict of player_id -> amount_won
        """
        # Filter winners to only eligible players
        eligible_winners = [
            w for w in winners if w in pot.eligible_players
        ]
        
        if not eligible_winners:
            # No eligible winners, pot goes to next hand (rare edge case)
            return {}
        
        # Split pot equally among winners
        amount_per_winner = pot.amount // len(eligible_winners)
        remainder = pot.amount % len(eligible_winners)
        
        result: Dict[str, int] = {}
        for i, winner_id in enumerate(eligible_winners):
            result[winner_id] = amount_per_winner
            # Give remainder to first winner(s)
            if i < remainder:
                result[winner_id] += 1
        
        return result
    
    @staticmethod
    def distribute_all_pots(
        pots: List[Pot],
        winners_by_pot: List[List[str]],  # Winners for each pot
        all_players: Dict[str, Player]
    ) -> Dict[str, int]:
        """
        Distribute all pots to winners
        Returns total amount won by each player
        """
        total_winnings: Dict[str, int] = {}
        
        for pot, winners in zip(pots, winners_by_pot):
            pot_distribution = PotManager.distribute_pot(pot, winners, all_players)
            
            for player_id, amount in pot_distribution.items():
                total_winnings[player_id] = total_winnings.get(player_id, 0) + amount
        
        return total_winnings
    
    @staticmethod
    def calculate_total_pot(players: List[Player]) -> int:
        """Calculate total pot amount"""
        return sum(p.bet for p in players)

