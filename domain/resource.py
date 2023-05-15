from .token import Token
class Resource:
    def __init__(self):
        self.token:list[Token]=[]
        self.white: int = 0
        self.blue: int = 0
        self.green: int = 0
        self.red: int = 0
        self.black: int = 0
        self.gold: int = 0

    def add_token(self,token:Token):
        self.token.append(token)
    #花寶石
    def spend_token(self,tokens:list[Token]):
        for token in tokens:
            for i in self.token:
                if i.name == token.name:
                    self.token.remove(token)