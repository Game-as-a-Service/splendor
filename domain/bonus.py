class Bonus:
    def __init__(self,diamond:int=0,sapphire:int=0,emerald:int=0,ruby:int=0,onyx:int=0):
        self.diamond: int = diamond
        self.sapphire: int = sapphire
        self.emerald: int = emerald
        self.ruby: int = ruby
        self.onyx: int = onyx

    def gain(self, bonus: "Bonus"):
        # print(self.onyx) 
        # print(bonus.onyx) 
        self.diamond += bonus.diamond
        self.sapphire += bonus.sapphire
        self.emerald += bonus.emerald
        self.ruby += bonus.ruby
        self.onyx += bonus.onyx

