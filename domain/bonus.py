from .Token import Token
from .DevelopmentCard import DevelopmentCard

class Bonus:
    def __init__(self) -> None:
        self.white = 0
        self.blue = 0
        self.green = 0
        self.red = 0
        self.black = 0

    def add_bonus(self, card: DevelopmentCard):
        if card.bonus.name == 'ruby':
            self.red += 1
        elif card.bonus.name == 'sapphire':
            self.blue += 1
        elif card.bonus.name == 'diamond':
            self.white += 1
        elif card.bonus.name == 'emerald':
            self.green += 1
        elif card.bonus.name == 'onyx':
            self.black += 1
        else:
            pass