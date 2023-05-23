from domain import Noble
from .bonus_user_case import BonusUserCase

class NobleUserCase:
    def __init__(self,id:int, score:int, bonus:BonusUserCase,noble:Noble=None)->None:
        self.id =id
        self.score =score
        self.bonus =bonus
        if noble:
            self.domain_to_usercase(noble)
        
    def domain_to_usercase(self,noble:Noble)->None:
        self.id = noble.id
        self.score = noble.score
        self.bonus = BonusUserCase(noble.bonus)

    def user_to_domain(self)->Noble:
        return Noble(self.id,self.score,self.bonus.usercase_to_domain())

    @classmethod
    def to_usercase(cls,id:int, score:int, bonus:BonusUserCase)->"NobleUserCase":
        return cls(
            id =id,
            score=score,
            bonus = bonus,
        )

    def to_dict(self)->dict:
        return{
            "id":self.id,
            "score":self.score,
            "bonus":self.bonus.__dict__
        }