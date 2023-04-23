import requests

from config.api_config import Config


class SystemMailer:
    def __init__(self, config: Config) -> None:
        self._config = config

    def send_billing_info_mail(self, payload: dict) -> None:
        url = "REPLACE ME"

        payload["env"] = self._config.ENV_SET
        res = requests.post(url=url, json=payload)

        res_payload = res.json()
        message = res_payload.get("message") or f"{res_payload}"
        if res.status_code != 200:
            raise Exception(
                f"[Error] 信件發送失敗，【EDM】-> 訂閱制帳單收據通知信，【收件者】-> {payload['recipient']}，錯誤訊息 -> {message}"
            )

    def send_trial_plan_mail(self, email: str) -> None:
        url = "REPLACE ME"

        payload = {"recipient": email, "env": self._config.ENV_SET}
        res = requests.post(url=url, json=payload)

        res_payload = res.json()
        message = res_payload.get("message") or f"{res_payload}"
        if res.status_code != 200:
            raise Exception(
                f"[Error] 信件發送失敗，【EDM】-> 訂閱制試用14天通知信，【收件者】-> {email}，錯誤訊息 -> {message}"
            )
