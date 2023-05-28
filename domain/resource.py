from .token import Token

class Resource:
    def __init__(self, diamond=0, sapphire=0, emerald=0, ruby=0, onyx=0):
        self.token = [Token.diamond] * diamond + [Token.sapphire] * sapphire + [Token.emerald] * emerald + [Token.ruby] * ruby + [Token.onyx] * onyx
        self.diamond = diamond
        self.sapphire = sapphire
        self.emerald = emerald
        self.ruby = ruby
        self.onyx = onyx
        self.gold = 0

    def add_token(self,token:Token):
        self.token.append(token)
        self.__dict__[token.name]+=1
    #花寶石
    def spend_token(self,tokens:list[Token]):
        for token in tokens:
            if self.__dict__[token.name] > 0:
                self.token.remove(token)
                self.__dict__[token.name] -= 1

        