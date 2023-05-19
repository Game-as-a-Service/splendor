from .bonus import Bonus

class Noble:
    def __init__(
        self, id: int, score: int,  bonus: Bonus
    ) -> None:
        self.id: int = id
        self.score: int = score
        self.bonus: Bonus = bonus

    def to_dict(self):
        return {
            'id': self.id,
            'score': self.score,
            'bonus': self.bonus.__dict__
        }
