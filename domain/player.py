from .bonus import Bonus
from .card import DevelopmentCard
from .resource import Resource, Token
from .noble import Noble


class Player:
    def __init__(self):
        self.score: int = 0
        self.resource: Resource = Resource()
        self.development_cards: list[DevelopmentCard] = []
        self.reserveDevelopmentCards: list[DevelopmentCard] = []
        self.bonus: Bonus = Bonus()
        self.nobles: list[Noble] = []

    def get_token(self, resource: Resource) -> None:
        pass

    def buy_development_card(self, cost: Resource, card: DevelopmentCard) -> None:
        pass

    def reserve_development_card(self, card: DevelopmentCard) -> None:
        pass

    def gain_permanent_token() -> None:
        pass

    def gain_score() -> None:
        pass

    def gain_noble() -> None:
        pass
