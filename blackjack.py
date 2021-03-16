"""Blackjack."""
import importlib
import os
import pkgutil
from GameOfBlackjack.game_view import GameView, FancyView, Move
from student_strategy import Strategy, HumanStrategy, NotSoDumbAI
from GameOfBlackjack.deck import Deck, Card


class Hand:
    """Hand."""

    def __init__(self, cards: list = None):
        """Init."""
        self.cards = [] if cards is None else cards
        self.is_double_down, self.is_surrendered = False, False

    def add_card(self, card: Card) -> None:
        """Add card to hand."""
        self.cards.append(card)

    def double_down(self, card: Card) -> None:
        """Double down."""
        self.add_card(card)
        self.is_double_down = True

    def split(self):
        """Split hand."""
        if self.can_split:
            new_hand = self.cards[:1]
            self.cards = self.cards[1:]
            return Hand(new_hand)
        raise ValueError("Invalid hand to split!")

    @property
    def can_split(self) -> bool:
        """Check if hand can be split."""
        if len(self.cards) == 2 and self.cards[0].value == self.cards[1].value:
            return True
        return False

    @property
    def is_blackjack(self) -> bool:
        """Check if is blackjack."""
        return True if len(self.cards) == 2 and self.is_soft_hand and {card.value for card in self.cards} & {"JACK",
                                                                                                             "10",
                                                                                                             "QUEEN",
                                                                                                             "KING"} else False

    @property
    def is_soft_hand(self):
        """Check if is soft hand."""
        return True if "ACE" in [card.value for card in self.cards] else False

    @property
    def score(self) -> int:
        """Get score of hand."""
        score = 0
        ace_score = 0
        for value in [card.value for card in self.cards]:
            if value.isdigit():
                score += int(value)
            else:
                if value != "ACE":
                    score += 10
                else:
                    ace_score += 11
        aces_in_hand = ace_score // 11
        for x in range(aces_in_hand):
            if score + ace_score < 22:
                return score + ace_score
            ace_score -= 10
        return score + ace_score


class Player:
    """Player."""

    def __init__(self, name: str, strategy: Strategy, coins: int = 100):
        """Init."""
        self.name = name
        self.strategy = strategy
        self.coins = coins
        self.hands = []

    def join_table(self):
        """Join table."""
        self.hands.append(Hand())

    def play_move(self, hand: Hand) -> Move:
        """Play move."""
        return self.strategy.play_move(hand)

    def split_hand(self, hand: Hand) -> None:
        """Split hand."""
        try:
            self.hands.append(hand.split())
        except ValueError:
            pass


