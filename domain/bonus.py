from .developmentcard import Developmentcard

class Bonus:
    def __init__(self) -> None:
        self.diamond: int = 0
        self.sapphire: int = 0
        self.emerald: int = 0
        self.ruby: int = 0
        self.onyx: int = 0
    
    def add_bonus(self,card:Developmentcard):
        setattr(self, card.bonus.value, getattr(self, card.bonus.value) + 1)

        #setattr(self, card.bonus, getattr(self, card.bonus) + 1)
        """
        if card.bonus=="diamond":
            self.diamond+=1
        elif card.bonus=="sapphire":
            self.sapphire+=1
        elif card.bonus=="emerald":
            self.emerald+=1
        elif card.bonus=="ruby":
            self.ruby+=1
        elif card.bonus=="onyx":
            self.onyx+=1
        """