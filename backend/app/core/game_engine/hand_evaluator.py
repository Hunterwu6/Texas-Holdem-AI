"""Hand evaluation for poker hands"""
from enum import IntEnum
from typing import List, Tuple, Dict
from collections import Counter
from .deck import Card


class HandRank(IntEnum):
    """Poker hand rankings"""
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


class HandEvaluator:
    """Evaluates poker hands"""
    
    @staticmethod
    def evaluate(cards: List[Card]) -> Tuple[HandRank, List[int]]:
        """
        Evaluate a poker hand (5-7 cards)
        Returns (hand_rank, tiebreaker_values)
        """
        if len(cards) == 7:
            # For 7 cards, find best 5-card combination
            return HandEvaluator._best_five_from_seven(cards)
        elif len(cards) == 5:
            return HandEvaluator._evaluate_five(cards)
        else:
            raise ValueError(f"Must evaluate 5 or 7 cards, got {len(cards)}")
    
    @staticmethod
    def _best_five_from_seven(cards: List[Card]) -> Tuple[HandRank, List[int]]:
        """Find the best 5-card hand from 7 cards"""
        from itertools import combinations
        
        best_rank = HandRank.HIGH_CARD
        best_tiebreaker = []
        
        # Check all 21 combinations of 5 cards from 7
        for five_cards in combinations(cards, 5):
            rank, tiebreaker = HandEvaluator._evaluate_five(list(five_cards))
            if rank > best_rank or (rank == best_rank and tiebreaker > best_tiebreaker):
                best_rank = rank
                best_tiebreaker = tiebreaker
        
        return best_rank, best_tiebreaker
    
    @staticmethod
    def _evaluate_five(cards: List[Card]) -> Tuple[HandRank, List[int]]:
        """Evaluate exactly 5 cards"""
        values = sorted([c.value for c in cards], reverse=True)
        suits = [c.suit for c in cards]
        value_counts = Counter(values)
        
        is_flush = len(set(suits)) == 1
        is_straight = HandEvaluator._is_straight(values)
        
        # Count pairs, three of a kind, etc.
        counts = sorted(value_counts.values(), reverse=True)
        
        # Royal Flush
        if is_flush and is_straight and values[0] == 14:  # Ace high
            return HandRank.ROYAL_FLUSH, values
        
        # Straight Flush
        if is_flush and is_straight:
            return HandRank.STRAIGHT_FLUSH, values
        
        # Four of a Kind
        if counts == [4, 1]:
            quads = [v for v, c in value_counts.items() if c == 4][0]
            kicker = [v for v, c in value_counts.items() if c == 1][0]
            return HandRank.FOUR_OF_A_KIND, [quads, kicker]
        
        # Full House
        if counts == [3, 2]:
            trips = [v for v, c in value_counts.items() if c == 3][0]
            pair = [v for v, c in value_counts.items() if c == 2][0]
            return HandRank.FULL_HOUSE, [trips, pair]
        
        # Flush
        if is_flush:
            return HandRank.FLUSH, values
        
        # Straight
        if is_straight:
            return HandRank.STRAIGHT, values
        
        # Three of a Kind
        if counts == [3, 1, 1]:
            trips = [v for v, c in value_counts.items() if c == 3][0]
            kickers = sorted([v for v, c in value_counts.items() if c == 1], reverse=True)
            return HandRank.THREE_OF_A_KIND, [trips] + kickers
        
        # Two Pair
        if counts == [2, 2, 1]:
            pairs = sorted([v for v, c in value_counts.items() if c == 2], reverse=True)
            kicker = [v for v, c in value_counts.items() if c == 1][0]
            return HandRank.TWO_PAIR, pairs + [kicker]
        
        # One Pair
        if counts == [2, 1, 1, 1]:
            pair = [v for v, c in value_counts.items() if c == 2][0]
            kickers = sorted([v for v, c in value_counts.items() if c == 1], reverse=True)
            return HandRank.ONE_PAIR, [pair] + kickers
        
        # High Card
        return HandRank.HIGH_CARD, values
    
    @staticmethod
    def _is_straight(values: List[int]) -> bool:
        """Check if values form a straight"""
        sorted_values = sorted(set(values))
        
        # Check regular straight
        if len(sorted_values) == 5:
            if sorted_values[-1] - sorted_values[0] == 4:
                return True
        
        # Check for A-2-3-4-5 (wheel)
        if sorted_values == [2, 3, 4, 5, 14]:
            return True
        
        return False
    
    @staticmethod
    def compare_hands(
        hand1: List[Card],
        hand2: List[Card]
    ) -> int:
        """
        Compare two hands
        Returns: 1 if hand1 wins, -1 if hand2 wins, 0 if tie
        """
        rank1, tiebreaker1 = HandEvaluator.evaluate(hand1)
        rank2, tiebreaker2 = HandEvaluator.evaluate(hand2)
        
        if rank1 > rank2:
            return 1
        elif rank1 < rank2:
            return -1
        else:
            # Same rank, compare tiebreakers
            if tiebreaker1 > tiebreaker2:
                return 1
            elif tiebreaker1 < tiebreaker2:
                return -1
            else:
                return 0
    
    @staticmethod
    def hand_description(rank: HandRank, tiebreaker: List[int]) -> str:
        """Get human-readable description of hand"""
        rank_names = {
            2: "Two", 3: "Three", 4: "Four", 5: "Five",
            6: "Six", 7: "Seven", 8: "Eight", 9: "Nine",
            10: "Ten", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"
        }
        
        if rank == HandRank.ROYAL_FLUSH:
            return "Royal Flush"
        elif rank == HandRank.STRAIGHT_FLUSH:
            return f"Straight Flush, {rank_names[tiebreaker[0]]} high"
        elif rank == HandRank.FOUR_OF_A_KIND:
            return f"Four of a Kind, {rank_names[tiebreaker[0]]}s"
        elif rank == HandRank.FULL_HOUSE:
            return f"Full House, {rank_names[tiebreaker[0]]}s over {rank_names[tiebreaker[1]]}s"
        elif rank == HandRank.FLUSH:
            return f"Flush, {rank_names[tiebreaker[0]]} high"
        elif rank == HandRank.STRAIGHT:
            return f"Straight, {rank_names[tiebreaker[0]]} high"
        elif rank == HandRank.THREE_OF_A_KIND:
            return f"Three of a Kind, {rank_names[tiebreaker[0]]}s"
        elif rank == HandRank.TWO_PAIR:
            return f"Two Pair, {rank_names[tiebreaker[0]]}s and {rank_names[tiebreaker[1]]}s"
        elif rank == HandRank.ONE_PAIR:
            return f"Pair of {rank_names[tiebreaker[0]]}s"
        else:
            return f"High Card, {rank_names[tiebreaker[0]]}"

