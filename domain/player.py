from .bonus import Bonus
from .card import DevelopmentCard
from .resource import Resource, Token
from .noble import Noble
from .table import Table


class Player:
    def __init__(self):
        self.score: int = 0
        self.resource: Resource = Resource()
        self.development_cards: list[DevelopmentCard] = []
        self.reserveDevelopmentCards: list[DevelopmentCard] = []
        self.bonus: Bonus = Bonus()
        self.nobles: list[Noble] = []

    def get_token(self, resource: Resource, table: Table):
        for token in resource.token:
            try:
                table.resource.token.remove(Token.__getitem__(token.name))
            except ValueError as e:
                e.add_note
                raise ValueError(f"There is no {token.name} to get.")
            table.resource.__setattr__(
                token.name,
                int(table.resource.__getattribute__(token.name)) - 1,
            )
            self.resource.token.append(token)
            self.resource.__setattr__(
                token.name, self.resource.__getattribute__(token.name) + 1
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
