class Bonus:
    def __init__(self):
        self.ruby: int = 0
        self.sapphire: int = 0
        self.emerald: int = 0
        self.diamond: int = 0
        self.onyx: int = 0

    def 獲得(self, bonus: "Bonus"):
        self.ruby += bonus.ruby
        self.sapphire += bonus.sapphire
        self.emerald += bonus.emerald
        self.diamond += bonus.diamond
        self.onyx += bonus.onyx
