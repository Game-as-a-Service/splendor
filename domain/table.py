from .noble import Noble
from .developmentcard import Developmentcard
from .resource import Resource
class Table:
    def __init__(self):
        self.noble:list[Noble]=[]
        self.deck1:list[Developmentcard]=Developmentcard().getlevel1()
        self.deck2:list[Developmentcard]=Developmentcard().getlevel2()
        self.deck3:list[Developmentcard]=Developmentcard().getlevel3()
        self.card1:list[Developmentcard]=[]
        self.card2:list[Developmentcard]=[]
        self.card3:list[Developmentcard]=[]
        self.resoure:Resource=Resource()
        self.deck: int