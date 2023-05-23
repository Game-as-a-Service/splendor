from domain import Bonus

class BonusUserCase:
    def __init__(self,diamond:int=0, sapphire:int=0, emerald:int=0, ruby:int=0, onyx:int=0,bonus:Bonus=None)->None:
        self.diamond =diamond
        self.sapphire =sapphire
        self.emerald =emerald 
        self.ruby =ruby
        self.onyx =onyx
        if bonus:
            self.domain_to_usercase(bonus)
        
    def domain_to_usercase(self,bonus:Bonus)->None:
        self.diamond = bonus.diamond
        self.sapphire = bonus.sapphire
        self.emerald = bonus.emerald
        self.ruby = bonus.ruby
        self.onyx = bonus.onyx
    
    def usercase_to_domain(self)->Bonus:
        return Bonus(self.diamond,self.sapphire,self.emerald,self.ruby,self.onyx)

    @classmethod
    def to_usercase(cls,diamond:int, sapphire:int, emerald:int, ruby:int, onyx:int)->"BonusUserCase":
        return cls(diamond,sapphire,emerald,ruby,onyx)