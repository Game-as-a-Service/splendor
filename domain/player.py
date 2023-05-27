from .Resource import Resource
from .Token import Token
from .DevelopmentCard import DevelopmentCard
from .Bonus import Bonus


class Player():
    def __init__(self):
        self.resource = Resource()
        self.bonus = Bonus()
        self.cards = []
        self.score = 0

    def get_token(self, token: Token):
        self.resource.add_token(token)
    
    def get_bonus(self, card: DevelopmentCard):
        self.bonus.add_bonus(card)
    
    def buy_development_card(self, card: DevelopmentCard):
        # TODO 可以供選擇
        if self.check_card_can_buy(card):
            self.cards.append(card)
            self.get_bonus(card)
            self.get_score(card)
            for x in range(card.cost.black):
                self.remove_resource(Token.onyx)
        else:
            raise KeyError

    def remove_resource(self, token):
        self.resource.remove_token(token)

    def get_score(self, card: DevelopmentCard):
        self.score += card.score

    def check_card_can_buy(self, card: DevelopmentCard):
        return self.resource.black >= card.cost.black