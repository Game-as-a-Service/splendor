from typing import List

from sqlalchemy.orm import Session

from api.common.datetime_utils import date_to_str
from dbmodels.manager.video_info import VideoInfo


class VideoInfoService:
    def __init__(self, manager_sql_session: Session):
        self._manager_sql_session = manager_sql_session

    def get_video_info_by_category(self, category: str) -> List[VideoInfo]:
        return self._manager_sql_session.query(VideoInfo) \
            .filter(VideoInfo.category == category) \
            .order_by(VideoInfo.created_at.desc()) \
            .all()

    def video_info(self, category: str) -> List[dict]:
        infos: List[VideoInfo] = self.get_video_info_by_category(category)

        data = []
        for i in infos:
            data.append({
                "category": i.category,
                "title": i.title,
                "content": i.content,
                "symbol": i.symbol,
                "publishedAt": date_to_str(i.published_at),
                "photoUrl": i.photo_url,
                "videoUrl": i.video_url,
                "status": i.status
            })
        return data
