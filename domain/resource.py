from enum import Enum


class Resource:
    def __init__(self) -> None:
        self.token: list[Token] = []
        self.ruby: int = 0
        self.sapphire: int = 0
        self.emerald: int = 0
        self.diamond: int = 0
        self.onyx: int = 0
        self.gold: int = 0

    # 新增Token至 self.token 並且更新 self.ruby, self.sapphire, self.emerald, self.diamond, self.onyx, self.gold
    def 存錢(self, token: "Token"):
        self.token.append(token)
        self.__dict__[token.name] += 1

    def 花錢(self, token: int):
        self.token.clear()
        self.onyx = 0


class Token(Enum):
    ruby = "ruby"
    sapphire = "sapphire"
    emerald = "emerald"
    diamond = "diamond"
    onyx = "onyx"
    gold = "gold"
