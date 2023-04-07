from typing import Optional

from discord_webhook import DiscordEmbed, DiscordWebhook
from sqlalchemy.orm import Session

from config.api_config import Config
from dbmodels.nike.tradingview_account_list import TradingviewAccountList


class TradingviewAccountService:
    def __init__(self, config: Config, nike_sql_session: Session) -> None:
        self._config = config
        self._nike_sql_session = nike_sql_session

    def account(self, user_id: str, tradingview_account: str) -> None:
        account: TradingviewAccountList = self._nike_sql_session.query(TradingviewAccountList) \
            .filter(TradingviewAccountList.user_id == user_id) \
            .first()

        if not account:
            self._nike_sql_session.add(
                TradingviewAccountList(**{"user_id": user_id, "tradingview_account": tradingview_account})
            )
            self._nike_sql_session.flush()
            self._discord_hook(tradingview_account=tradingview_account, last_tradingview_account=None)
            return

        last_tradingview_account = account.tradingview_account
        self._nike_sql_session.query(TradingviewAccountList) \
            .filter(TradingviewAccountList.user_id == user_id) \
            .update({
                "last_tradingview_account": last_tradingview_account,
                "tradingview_account": tradingview_account
            })
        self._discord_hook(tradingview_account=tradingview_account, last_tradingview_account=last_tradingview_account)

    def _discord_hook(self, tradingview_account: str, last_tradingview_account: Optional[str]) -> None:
        webhook = DiscordWebhook(url=self._config.DISCORD_TRADINGVIEW_HOOK_URL)
        embed = DiscordEmbed(title="Register Growin Indicator.", description="", color="03b2f8")
        embed.add_embed_field(name="Last Register Account", value=f"```{last_tradingview_account}```", inline=True)
        embed.add_embed_field(name="Current Register Account", value=f"```{tradingview_account}```", inline=True)
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
