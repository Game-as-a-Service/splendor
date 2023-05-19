from .bonus import Bonus
from .resource import Resource,Token


class DevelopmentCard:
    def __init__(
        self, level: int, id: int, score: int, cost: Resource, bonus: Token
    ) -> None:
        self.id: int = id
        self.level: int = level
        self.score: int = score
        self.cost: Resource = cost
        self.bonus: Token = bonus

    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'score': self.score,
            'cost': self.cost.to_dict_cost(),
            'bonus': self.bonus.value,
        }

