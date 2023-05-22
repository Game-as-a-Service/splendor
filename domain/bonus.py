from .resource import  Token
class Bonus:
    def __init__(self,diamond:int=0,sapphire:int=0,emerald:int=0,ruby:int=0,onyx:int=0):
        self.diamond: int = diamond
        self.sapphire: int = sapphire
        self.emerald: int = emerald
        self.ruby: int = ruby
        self.onyx: int = onyx