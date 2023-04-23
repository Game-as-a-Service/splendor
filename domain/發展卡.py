class Player:
    def __init__(self,id,順位,購買的發展卡,保留的發展卡,貴族卡,資源) -> None:
        self._id=id
        self._順位=順位
        self._購買的發展卡=購買的發展卡
        self._保留的發展卡=保留的發展卡
        self._貴族卡=貴族卡
        self._資源=資源

    def 購買發展卡(self,LV,卡號,花費資源):
        self._購買的發展卡.append(發展卡(LV,卡號,花費資源))
        self._資源.黑寶石-=花費資源.黑寶石