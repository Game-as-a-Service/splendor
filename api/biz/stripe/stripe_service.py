from logging import Logger

import stripe
from sqlalchemy.orm import Session

from api.biz.stripe.stripe_customer_info_service import NikeCustomerInfoService
from api.biz.stripe.stripe_subscribe_info_service import StripeSubscribeInfoService
from config.api_config import Config
from dbmodels.user_profile.nike_customer_info import NikeCustomerInfo
from dbmodels.user_profile.stripe_subscribe_info import StripeSubscribeInfo

stripe.api_key = Config.STRIPE_SECRET_KEY


class StripeService:
    def __init__(
            self,
            config: Config,
            logger: Logger,
            nike_sql_session: Session,
            nike_customer_info_service: NikeCustomerInfoService,
            stripe_subscribe_info_service: StripeSubscribeInfoService
    ) -> None:
        self._config = config
        self._logger = logger
        self._nike_sql_session = nike_sql_session
        self._nike_customer_info_service = nike_customer_info_service
        self._stripe_subscribe_info_service = stripe_subscribe_info_service

    @staticmethod
    def stripe_customer_retrieve(customer_id: str) -> dict:
        return stripe.Customer.retrieve(customer_id)

    def customer_portal(self, user_id: str, return_url: str) -> dict:
        cus_info: NikeCustomerInfo = self._nike_customer_info_service.get("user_id", user_id)

        if cus_info:
            session = stripe.billing_portal.Session.create(
                customer=cus_info.customer_id,
                return_url=return_url
            )
            return {"sessionUrl": session.url}
        return {"sessionUrl": None}

    def customer_portal_update_page(self, user_id: str, return_url: str) -> dict:
        cus_info: NikeCustomerInfo = self._nike_customer_info_service.get("user_id", user_id)

        if cus_info:
            session = stripe.billing_portal.Session.create(
                customer=cus_info.customer_id,
                return_url=return_url
            )
            subscribe_info: StripeSubscribeInfo = self._stripe_subscribe_info_service.get(
                "customer_id", cus_info.customer_id)
            return {"sessionUrl": f"{session.url}/subscriptions/{subscribe_info.subscription_id}/update"}
        return {"sessionUrl": None}
