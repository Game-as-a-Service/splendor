from .Token import Token


class Resource:
    def __init__(self):
        self.token: list[Token] = []
        self.white = 0
        self.blue = 0
        self.green = 0
        self.red = 0
        self.black = 0
        self.gold = 0

    def add_token(self, token: Token):
        self.token.append(token)
    
    def remove_token(self, token: Token):
        for t in self.token:
            if t.name == token.name:
                self.token.remove(t)
        