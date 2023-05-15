from .bonus import Bonus

class Noble:
    def __init__(
        self, id: int, score: int,  bonus: Bonus
    ) -> None:
        self.id: int = id
        self.score: int = score
        self.bonus: Bonus = bonus
