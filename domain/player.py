
from .bonus import Bonus
from .card import DevelopmentCard
from .resource import Resource, Token
from .noble import Noble


class Player:
    def __init__(self):
        self.score: int = 0
        self.resource: Resource = Resource()
        self.development_cards: list[DevelopmentCard] = []
        self.reserveDevelopmentCards: list[DevelopmentCard] = []
        self.bonus: Bonus = Bonus()
        self.nobles:list[Noble]=[]        

    def buyDevelopmentCard(self, cost: Resource, card: DevelopmentCard):
        if self.canBuy(cost,card):
            self.score += card.score
            self.appendCard(card)
            self.resource.cost(cost)

    def getReserveDevelopmentCard(self,level:int,id:int)->DevelopmentCard:
        card =list(filter(lambda c: c.id == id and c.level ==level, self.reserveDevelopmentCards))[0]
        self.reserveDevelopmentCards.remove(card)
        return card
            
    def appendCard(self,card:DevelopmentCard):
        self.development_cards.append(card)
        self.bonus.gain(card.bonus)
        self.setScore()

    def appendNoble(self,noble:Noble):
        self.nobles.append(noble)
        self.setScore()
    
    def setScore(self):
        total=0
        for card in self.development_cards:
            total+=card.score
        for noble in self.nobles:
            total+=noble.score
        self.score =total

    def setBonus(self):
        newBonus =Bonus()
        for b in self.development_cards:
            newBonus.gain(b.bonus)
        return newBonus

    def canBuy(self,cost: Resource, card: DevelopmentCard)->bool:
        diamond = card.cost.diamond -self.bonus.diamond-cost.diamond
        ruby = card.cost.ruby -self.bonus.ruby-cost.ruby
        emerald = card.cost.emerald -self.bonus.emerald-cost.emerald
        sapphire = card.cost.sapphire -self.bonus.sapphire-cost.sapphire
        onyx = card.cost.onyx -self.bonus.onyx-cost.onyx
        diamond = 0 if diamond<=0 else diamond
        ruby = 0 if ruby<=0 else ruby
        emerald = 0 if emerald<=0 else emerald
        sapphire = 0 if sapphire<=0 else sapphire
        onyx = 0 if onyx<=0 else onyx

        if diamond+ruby+emerald+sapphire+onyx ==0:
            return True
        else:
            return False


    def to_dict(self):
        return {
            'score': self.score,
            'resource': self.resource.to_dict(),
            'development_cards': [card.to_dict() for card in self.development_cards],
            'reserveDevelopmentCards': [card.to_dict() for card in self.reserveDevelopmentCards],
            'bonus': self.bonus.__dict__,
            'nobles': [noble.to_dict() for noble in self.nobles]
        }

