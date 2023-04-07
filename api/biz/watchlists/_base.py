from abc import abstractmethod
from typing import List


class WatchlistHandler:

    def __init__(self):
        pass

    @property
    def account_type(self) -> str:
        """
        使用者類型
        :return:
        """
        raise NotImplementedError(f"{self.__class__.__name__}.account_type")

    @abstractmethod
    def _update_watchlist(self, user_id: str, watchlist: list) -> None:
        """
        更新 DB 追蹤清單
        :param user_id: Growin 使用者 id
        :param watchlist: 追蹤清單
        """
        raise NotImplementedError

    @abstractmethod
    def add_watchlist(self, user_id: str, name: str) -> str:
        """
        新增追蹤清單
        :param user_id: Growin 使用者 id
        :param name: 欲命名的名稱
        :raise DataNotFound: 找不到 user_id
        :return watchlist_id: 新產生的追蹤清單編號
        """
        raise NotImplementedError

    @abstractmethod
    def delete_watchlist(self, user_id: str, watchlist_id: str) -> None:
        """
        新增追蹤清單
        :param user_id: Growin 使用者 id
        :param watchlist_id: 追蹤清單編號
        :raise DataNotFound: 找不到 user_id
        """
        raise NotImplementedError

    @abstractmethod
    def rename_watchlist(self, user_id: str, watchlist_id: str, name: str) -> None:
        """
        重新命名追蹤清單
        :param user_id: Growin 使用者 id
        :param watchlist_id: 追蹤清單編號
        :param name: 欲修改的名稱
        :raise DataNotFound: 找不到 user_id
        """
        raise NotImplementedError

    @abstractmethod
    def add_symbol(self, user_id: str, watchlist_id: str, symbol: str) -> None:
        """
        增加標的
        :param user_id: Growin 使用者 id
        :param watchlist_id: 追蹤清單編號
        :param symbol: 欲增加的標的
        :raise DataNotFound: 找不到 user_id
        """
        raise NotImplementedError

    @abstractmethod
    def remove_symbol(self, user_id: str, watchlist_id: str, symbol: str) -> None:
        """
        移除標的
        :param user_id: Growin 使用者 id
        :param watchlist_id: 追蹤清單編號
        :param symbol: 欲移除的標的
        :raise DataNotFound: 找不到 user_id
        """
        raise NotImplementedError

    @abstractmethod
    def replace_symbols(self, user_id: str, watchlist_id: str, symbols: List[str]) -> None:
        """
        移除標的
        :param user_id: Growin 使用者 id
        :param watchlist_id: 追蹤清單編號
        :param symbols: 欲重新排序的標的列表
        :raise DataNotFound: 找不到 user_id
        """
        raise NotImplementedError
