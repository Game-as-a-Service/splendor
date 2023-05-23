from enum import Enum

class Resource:
    def __init__(self,diamond:int=0, sapphire:int=0, emerald:int=0,ruby:int=0, onyx:int=0,gold:int=0) -> None:
        self.token: list[Token] = []
        self.diamond = 0        
        self.sapphire = 0
        self.emerald = 0
        self.ruby = 0
        self.onyx = 0
        self.gold = 0
        for _ in range(diamond):
            self.token.append(Token.diamond)
        for _ in range(sapphire):
            self.token.append(Token.sapphire)
        for _ in range(emerald):
            self.token.append(Token.emerald)
        for _ in range(ruby):
            self.token.append(Token.ruby)
        for _ in range(onyx):
            self.token.append(Token.onyx)
        for _ in range(gold):
            self.token.append(Token.gold)
        self.setResource()

    def setResource(self):
        self.diamond = self.token.count(Token.diamond)
        self.sapphire = self.token.count(Token.sapphire)
        self.emerald = self.token.count(Token.emerald)
        self.ruby = self.token.count(Token.ruby)
        self.onyx = self.token.count(Token.onyx)
        self.gold = self.token.count(Token.gold)

    def appendToken(self, token: list["Token"]):
        for i in token:
            self.token.append(i)
        self.setResource()
        
    def removeToken(self, token: list["Token"]):
        for i in token:
            self.token.remove(i)
        self.setResource()

    def cost(self,cost: "Resource"):
        for i in cost.token:
            self.token.remove(i)
        self.setResource()

    def to_dict(self):
        return {
            'diamond': self.diamond,
            'sapphire': self.sapphire,
            'emerald': self.emerald,
            'ruby': self.ruby,
            'onyx': self.onyx,
            'gold': self.gold,
        }

    def to_dict_cost(self):
        return {
            'diamond': self.diamond,
            'sapphire': self.sapphire,
            'emerald': self.emerald,
            'ruby': self.ruby,
            'onyx': self.onyx,
        }



class Token(Enum):
    diamond = "diamond"#鑽石    
    sapphire = "sapphire"#藍寶石
    emerald = "emerald"#綠寶石
    ruby = "ruby"#紅寶石
    onyx = "onyx"#瑪瑙
    gold = "gold"#黃金
