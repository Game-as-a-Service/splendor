from .table import Table
import uuid
import random
class Game:
    def __init__(self) -> None:
        self.uuid = uuid.UUID(int=0)
        self.table: Table=Table()
        self.turn:int
        self.lastround: bool

    def startGame(self,):
        self.uuid = uuid.uuid4()
        self.turn=1
        self.lastround=False

    def draw_card1(self):
        if self.table.deck1:
            random_card = random.choice(self.table.deck1)
            self.table.deck1.remove(random_card)
            self.table.card1.append(random_card)

    def draw_card2(self):
        if self.table.deck2:
            random_card = random.choice(self.table.deck2)
            self.table.deck2.remove(random_card)
            self.table.card2.append(random_card)

    def draw_card3(self):
        if self.table.deck3:
            random_card = random.choice(self.table.deck3)
            self.table.deck3.remove(random_card)
            self.table.card3.append(random_card)