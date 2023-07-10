from .bonus import Bonus
from .resource import Resource,Token
from .dbmodels

class DevelopmentCard:
    def __init__(self) -> None:
        self.id: int 
        self.level: int 
        self.score: int 
        self.cost: Resource
        self.bonus: Token

    def get_development_card():
        # 查

        cards = [
            DevelopmentCard(1)
        ]
