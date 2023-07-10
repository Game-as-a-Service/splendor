from .bonus import Bonus
import random

class Noble:
    def __init__(self, id: int = 0, score: int = 0, bonus: Bonus = None):
        self.id: int = id
        self.score: int = score
        self.bonus: Bonus = bonus
        
    
def get_noble(players: int):
    nobles:list[Noble]=[
        Noble(1, 3, Bonus(3, 0, 0, 3, 3)),
        Noble(2, 3, Bonus(0, 0, 0, 4, 4)),
        Noble(3, 3, Bonus(4, 0, 0, 0, 4)),
        Noble(4, 3, Bonus(4, 0, 4, 0, 0)),
        Noble(5, 3, Bonus(0, 4, 4, 0, 0)),
        Noble(6, 3, Bonus(0, 3, 3, 3, 0)),
        Noble(7, 3, Bonus(0, 3, 0, 3, 3)),
        Noble(8, 3, Bonus(3, 0, 3, 0, 4)),
        Noble(9, 3, Bonus(0, 4, 0, 4, 0)),
        Noble(10, 3, Bonus(3, 3, 3, 0, 0))]
    noble = random.sample(nobles, players + 1)
    return noble