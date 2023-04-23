import os.path
import pathlib
import shutil
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from stat import S_ISDIR, S_ISREG
from typing import List, Optional

import boto3
from flask import current_app

TYPE_UNKNOWN = 0
TYPE_FILE = 1
TYPE_DIRECTORY = 2


@dataclass
class FileStat:
    type: int
    creation_time: datetime
    modification_time: datetime
    size: int


class IFileStorage(metaclass=ABCMeta):
    @property
    @abstractmethod
    def base_path(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def read(self, path: str) -> bytes:
        """
        讀取相對路徑的檔案內容
        :param path: 相對路徑
        :raise IsADirectoryError: 當要讀取的路徑是目錄
        :raise FileNotFoundError: 當要讀取的路徑不存在
        :raise PermissionError: 沒有讀取的權限
        :return: 檔案內容
        """
        raise NotImplementedError

    @abstractmethod
    def write(self, path: str, content: bytes):
        """
        將檔案內容寫入相對路徑
        :param path: 相對路徑
        :param content: 檔案內容
        :raise IsADirectoryError: 當要寫入的路徑是目錄
        :raise PermissionError: 沒有讀寫入的權限
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, path: str, recursive: bool = False):
        """
        刪除相對路徑的檔案
        :param path: 相對路徑
        :param recursive: 遞歸刪除
        :raise IsADirectoryError: 當要刪除的路徑是目錄
        :raise FileNotFoundError: 當要刪除的路徑不存在
        :raise PermissionError: 沒有刪除的權限
        """
        raise NotImplementedError

    @abstractmethod
    def stat(self, path: str) -> FileStat:
        """
        取得相對路徑的檔案狀態
        :param path: 相對路徑
        :raise PermissionError: 沒有讀取的權限
        :raise FileNotFoundError: 單案不存在
        :return: 檔案狀態，如果檔案不存在將會 None
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def path_join(path: str, *paths: str) -> str:
        """
        組合路徑
        :param path: 相對路徑
        :param paths:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def list(self, path: str) -> List[str]:
        """
        列出相對路徑中的檔案或目錄, list 包含完成的相對路徑
        :param path: 相對路徑
        :raise PermissionError: 沒有讀取的權限
        :raise FileNotFoundError: 相對路徑不存在
        :return: 單案或目錄清單
        """
        raise NotImplementedError

    def is_exist(self, path: str) -> bool:
        """
        相對路徑是否存在
        :param path: 相對路徑
        :raise PermissionError: 沒有讀取的權限
        :return:
        """
        try:
            self.stat(path)
            return True
        except FileNotFoundError:
            return False

    def is_dir(self, path: str) -> bool:
        """
        相對路徑是否為目錄
        :param path: 相對路徑
        :raise PermissionError: 沒有讀取的權限
        :return:
        """
        try:
            stat = self.stat(path)
            return stat.type == TYPE_DIRECTORY
        except FileNotFoundError:
            return False

    def is_file(self, path: str) -> bool:
        """
        相對路徑是否為單案
        :param path: 相對路徑
        :raise PermissionError: 沒有讀取的權限
        :return:
        """
        try:
            stat = self.stat(path)
            return stat.type == TYPE_FILE
        except FileNotFoundError:
            return False

    def last_modified(self, path: str) -> Optional[float]:
        """
        單案最後更新時間的 timestamp
        :param path: 相對路徑
        :raise PermissionError: 沒有讀取的權限
        :raise FileNotFoundError: 相對路徑不存在
        :return:
        """
        stat = self.stat(path)
        return stat.modification_time.timestamp() if stat else None


class LocalFileStorage(IFileStorage):
    @property
    def base_path(self) -> str:
        return self._base_path

    def __init__(self, base_path: str):
        self._base_path = os.path.abspath(base_path)
        self.stat("/")

    def read(self, path: str) -> bytes:
        real_path = self.path_join(self.base_path, path)
        stat = self.stat(path)
        if stat.type == TYPE_DIRECTORY:
            raise IsADirectoryError(f"要讀取的檔案 {real_path} 是目錄")

        with open(real_path, "rb") as fd:
            res = fd.read()
        return res

    def write(self, path: str, content: bytes):
        real_path = self.path_join(self.base_path, path)
        pathlib.Path(os.path.dirname(real_path)).mkdir(parents=True, exist_ok=True)
        with open(real_path, "wb") as fd:
            fd.write(content)

    def delete(self, path: str, recursive: bool = False):
        if path == "/" or "":
            raise PermissionError("不能刪除相對的根目錄")
        stat = self.stat(path)
        real_path = self.path_join(self.base_path, path)

        if not recursive and stat.type == TYPE_DIRECTORY:
            raise IsADirectoryError(f"要刪除的路徑 {path} 是目錄")

        rm = os.remove if stat.type != TYPE_DIRECTORY else shutil.rmtree
        rm(real_path)

    def stat(self, path: str) -> FileStat:
        real_path = self.path_join(self.base_path, path)
        os_stat = os.stat(real_path)
        if S_ISDIR(os_stat.st_mode):
            stat_type = TYPE_DIRECTORY
        elif S_ISREG(os_stat.st_mode):
            stat_type = TYPE_FILE
        else:
            stat_type = TYPE_UNKNOWN
        return FileStat(
            type=stat_type,
            creation_time=datetime.fromtimestamp(os_stat.st_ctime),
            modification_time=datetime.fromtimestamp(os_stat.st_mtime),
            size=os_stat.st_size,
        )

    @staticmethod
    def path_join(path: str, *paths: str) -> str:
        return os.path.abspath(os.path.join(path, *[p.strip("/") for p in paths]))

    def list(self, path: str) -> List[str]:
        stat = self.stat(path)
        if stat.type != TYPE_DIRECTORY:
            return ["/" + path.lstrip("/")]

        real_path = self.path_join(self.base_path, path)
        file_list_set = set()
        for r in os.listdir(real_path):
            file_list_set.add("/" + self.path_join(path, r).strip("/"))

        return list(file_list_set)


class S3FileStorage(IFileStorage):
    _s3_client: boto3.client

    @property
    def base_path(self) -> str:
        return self._base_path

    @property
    def base_uri(self) -> str:
        return self._base_uri

    def __init__(
        self,
        bucket: str,
        base_prefix: str,
        aws_region: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        self.logger = current_app.logger
        self._base_path = base_prefix.strip(" /")
        self._base_uri = f"s3://{bucket}/{self._base_path}"
        self._bucket = bucket
        kwargs = {}
        if aws_region:
            kwargs["region_name"] = aws_region
        if aws_access_key_id:
            kwargs["aws_access_key_id"] = aws_access_key_id
        if aws_secret_access_key:
            kwargs["aws_secret_access_key"] = aws_secret_access_key

        self._s3_client = boto3.client("s3", **kwargs)
        if not self.is_dir("/"):
            raise Exception(f"{self._base_path} is not exists in Bucket {self._bucket}")

    def read(self, path: str) -> bytes:
        key = self.path_join(self.base_path, path)
        stat = self.stat(path)
        if stat.type == TYPE_DIRECTORY:
            raise IsADirectoryError(f"要讀取的路徑 {self.base_uri}/{key} 是目錄")
        res = self._s3_client.get_object(Bucket=self._bucket, Key=key)
        return res["Body"].read()

    def write(self, path: str, content: bytes):
        key = self.path_join(self.base_path, path)
        if self.is_dir(path):
            raise IsADirectoryError(f"要寫入的路徑 {self.base_uri}/{key} 是目錄")
        self._s3_client.put_object(Bucket=self._bucket, Key=key, Body=content)

    def delete(self, path: str, recursive: bool = False):
        if path == "/" or "":
            raise PermissionError("不能刪除相對的根目錄")
        key = self.path_join(self.base_path, path)
        stat = self.stat(path)
        if not recursive and stat.type == TYPE_DIRECTORY:
            raise IsADirectoryError(f"要刪除的路徑 {self.base_uri}/{key} 是目錄")

        if stat.type != TYPE_DIRECTORY:
            self._s3_client.delete_object(Bucket=self._bucket, Key=key)
            return

        prefix = key.strip("/") + "/"
        next_marker = True
        while next_marker:
            params = dict(Bucket=self._bucket, Prefix=prefix)
            if isinstance(next_marker, str):
                params["Marker"] = next_marker
            res = self._s3_client.list_objects(Bucket=self._bucket, Prefix=prefix)
            contents = res.get("Contents") or []
            objects = [{"Key": content["Key"]} for content in contents]
            interval = 500
            s = 0
            delete_objects = objects[s : s + interval]
            while delete_objects:
                self._s3_client.delete_objects(
                    Bucket=self._bucket, Delete={"Objects": delete_objects}
                )
                s += interval
                delete_objects = objects[s : s + interval]
            next_marker = res.get("NextMarker")

    def stat(self, path: str) -> FileStat:
        prefix = self.path_join(self.base_path, path)
        res = self._s3_client.list_objects(
            Bucket=self._bucket, Prefix=prefix, Delimiter="/", MaxKeys=1
        )
        contains = res.get("Contents")
        common_prefixes = res.get("CommonPrefixes")
        if not contains and not common_prefixes:
            raise FileNotFoundError(f"檔案 {path} 不存在")

        if not contains and common_prefixes[0]["Prefix"] == path.strip("/") + "/":
            res = self._s3_client.list_objects(
                Bucket=self._bucket,
                Prefix=common_prefixes[0]["Prefix"],
                Delimiter="/",
                MaxKeys=1,
            )
            contains = res.get("Contents")
        if not contains:
            file_type = (
                TYPE_DIRECTORY
                if common_prefixes[0]["Prefix"].endswith("/")
                else TYPE_FILE
            )
            return FileStat(
                type=file_type,
                creation_time=datetime.fromtimestamp(0),
                modification_time=datetime.fromtimestamp(0),
                size=0,
            )
        if prefix != contains[0]["Key"] and contains[0]["Key"].startswith(
            prefix.strip("/") + "/"
        ):
            return FileStat(
                type=TYPE_DIRECTORY,
                creation_time=datetime.fromtimestamp(0),
                modification_time=datetime.fromtimestamp(0),
                size=0,
            )

        file_type = TYPE_DIRECTORY if contains[0]["Key"].endswith("/") else TYPE_FILE
        datetime.now().timestamp()
        last_modified_ts = contains[0]["LastModified"].timestamp()
        return FileStat(
            type=file_type,
            creation_time=datetime.fromtimestamp(last_modified_ts),
            modification_time=datetime.fromtimestamp(last_modified_ts),
            size=contains[0]["Size"],
        )

    @staticmethod
    def path_join(path: str, *paths: str) -> str:
        tail_slash = "/" if paths[-1].endswith("/") else ""
        return (
            "/".join([path.strip("/"), *[r.strip("/") for r in paths if r.strip("/")]])
            + tail_slash
        ).lstrip("/")

    def list(self, path: str) -> List[str]:
        stat = self.stat(path)
        if stat.type != TYPE_DIRECTORY:
            return ["/" + path.lstrip("/")]

        path = path.rstrip("/") + "/"
        prefix = self.path_join(self.base_path, path)
        next_marker = True
        file_list_set = set()
        while next_marker:
            params = dict(Bucket=self._bucket, Prefix=prefix, Delimiter="/")
            if isinstance(next_marker, str):
                params["Marker"] = next_marker
            res = self._s3_client.list_objects(**params)
            prefix_len = len(self.base_path)
            for r in res.get("Contents") or []:
                p = r["Key"][prefix_len:].rstrip("/")
                if not p:
                    continue
                file_list_set.add("/" + p.strip("/"))
            for r in res.get("CommonPrefixes") or []:
                p = r["Prefix"][prefix_len:].rstrip("/")
                if not p:
                    continue
                file_list_set.add("/" + p.strip("/"))
            next_marker = res.get("NextMarker")

        return list(file_list_set)
