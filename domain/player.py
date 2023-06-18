from .bonus import Bonus
from .card import DevelopmentCard
from .resource import Resource, Token
from .noble import Noble


class Player:
    def __init__(self):
        self.score: int = 0
        self.resource: Resource = Resource()
        self.development_cards: list[DevelopmentCard] = []
        self.reserve_development_cards: list[DevelopmentCard] = []
        self.bonus: Bonus = Bonus()
        self.nobles: list[Noble] = []

    def get_token(self, resource: Resource) -> None:
        pass

    def buy_development_card(self, cost: Resource, card: DevelopmentCard) -> None:
        pass
    
    def choose_resource(
            self,
            diamond: int = 0,
            emerald: int = 0,
            ruby:int = 0,
            onyx:int = 0,
            sapphire: int = 0,
            gold:int = 0,
            ) -> Resource:
        resource = Resource()
        resource.diamond += diamond
        resource.emerald += emerald
        resource.ruby += ruby
        resource.onyx += onyx
        resource.sapphire += sapphire
        resource.gold += gold
        return resource
    
    def buy_development_card_from_reserve(self, cost: Resource, card: DevelopmentCard) -> None:
        # 扣除花費的resource
        self.resource.diamond -= cost.diamond
        self.resource.emerald -= cost.emerald
        self.resource.ruby -= cost.ruby
        self.resource.onyx -= cost.onyx
        self.resource.sapphire -= cost.sapphire
        self.resource.gold -= cost.gold
        # 手上保留中轉移至手上發展卡
        self.reserve_development_cards.remove(card)
        self.development_cards.append(card)
        # bonus 加上去
        self.bonus.diamond += card.bonus.diamond
        self.bonus.emerald += card.bonus.emerald
        self.bonus.sapphire += card.bonus.sapphire
        self.bonus.ruby += card.bonus.ruby
        self.bonus.onyx += card.bonus.onyx

    def reserve_development_card(self, card: DevelopmentCard) -> None:
        pass

    def gain_permanent_token() -> None:
        pass

    def gain_score() -> None:
        pass

    def gain_noble() -> None:
        pass
