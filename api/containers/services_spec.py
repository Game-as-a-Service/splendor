import os.path

import paramiko
import pinject
from flask import Flask

from api.biz.account.business_account_service import BusinessAccountService
from api.biz.account.institution_exclusive_offers_service import InstitutionExclusiveOffersService
from api.biz.account.normal_account_service import NormalAccountService
from api.biz.account.tradingview_account_service import TradingviewAccountService
from api.biz.backtest.backtest_action_service import BacktestActionService
from api.biz.backtest.backtest_result_service import BacktestResultService
from api.biz.backtest.backtest_trend_service import BacktestTrendService
from api.biz.backtest.cumulative_roi_service import CumulativeRoiService
from api.biz.content.content_service import ContentService
from api.biz.historical.historical_dividend_service import HistoricalDividendService
from api.biz.historical.historical_rating_service import HistoricalRatingService
from api.biz.historical.historical_symbol_price_service import HistoricalSymbolPriceService
from api.biz.indicator.dividend_indicator_service import DividendIndicatorService
from api.biz.indicator.indicator_result_service import IndicatorResultService
from api.biz.indicator.trend_indicator_service import TrendIndicatorService
from api.biz.indicator.value_indicator_service import ValueIndicatorService
from api.biz.institution.chip_basic_info_service import ChipBasicInfoService
from api.biz.institution.chip_institution_holding_info_service import ChipInstitutionHoldingInfoService
from api.biz.institution.famous_investor_status_service import FamousInvestorStatusService
from api.biz.institution.insider_buying_info_service import InsiderBuyingInfoService
from api.biz.institution.investor_ranking_service import InvestorRankingService
from api.biz.line.line_webhook_service import LineWebhookService
from api.biz.market_sentiment import MarketSentimentService
from api.biz.market_sentiment.early_warning_service import EarlyWarningService
from api.biz.market_sentiment.fear_greed_service import FearGreedService
from api.biz.notification.record.push_notification_record_service import PushNotificationRecordService
from api.biz.notification.robo.robo_available_service import RoboAvailableService
from api.biz.notification.robo.robo_notification_service import RoboNotificationService
from api.biz.search_engine.screener_service import ScreenerService
from api.biz.search_engine.search_symbol_service import SearchSymbolService
from api.biz.service_status.stock_mining_service import StockMiningServiceStatus
from api.biz.stripe.cancel_subscribe_record_service import CancelSubscribeRecordService
from api.biz.stripe.stripe_customer_info_service import NikeCustomerInfoService
from api.biz.stripe.stripe_service import StripeService
from api.biz.stripe.stripe_session_info_service import StripeSessionInfoService
from api.biz.stripe.stripe_subscribe_info_service import StripeSubscribeInfoService
from api.biz.stripe.stripe_webhook_service import StripeWebhookService
from api.biz.symbol.symbol_info_service import SymbolInfoService
from api.biz.symbol.symbol_service import SymbolService
from api.biz.video.video_info_service import VideoInfoService
from api.biz.watchlists import WatchlistServiceFacade
from api.common.file_storage.storage_adapter import IFileStorage, S3FileStorage, LocalFileStorage
from api.common.mail.system_mailer import SystemMailer
from api.common.updated_at_utils import UpdatedAtUtils
from config.api_config import Config

service_classes = [
    BacktestActionService,
    BacktestResultService,
    BacktestTrendService,
    BusinessAccountService,
    CancelSubscribeRecordService,
    ChipBasicInfoService,
    ChipInstitutionHoldingInfoService,
    ContentService,
    CumulativeRoiService,
    DividendIndicatorService,
    EarlyWarningService,
    FamousInvestorStatusService,
    FearGreedService,
    HistoricalDividendService,
    HistoricalRatingService,
    HistoricalSymbolPriceService,
    IndicatorResultService,
    InsiderBuyingInfoService,
    InstitutionExclusiveOffersService,
    InvestorRankingService,
    LineWebhookService,
    MarketSentimentService,
    NikeCustomerInfoService,
    NormalAccountService,
    PushNotificationRecordService,
    RoboAvailableService,
    RoboNotificationService,
    ScreenerService,
    SearchSymbolService,
    StockMiningServiceStatus,
    StripeService,
    StripeSessionInfoService,
    StripeSubscribeInfoService,
    StripeWebhookService,
    SymbolInfoService,
    SymbolService,
    SystemMailer,
    TradingviewAccountService,
    TrendIndicatorService,
    UpdatedAtUtils,
    ValueIndicatorService,
    VideoInfoService,
    WatchlistServiceFacade,
]


class BindingSpec(pinject.BindingSpec):
    """Binding setup"""

    def __init__(self, app: Flask):
        self.app = app

    def configure(self, bind):
        bind('app', to_instance=self.app)
        bind('cache', to_instance=self.app.rediscache)
        bind('config', to_instance=Config())
        bind('logger', to_instance=self.app.logger)
        bind('user_sql_session', to_instance=self.app.userDBSession)

    @pinject.provides(in_scope=pinject.SINGLETON)
    def provide_cronjob(self) -> paramiko.SSHClient():
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                hostname=Config().CRONJOB_HOST, username=Config().CRONJOB_USER, password=Config().CRONJOB_PWD)
        except Exception as e:
            print(f"[!] Cannot connect to the SSH Server. \n {e}")  # noqa : T201
            exit()

        return client

    @pinject.provides(in_scope=pinject.SINGLETON)
    def provide_photo_storage(self) -> IFileStorage:
        if self.app.config.get("STORAGE_DRIVER") == "s3":
            kwargs = dict(
                bucket=self.app.config["UPLOAD_S3_BUCKET"],
                base_prefix="/",
                aws_region=self.app.config.get("S3_AWS_REGION") or "us-west-1"
            )
            if self.app.config.get("S3_AWS_KID"):
                kwargs["aws_access_key_id"] = self.app.config["S3_AWS_KID"]
                kwargs["aws_secret_access_key"] = self.app.config["S3_AWS_KEY"]
            return S3FileStorage(kwargs)

        local_storage_path = os.path.abspath(os.path.join(
            self.app.config["LOCAL_FOLDER_AS_S3"], "growin-manager-files"))
        return LocalFileStorage(local_storage_path)
