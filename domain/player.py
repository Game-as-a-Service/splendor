from .bonus import Bonus
from .card import DevelopmentCard
from .resource import Resource, Token


class Player:
    def __init__(self):
        self.score: int = 0
        self.resource: Resource = Resource()
        self.development_cards: list[DevelopmentCard] = []
        self.bonus: Bonus = Bonus()

    def buy_development_card(self, cost: "Resource", card: "DevelopmentCard"):
        self.score += card.score
        self.development_cards.append(card)
        self.resource.花錢(card.cost)
        self.bonus.獲得(card.bonus)


p = Player()

p.resource.存錢(Token.onyx)
p.resource.存錢(Token.onyx)
p.resource.存錢(Token.onyx)
p.resource.存錢(Token.onyx)
print(p.resource.onyx)
