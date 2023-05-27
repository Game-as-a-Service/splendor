from .Token import Token


class DevelopmentCard:
    def __init__(self, level, id, score, cost, bonus) -> None:
        self.level = level
        self.id = id
        self.score = score
        self.cost = cost
        self.bonus = bonus
    