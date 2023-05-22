from enum import Enum
from typing import List


class Resource:
    def __init__(self) -> None:
        self.token: List[Token] = []
        self.diamond: int = 0
        self.sapphire: int = 0
        self.emerald: int = 0
        self.ruby: int = 0
        self.onyx: int = 0
        self.gold: int = 0


class Token(Enum):
    diamond = "diamond"  # 鑽石
    sapphire = "sapphire"  # 藍寶石
    emerald = "emerald"  # 綠寶石
    ruby = "ruby"  # 紅寶石
    onyx = "onyx"  # 瑪瑙
    gold = "gold"  # 黃金
