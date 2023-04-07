import json
from datetime import datetime
from logging import Logger

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TemplateSendMessage, ButtonsTemplate, URIAction
from sqlalchemy.orm import Session

from api.biz.error import InvalidInvocation
from config.api_config import Config
from dbmodels.user_profile.nike_customer_info import NikeCustomerInfo

line_bot_api = LineBotApi(Config().LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config().LINE_CHANNEL_SECRET)


class LineWebhookService:
    def __init__(self, config: Config, logger: Logger, user_sql_session: Session):
        self._config = config
        self._logger = logger
        self._user_sql_session = user_sql_session

    def webhook(self, body: str, signature: str) -> None:
        self._logger.info(f"Request Body: {body}")

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            raise InvalidInvocation("Invalid signature. Please check your channel access token/channel secret.")

        body = json.loads(body)
        if not body["events"]:
            self._logger.error(
                "Line webhook event is empty. Maybe webhook authentication. Please pay more attention to this issue.")
            return

        events = body["events"][0]

        if "message" in events and events["message"]["text"] == "綁定帳號":
            self._create_account_integration(events["source"]["userId"])
        elif ("type" in events and events["type"] == "accountLink") and \
                ("link" in events and events["link"]["result"] == "ok"):
            self._account_integration_succeeded(events["source"]["userId"], events["link"]["nonce"])

    def _create_account_integration(self, user_id: str) -> None:
        link_token = line_bot_api.issue_link_token(user_id)
        uri = self._config.GROWIN_URL.rstrip("/") + f"/my/notification/line?linkToken={link_token.link_token}"

        line_bot_api.push_message(user_id, TemplateSendMessage(
            alt_text="綁定帳號",
            template=ButtonsTemplate(
                text="綁定帳號",
                actions=[
                    URIAction(label="綁定帳號", uri=uri)
                ]
            )
        ))

    def _account_integration_succeeded(self, line_user_id: str, nonce: str) -> None:
        self._user_sql_session.query(NikeCustomerInfo) \
            .filter(NikeCustomerInfo.line_nonce == nonce) \
            .update({"line_user_id": line_user_id, "line_bind_status": True, "line_bind_at": datetime.now()})
