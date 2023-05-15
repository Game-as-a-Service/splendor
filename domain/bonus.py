from .developmentcard import Developmentcard

class Bonus:
    def __init__(self) -> None:
        self.white: int = 0
        self.blue: int = 0
        self.green: int = 0
        self.red: int = 0
        self.black: int = 0
    
    def add_bonus(self,card:Developmentcard):
        bonus_color = {
            "diamond": "white",
            "sapphire": "blue",
            "emerald": "green",
            "ruby": "red",
            "onyx": "black"
        }
        bonus_type = bonus_color.get(card.bonus)
        if bonus_type:
            setattr(self, bonus_type, getattr(self, bonus_type) + 1)
        """
        if card.bonus=="diamond":
            self.white+=1
        elif card.bonus=="sapphire":
            self.blue+=1
        elif card.bonus=="emerald":
            self.green+=1
        elif card.bonus=="ruby":
            self.red+=1
        elif card.bonus=="onyx":
            self.black+=1
        """