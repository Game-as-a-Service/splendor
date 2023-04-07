from logging import Logger
from typing import Optional

from flask import session
from sqlalchemy.orm import Session

from dbmodels.user_profile.institution_exclusive_offers import InstitutionExclusiveOffers


class InstitutionExclusiveOffersService:
    def __init__(self, logger: Logger, user_sql_session: Session):
        self._logger = logger
        self._user_sql_session = user_sql_session

    def get_exclusive_offers_by_user_id(
            self,
            user_id: str,
            institution: str,
            collaborate: str,
    ) -> InstitutionExclusiveOffers:
        return self._user_sql_session.query(InstitutionExclusiveOffers) \
            .filter(InstitutionExclusiveOffers.user_id == user_id) \
            .filter(InstitutionExclusiveOffers.institution == institution) \
            .filter(InstitutionExclusiveOffers.collaborate == collaborate) \
            .order_by(InstitutionExclusiveOffers.created_at.desc()) \
            .first()

    def get_offer(self, institution: str, collaborate: str) -> Optional[dict]:
        offer: InstitutionExclusiveOffers = self.get_exclusive_offers_by_user_id(
            session["user_id"], institution, collaborate)

        if not offer or offer.end_at is not None:
            return {
                "isOpened": False
            }

        data = {
            "isOpened": True,
            "institution": offer.institution,
            "collaborate": offer.collaborate,
            **offer.package
        }
        return data
