"""Deck."""
from typing import Optional, List
import requests
from random import choice, shuffle


class Card:
    """Dataclass for holding card information."""

    def __init__(self, value: str, suit: str, code: str, top_down=False):
        """Constructor."""
        self.value = value
        self.suit = suit
        self.code = code
        self.top_down = top_down

    def __str__(self):
        """Str."""
        return "??" if self.top_down else self.code

    def __repr__(self) -> str:
        """Repr."""
        return self.code

    def __eq__(self, o) -> bool:
        """Eq."""
        return isinstance(o, Card) and o.suit == self.suit and o.value == self.value


class Deck:
    """Deck."""

    DECK_BASE_API = "https://deckofcardsapi.com/api/deck/"

    def __init__(self, deck_count: int = 1, shuffle: bool = False):
        """Constructor."""
        self.deck_count = deck_count
        self.is_shuffled = shuffle
        self._backup_deck = self._generate_backup_pile()
        self.card_pack = self._request(f"{Deck.DECK_BASE_API}new/?deck_count={self.deck_count}")
        if shuffle:
            self.shuffle()

    def shuffle(self) -> None:
        """Shuffle the deck."""
        if self.is_shuffled:
            try:
                self.card_pack = requests.get(f"{Deck.DECK_BASE_API}{self.deck_id}/shuffle/")
            except KeyError:
                pass
            shuffle(self._backup_deck)

    def draw_card(self, top_down: bool = False) -> Optional[Card]:
        """Draw card from the deck."""
        if self.remaining:
            card = choice(self._backup_deck) if self.is_shuffled else self._backup_deck[0]
            self.remaining -= 1
            self._backup_deck.remove(card)
            return Card(card.value, card.suit, card.code, top_down)

    def _request(self, url: str):
        """Update deck."""
        self.deck_id = "StoneAge"
        self.remaining = len(self._backup_deck)
        self.online = False
        return self._backup_deck

    def _generate_backup_pile(self) -> List[Card]:
        """Generate backup pile."""
        card_pile = []
        suits = {"S": "SPADES", "D": 'DIAMONDS', 'H': 'HEARTS', 'C': 'CLUBS'}
        values = {"J": "JACK", "Q": "QUEEN", "K": "KING", "A": "ACE", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6",
                  "7": "7", "8": "8", "9": "9", "0": "10"}
        codes = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '0S', 'JS', 'QS', 'KS', 'AD', '2D', '3D', '4D',
                 '5D', '6D', '7D', '8D', '9D', '0D', 'JD', 'QD', 'KD', 'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C',
                 '9C', '0C', 'JC', 'QC', 'KC', 'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '0H', 'JH', 'QH',
                 'KH']
        for times in range(self.deck_count):
            for code in codes:
                suit = suits[code[-1]]
                value = values[code[0]]
                card = Card(value, suit, code)
                card_pile.append(card)
        return card_pile