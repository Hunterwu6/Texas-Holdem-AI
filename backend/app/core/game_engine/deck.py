"""Deck and Card management"""
import random
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Card:
    """Represents a playing card"""
    rank: str  # '2'-'9', 'T', 'J', 'Q', 'K', 'A'
    suit: str  # 's', 'h', 'd', 'c'
    
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    SUITS = ['s', 'h', 'd', 'c']  # spades, hearts, diamonds, clubs
    RANK_VALUES = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    
    def __str__(self) -> str:
        """String representation e.g., 'As' for Ace of Spades"""
        return f"{self.rank}{self.suit}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self) -> int:
        return hash((self.rank, self.suit))
    
    @property
    def value(self) -> int:
        """Numeric value of the card"""
        return self.RANK_VALUES[self.rank]
    
    @classmethod
    def from_string(cls, card_str: str) -> "Card":
        """Create card from string like 'As' or 'Kh'"""
        if len(card_str) != 2:
            raise ValueError(f"Invalid card string: {card_str}")
        rank, suit = card_str[0], card_str[1]
        if rank not in cls.RANKS or suit not in cls.SUITS:
            raise ValueError(f"Invalid card: {card_str}")
        return cls(rank=rank, suit=suit)


class Deck:
    """Standard 52-card deck"""
    
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()
    
    def reset(self) -> None:
        """Reset deck to full 52 cards"""
        self.cards = [
            Card(rank=rank, suit=suit)
            for suit in Card.SUITS
            for rank in Card.RANKS
        ]
    
    def shuffle(self) -> None:
        """Shuffle the deck using Fisher-Yates algorithm"""
        random.shuffle(self.cards)
    
    def deal(self, num_cards: int = 1) -> List[Card]:
        """Deal specified number of cards from the deck"""
        if num_cards > len(self.cards):
            raise ValueError(f"Cannot deal {num_cards} cards, only {len(self.cards)} remaining")
        
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards
    
    def deal_one(self) -> Optional[Card]:
        """Deal a single card"""
        if not self.cards:
            return None
        return self.deal(1)[0]
    
    def burn(self) -> Optional[Card]:
        """Burn a card (deal and discard)"""
        return self.deal_one()
    
    def remaining(self) -> int:
        """Number of cards remaining in deck"""
        return len(self.cards)
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __str__(self) -> str:
        return f"Deck({len(self.cards)} cards remaining)"

