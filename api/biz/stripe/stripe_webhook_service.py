import json
from datetime import datetime
from logging import Logger
from os import path

import paramiko

from api.biz.error import InvalidInvocation
from api.biz.stripe.cancel_subscribe_record_service import CancelSubscribeRecordService
from api.biz.stripe.stripe_customer_info_service import NikeCustomerInfoService
from api.biz.stripe.stripe_service import StripeService, stripe
from api.biz.stripe.stripe_session_info_service import StripeSessionInfoService
from api.common.datetime_utils import timestamp_to_datetime, date_to_str
from config.api_config import Config

growin_stripe = (path.realpath(path.join(path.dirname(__file__), '..', '..', 'static', 'growin-stripe.json')))


class StripeWebhookService:
    def __init__(
            self,
            config: Config,
            cronjob: paramiko.SSHClient,
            logger: Logger,
            stripe_service: StripeService,
            stripe_session_info_service: StripeSessionInfoService,
            nike_customer_info_service: NikeCustomerInfoService,
            cancel_subscribe_record_service: CancelSubscribeRecordService,
    ) -> None:
        self._config = config
        self._cronjob = cronjob
        self._logger = logger
        self._stripe_service = stripe_service
        self._growin_stripe = json.loads(open(growin_stripe, "r").read())
        self._stripe_session_info_service = stripe_session_info_service
        self._nike_customer_info_service = nike_customer_info_service
        self._cancel_subscribe_record_service = cancel_subscribe_record_service

    def webhook(self, body: str, signature: str) -> None:
        event = None
        endpoint_secret = self._config.ENDPOINT_SECRET

        try:
            event = stripe.Webhook.construct_event(body, signature, endpoint_secret)
            if event["type"] == "checkout.session.completed":
                self.checkout_session_completed(event)
            elif event["type"] == "customer.subscription.created":
                self.customer_subscription_created(event)
            elif event["type"] == "customer.subscription.updated":
                self.customer_subscription_updated(event)
            else:
                pass

        except ValueError as e:
            raise InvalidInvocation(f"Invalid payload, {e}")
        except stripe.error.SignatureVerificationError as e:
            raise InvalidInvocation(f"Invalid signature, {e}")

    def checkout_session_created(
            self,
            user_id: str,
            email: str,
            item: str,
            success_url: str,
            cancel_url: str,
            discount: str
    ) -> dict:

        customer_id = None
        customer_email = email

        cus_info = self._nike_customer_info_service.get("user_id", user_id)
        if cus_info.status != "inactive":
            customer_id = cus_info.customer_id
            customer_email = None

        if item == "Basic Yearly":
            session = stripe.checkout.Session.create(
                mode="subscription",
                payment_method_types=["card"],
                discounts=[{"coupon": "seAXfDr2"}],
                line_items=[{
                    "price": self._growin_stripe["item"][item],
                    "quantity": 1
                }],
                success_url=success_url,
                cancel_url=cancel_url,
                phone_number_collection={'enabled': True},
                customer=customer_id,
                customer_email=customer_email,
                locale="zh-TW"
            )
        elif item == "Basic Monthly" and discount:
            session = stripe.checkout.Session.create(
                mode="subscription",
                payment_method_types=["card"],
                discounts=[{"coupon": discount}],
                line_items=[{
                    "price": self._growin_stripe["item"][item],
                    "quantity": 1
                }],
                success_url=success_url,
                cancel_url=cancel_url,
                phone_number_collection={'enabled': True},
                customer=customer_id,
                customer_email=customer_email,
                locale="zh-TW"
            )
        else:
            session = stripe.checkout.Session.create(
                mode="subscription",
                payment_method_types=["card"],
                allow_promotion_codes=True,
                line_items=[{
                    "price": self._growin_stripe["item"][item],
                    "quantity": 1
                }],
                success_url=success_url,
                cancel_url=cancel_url,
                phone_number_collection={'enabled': True},
                customer=customer_id,
                customer_email=customer_email,
                locale="zh-TW"
            )
        self._logger.info(f"{user_id} 建立一個 {item} 的checkout session.")

        self._stripe_session_info_service.insert({
            "user_id": user_id,
            "customer_id": customer_id,
            "session_id": session["id"],
            "payment_status": session["payment_status"],
        })

        return {"sessionUrl": session["url"]}

    def checkout_session_completed(self, event: dict) -> None:
        self._stripe_session_info_service.update(
            key="session_id",
            value=event["data"]["object"]["id"],
            data={
                "customer_id": event["data"]["object"]["customer"],
                "subscription_id": event["data"]["object"]["subscription"],
                "payment_status": "paid"
            }
        )

    def customer_subscription_created(self, event: dict) -> None:
        event = event["data"]["object"]

        session_info = self._stripe_session_info_service.get("subscription_id", event["id"])
        stripe_cus_r = self._stripe_service.stripe_customer_retrieve(event["customer"])

        self._nike_customer_info_service.update(
            key="user_id",
            value=session_info.user_id,
            data={
                "customer_id": event["customer"],
                "name": stripe_cus_r["name"],
                "phone": stripe_cus_r["phone"],
                "plan": [k for k, v in self._growin_stripe["item"].items()
                         if v == event["items"]["data"][0]["plan"]["id"]][0],
                "subscribed_at": timestamp_to_datetime(event["current_period_start"]),
                "expire_at": timestamp_to_datetime(event["current_period_end"]),
                "status": "active",
            }
        )

        self._logger.info("=" * 50, "[Connect CronJob]", "=" * 50)
        stdin, stdout, stderr = self._cronjob.exec_command(
            f"/home/app_runner/app/growin-cron-job/venv/bin/growin-cron-job account create-subscribe-info -s "
            f"{event['id']}")
        self._logger.info(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            self._logger.error(err)

    def customer_subscription_updated(self, event: dict) -> None:
        obj = event["data"]["object"]
        previous = event["data"]["previous_attributes"]

        if all(key in previous for key in ("cancel_at", "cancel_at_period_end", "canceled_at")):
            stripe_session_info = self._stripe_session_info_service.get("subscription_id", obj["id"])
            # 取消訂閱
            if obj["cancel_at_period_end"]:
                self._cancel_subscribe_record_service.insert({
                    "subscription_id": obj["id"],
                    "customer_id": stripe_session_info.customer_id,
                    "canceled_at": date_to_str(timestamp_to_datetime(obj["canceled_at"])),
                    "expire_at": date_to_str(timestamp_to_datetime(obj["cancel_at"])),
                    "status": "canceled"
                })
                return

            # 恢復訂閱
            if not obj["cancel_at_period_end"]:
                self._cancel_subscribe_record_service.insert({
                    "subscription_id": obj["id"],
                    "customer_id": stripe_session_info.customer_id,
                    "recovered_at": datetime.now(),
                    "status": "recovered"
                })

        if all(key in previous for key in ("items", "latest_invoice", "plan")):
            # 變更方案 (月 -> 年 or 年 -> 月)
            pass
