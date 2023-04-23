import logging
import socket
import sys
from typing import Optional

from discord_webhook import DiscordEmbed, DiscordWebhook
from requests import Response

COLOURS = {
    None: 2040357,  # Unknown log level
    logging.CRITICAL: 14362664,  # Red
    logging.ERROR: 14362664,  # Red
    logging.WARNING: 16497928,  # Yellow
    logging.INFO: 2196944,  # Blue
    logging.DEBUG: 8947848,  # Gray
}

EMOJIS = {
    None: "",  # Unknown log level
    logging.CRITICAL: "🆘",
    logging.ERROR: "❌",
    logging.WARNING: "⚠️",
    logging.INFO: "🚀",
    logging.DEBUG: "",
}


class DiscordHandler(logging.Handler):
    def __init__(
        self,
        service_name: str,
        webhook_url: str,
        colours=COLOURS,
        emojis=EMOJIS,
        avatar_url: Optional[str] = None,
        rate_limit_retry: bool = True,
        embed_line_wrap_threshold: int = 60,
        message_break_char: Optional[str] = None,
        discord_timeout: float = 5.0,
        message_content: bool = False,
        environment: str = "",
    ):
        logging.Handler.__init__(self)
        self._webhook_url = webhook_url
        self._service_name = service_name
        self._colours = colours
        self._emojis = emojis
        self._avatar_url = avatar_url
        self._rate_limit_retry = rate_limit_retry
        self._embed_line_wrap_threshold = embed_line_wrap_threshold
        self._message_break_char = message_break_char
        self._discord_timeout = discord_timeout
        self._environment = environment

    def attempt_to_report_failure(self, resp: Response, orignal: DiscordWebhook):
        """
        Attempt to report a failure to deliver a log message.

        Usually this happens if we pass content to Discord the server does not like.

        More information

        - https://stackoverflow.com/questions/53935198/in-my-discord-webhook-i-am-getting-the-error-embeds-0
        """
        # Output to the stderr, as it is not safe to use logging here
        #
        print(  # noqa : T201
            f"Discord webhook request failed: {resp.status_code}: {resp.content}. Payload content was: "
            + "{orignal.content}, embeds: {orignal.embeds}",
            file=sys.stderr,
        )
        # Attempt to warn account about log failure
        discord = DiscordWebhook(
            url=self._webhook_url,
            username=self._service_name,
            rate_limit_retry=self._rate_limit_retry,
            avatar_url=self._avatar_url,
            timeout=self._discord_timeout,
        )
        discord.content = (
            f"Failed to deliver log message: {resp.status_code}: {resp.content}"
        )
        discord.execute()

    def emit(self, record: logging.LogRecord):  # noqa: C901
        """Send a log entry to Discord."""

        inbound_msg = self.format(record)
        colour = self._colours.get(record.levelno, None)
        emoji = self._emojis.get(record.levelno, None)

        discord_text = DiscordWebhook(
            url=self._webhook_url,
            username=self._service_name,
            rate_limit_retry=self._rate_limit_retry,
            avatar_url=self._avatar_url,
            timeout=self._discord_timeout,
        )

        discord_file = DiscordWebhook(
            url=self._webhook_url,
            username=self._service_name,
            rate_limit_retry=self._rate_limit_retry,
            avatar_url=self._avatar_url,
            timeout=self._discord_timeout,
        )

        try:
            first, remainder = inbound_msg.split("\n", maxsplit=1)
            fields = first.split(" | ")

            embed = DiscordEmbed(
                title=f"{emoji}  {self._service_name} ({self._environment})",
                description="",
                color=colour,
            )
            embed.set_timestamp()
            embed.set_footer(text="Backend team need to hotfix.")
            embed.add_embed_field(name="LEVEL", value=f"```{fields[2]}```", inline=True)
            embed.add_embed_field(
                name="DATETIME", value=f"```{fields[0]}```", inline=True
            )
            embed.add_embed_field(
                name="HOSTNAME", value=f"```{socket.gethostname()}```", inline=False
            )
            embed.add_embed_field(
                name="ERROR MESSAGE", value=f"```{fields[5]}```", inline=False
            )
            discord_text.add_embed(embed)

            resp = discord_text.execute()
            assert isinstance(resp, Response), f"Discord webhook replies: {resp}"
            if resp.status_code != 200:
                self.attempt_to_report_failure(resp, discord_text)

            discord_file.add_file(file=remainder, filename="error.txt")

            resp = discord_file.execute()
            assert isinstance(resp, Response), f"Discord webhook replies: {resp}"
            if resp.status_code != 200:
                self.attempt_to_report_failure(resp, discord_file)
        except Exception as e:
            # We cannot use handleError here, because Discord request may cause
            # infinite recursion when Discord connection fails and
            # it tries to log.
            # We fall back to writing the error to stderr
            print(f"Error from Discord logger {e}", file=sys.stderr)  # noqa : T201
            self.handleError(record)
