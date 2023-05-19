from .resource import  Token
class Bonus:
    def __init__(self,diamond:int=0,sapphire:int=0,emerald:int=0,ruby:int=0,onyx:int=0):
        self.diamond: int = diamond
        self.sapphire: int = sapphire
        self.emerald: int = emerald
        self.ruby: int = ruby
        self.onyx: int = onyx

    def gain(self, bonus: Token):
        if bonus==Token.diamond:
            self.diamond += 1
        elif bonus==Token.sapphire:
            self.sapphire += 1
        elif bonus==Token.emerald:
            self.emerald += 1
        elif bonus==Token.ruby:
            self.ruby += 1
        elif bonus==Token.onyx:
            self.onyx += 1