class GameController:
    """Game controller."""

    PLAYER_START_COINS = 200
    BUY_IN_COST = 5

    def __init__(self, view: GameView):
        """Init."""
        self.deck_ammount = view.ask_decks_count()
        self.view = view
        self.house = Hand()
        self.players = []
        self.deck = None
        self.playing_players = []
        self.playing = True

    def start_game(self) -> None:
        """Start game."""
        self.house = Hand()
        player_count = 0
        human_names = []
        bot_names = []
        players_amount = self.view.ask_players_count()
        for num in range(players_amount):
            human_names.append(self.view.ask_name(player_count))
            player_count += 1
        bots_amount = self.view.ask_bots_count()
        for num in range(bots_amount):
            bot_names.append(self.view.ask_name(player_count))
            player_count += 1
        self.deck = Deck(self.deck_ammount, True)
        self.players = [Player(name, HumanStrategy(self.players, self.house, self.deck_ammount, self.view),
                               GameController.PLAYER_START_COINS) for name in human_names]
        for ind, name in enumerate(bot_names):
            self.players.append(Player(name, NotSoDumbAI(self.players, self.house, self.deck_ammount),
                                           GameController.PLAYER_START_COINS))


    def play_round(self) -> None:
        """Play round."""
        for player in self.playing_players:
            player.hands = []
        self.playing_players = []
        self.house = Hand()
        self.give_players_cards()

        # Play the game Blackjack.
        self.play_blackjack()
        self.house.cards[0].top_down = False

        while True:
            if self.house.score < 17 or self.house.is_soft_hand and self.house.score < 18:
                self.house.add_card(self._draw_card())
            else:
                break
        # Give money to suitable players.
        self.give_money_to_players()
        if self.playing:
            FancyView.show_table(self.view, self.playing_players, self.house, self.house)
        print(f"Buy in coset: {GameController.BUY_IN_COST}")

    def give_players_cards(self):
        for player in self.players:
            if player.coins >= GameController.BUY_IN_COST:
                player.coins -= GameController.BUY_IN_COST
                player.hands.append(Hand([self._draw_card()]))
                self.playing_players.append(player)
        for counter in range(2):
            for player in self.playing_players:
                if counter:
                    player.hands[0].add_card(self._draw_card())
            house_card = self._draw_card()
            if not counter:
                house_card.top_down = True
            self.house.add_card(house_card)

    def play_blackjack(self):
        """Play blackjack with the players."""
        GameController.BUY_IN_COST += 1
        for player in self.playing_players:
            hand_index = -1
            player.strategy.house = self.house
            for hand in player.hands:
                hand_index += 1
                while True:
                    if hand.score > 21 or hand.is_blackjack:
                        break
                    if self.playing:
                        FancyView.show_table(self.view, self.playing_players, self.house, hand)
                    move = player.play_move(hand)
                    if move == Move.HIT:
                        hand.add_card(self._draw_card())
                    if move == Move.SPLIT and hand.can_split:
                        if player.coins < GameController.BUY_IN_COST:
                            hand.add_card(self._draw_card())
                        else:
                            player.coins -= GameController.BUY_IN_COST
                            player.split_hand(hand)
                            player.hands[hand_index].add_card(self._draw_card())
                            player.hands[-1].add_card(self._draw_card())
                    if move == Move.DOUBLE_DOWN:
                        if player.coins < GameController.BUY_IN_COST:
                            hand.add_card(self._draw_card())
                            break
                        player.coins -= GameController.BUY_IN_COST
                        hand.double_down(self._draw_card())
                        break
                    if move == Move.SURRENDER:
                        hand.is_surrendered = True
                        break
                    if move == Move.STAND:
                        break
            player.strategy.on_game_end()
    def give_money_to_players(self):
        """People get their money."""
        for player in self.playing_players:
            for hand in player.hands:
                modifier = 1
                if hand.is_double_down:
                    modifier = 2
                if hand.is_blackjack and not self.house.is_blackjack:
                    player.coins += GameController.BUY_IN_COST * 2.5
                elif hand.is_surrendered:
                    player.coins += GameController.BUY_IN_COST * 0.5
                elif hand.score > 21:
                    pass
                elif self.house.score > 21:
                    player.coins += GameController.BUY_IN_COST * 2 * modifier
                elif hand.score > self.house.score:
                    player.coins += GameController.BUY_IN_COST * 2 * modifier
                elif hand.score == self.house.score:
                    player.coins += GameController.BUY_IN_COST * modifier

    def _draw_card(self) -> Card:
        """Draw card."""
        card = self.deck.draw_card()
        for player in self.players:
            player.strategy.on_card_drawn(card)
        if self.deck.remaining == 0:
            self.deck = Deck(self.deck_ammount, True)
        return self.deck.draw_card()

    @staticmethod
    def load_strategies() -> list:
        """Load strategies."""
        pkg_dir = os.path.dirname(__file__)
        for (module_loader, name, is_pkg) in pkgutil.iter_modules([pkg_dir]):
            importlib.import_module('.' + name, 'ex13_blackjack')
        return list(filter(lambda x: x.__name__ != HumanStrategy.__name__, Strategy.__subclasses__()))


if __name__ == '__main__':
    game_controller = GameController(FancyView())
    game_controller.start_game()
    while True:
        game_controller.play_round()
