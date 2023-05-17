from .bonus import Bonus
from .resource import Resource,Token


class DevelopmentCard:
    def __init__(
        self, level: int, id: int, score: int, cost: Resource, bonus: Bonus
    ) -> None:
        self.id: int = id
        self.level: int = level
        self.score: int = score
        self.cost: Resource = cost
        self.bonus: Token = bonus
