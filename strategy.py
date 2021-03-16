"""Strategy."""
from abc import abstractmethod
from GameOfBlackjack.game_view import GameView, Move
from random import choice


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


def generate_pack(deck_count):
    """Generate backup pile."""
    card_pile = []
    suits = {"S": "SPADES", "D": 'DIAMONDS', 'H': 'HEARTS', 'C': 'CLUBS'}
    values = {"J": "JACK", "Q": "QUEEN", "K": "KING", "A": "ACE", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6",
              "7": "7", "8": "8", "9": "9", "0": "10"}
    codes = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '0S', 'JS', 'QS', 'KS', 'AD', '2D', '3D', '4D',
             '5D', '6D', '7D', '8D', '9D', '0D', 'JD', 'QD', 'KD', 'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C',
             '9C', '0C', 'JC', 'QC', 'KC', 'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '0H', 'JH', 'QH',
             'KH']
    for times in range(deck_count):
        for code in codes:
            suit = suits[code[-1]]
            value = values[code[0]]
            card = Card(value, suit, code)
            card_pile.append(card)
    return card_pile


class Strategy:
    """Strategy."""

    def __init__(self, other_players: list, house, decks_count: int):
        """Init."""
        self.player = None
        self.house = house
        self.decks_count = decks_count
        self.other_players = other_players

    @abstractmethod
    def on_card_drawn(self, card) -> None:
        """Called every time when card is drawn."""

    @abstractmethod
    def play_move(self, hand) -> Move:
        """Play move."""

    @abstractmethod
    def on_game_end(self) -> None:
        """Called on game end."""



class Karmoai(Strategy):
    """Very simple strategy."""

    def __init__(self, other_players: list, house, decks_count):
        """Init."""
        super().__init__(other_players, house, decks_count)
        self.used_cards = []
        self.card_pack = generate_pack(decks_count)
        one_soft = {12: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 13: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 14: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 15: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],16: ['H', 'S', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 17: ['D', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'], 18: ['S', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'S'], 19: ['S', 'S', 'S', 'S', 'D', 'S', 'S', 'S', 'S', 'S']}
        one_hard = {4: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'], 5: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'], 6: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'], 7: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'], 8: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 9: ['D', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'], 11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'], 12: ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], 13: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], 14: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], 15: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], 16: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'Q', 'Q'], 17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 18: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 21: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']}
        one_split = {"2": ['X', 'X', 'X', 'X', 'X', 'X', 'H', 'H', 'H', 'H'], "3": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'H', 'H', 'H'], "4": ['H', 'H', 'X', 'X', 'X', 'H', 'H', 'H', 'H', 'H'], "5": ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'], "6": ['X', 'X', 'X', 'X', 'X', 'X', 'H', 'H', 'H', 'H'], "7": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'H', 'Q', 'H'],  "8": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], "9": ['X', 'X', 'X', 'X', 'X', 'S', 'X', 'X', 'S', 'S'], "1": ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  "J": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], "Q": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], "K": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],  "A": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']}
        two_soft = {12: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 13: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  14: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  15: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 16: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 17: ['H', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'], 18: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']}
        two_hard = {4: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'], 5: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  6: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  7: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'], 8: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 9: ['D', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'], 11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],  12: ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  13: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], 14: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], 15: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'Q', 'H'], 16: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'Q', 'Q'], 17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 18: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 21: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']}
        two_split = {"2": ['X', 'X', 'X', 'X', 'X', 'X', 'H', 'H', 'H', 'H'], "3": ['X', 'X', 'X', 'X', 'X', 'X', 'H', 'H', 'H', 'H'], "4": ['H', 'H', 'H', 'X', 'X', 'H', 'H', 'H', 'H', 'H'],  "5": ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'], "6": ['X', 'X', 'X', 'X', 'X', 'X', 'H', 'H', 'H', 'H'], "7": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'H', 'Q', 'H'], "8": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], "9": ['X', 'X', 'X', 'X', 'X', 'S', 'X', 'X', 'S', 'S'],  "1": ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], "J": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], "Q": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], "K": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], "A": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']}
        else_soft = {12: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'], 13: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 14: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  15: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 16: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 17: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  18: ['S', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'],  19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']}
        else_hard = {4: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'], 5: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'], 6: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'], 7: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'], 8: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 9: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], 10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'], 11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'], 12: ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], 13: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], 14: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'], 15: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'Q', 'H'], 16: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'Q', 'Q', 'Q'], 17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 18: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], 21: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']}
        else_split = {"2": ['X', 'X', 'X', 'X', 'X', 'X', 'H', 'H', 'H', 'H'],  "3": ['X', 'X', 'X', 'X', 'X', 'X', 'H', 'H', 'H', 'H'], "4": ['H', 'H', 'H', 'X', 'X', 'H', 'H', 'H', 'H', 'H'],  "5": ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],  "6": ['X', 'X', 'X', 'X', 'X', 'H', 'H', 'H', 'H', 'H'],  "7": ['X', 'X', 'X', 'X', 'X', 'X', 'H', 'H', 'Q', 'H'],  "8": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], "9": ['X', 'X', 'X', 'X', 'X', 'S', 'X', 'X', 'S', 'S'], "1": ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], "J": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], "Q": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],  "K": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], "A": ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']}
        if decks_count == 1:
            self.soft_hand_dict = one_soft
            self.hard_hand_dict = one_hard
            self.split_hand = one_split
        elif decks_count == 2:
            self.soft_hand_dict = two_soft
            self.hard_hand_dict = two_hard
            self.split_hand = two_split
        else:
            self.soft_hand_dict = else_soft
            self.hard_hand_dict = else_hard
            self.split_hand = else_split


    def play_move(self, hand) -> Move:
        """Get next move."""
        code = [card.__str__() for card in self.house.cards]
        house_card_value = code[0] if code[0] != "??" else code[1]
        hand_host = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7, "0": 8, "J": 8, "Q": 8, "K": 8,
                     'A': 9}
        self.host_hand_index = hand_host[house_card_value[0]]
        if hand.can_split:
            response = self.split_hand[hand.cards[0].value[0]]
        elif hand.is_soft_hand and hand.score in range(12, 20):
            response = self.soft_hand_dict[hand.score][self.host_hand_index]
        elif hand.score < 21:
            response = self.hard_hand_dict[hand.score][self.host_hand_index]
        else:
            response = "S"
        response = choice(response)
        if response == "H":
            return Move.HIT
        if response == "D":
            return Move.DOUBLE_DOWN
        if response == "Q":
            return Move.SURRENDER
        if response == "S":
            return Move.STAND
        if response == "X":
            return Move.SPLIT

    def on_card_drawn(self, card) -> None:
        """Called every time card is drawn."""
        self.used_cards.append(card)
        if card in self.card_pack:
            self.card_pack.remove(card)

    def on_game_end(self) -> None:
        """Called on game end."""
        self.used_cards = []

class HumanStrategy(Strategy):
    """Human strategy."""

    def __init__(self, other_players: list, house, decks_count, view: GameView):
        """Init."""
        super().__init__(other_players, house, decks_count)
        self.view = view

    def play_move(self, hand) -> Move:
        """Play move."""
        return self.view.ask_move()

    def on_card_drawn(self, card) -> None:
        """Called every time card is drawn."""

    def on_game_end(self) -> None:
        """Called on game end."""