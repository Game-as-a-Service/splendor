from .bonus import Bonus
from .card import DevelopmentCard
from .resource import Resource, Token
from .noble import Noble


class Player:
    def __init__(self, game):
        from .game import Game

        self.game: Game = game
        self.score: int = 0
        self.resource: Resource = Resource()
        self.development_cards: list[DevelopmentCard] = []
        self.reserveDevelopmentCards: list[DevelopmentCard] = []
        self.bonus: Bonus = Bonus()
        self.nobles: list[Noble] = []

    def get_token(self, resource: Resource):
        for token in resource.token:
            self.resource.token.append(token)
            self.resource.__setattr__(
                token.name, self.resource.__getattribute__(token.name) + 1
            )
            self.game.table.resource.token.remove(Token.__getitem__(token.name))
            self.game.table.resource.__setattr__(
                token.name,
                int(self.game.table.resource.__getattribute__(token.name)) - 1,
            )

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
