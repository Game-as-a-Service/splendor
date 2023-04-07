from flask import Flask
from flask_restful import Api

from api.routes.account.api_business_account_login import ApiBusinessAccountLogin
from api.routes.account.api_generate_business_account import ApiGenerateBusinessAccount
from api.routes.account.api_line_account_link import ApiLineAccountLink
from api.routes.account.api_line_account_link_status import ApiLineAccountLinkStatus
from api.routes.account.api_logout import ApiLogout
from api.routes.account.api_user_profile import ApiUserProfile
from api.routes.account.api_user_subscription_plan import ApiUserSubscriptionPlan
from api.routes.api_ai_sector_optional import ApiAiSectorOptional
from api.routes.api_backtest_action import ApiBacktestAction
from api.routes.api_backtest_result import ApiBacktestResult
from api.routes.api_chip_basic_info import ApiChipBasicInfo
from api.routes.api_chip_institution_holding_info import ApiChipInstitutionHoldingInfo
from api.routes.api_content import ApiContent
from api.routes.api_cumulative_roi import ApiCumulativeRoi
from api.routes.api_default_search_symbol import ApiDefaultSearchSymbol
from api.routes.api_famous_investor_status import ApiFamousInvestorStatus
from api.routes.api_historical_rating import ApiHistoricalRating
from api.routes.api_home import ApiHome
from api.routes.api_insider_buying_info import ApiInsiderBuyingInfo
from api.routes.api_institution_exclusive_offers import ApiInstitutionExclusiveOffers
from api.routes.api_investor_ranking import ApiInvestorRanking
from api.routes.api_online_symbols import ApiOnlineSymbols
from api.routes.api_preview import ApiPreview
from api.routes.api_related_symbol import ApiRelatedSymbol
from api.routes.api_screener import ApiScreener
from api.routes.api_screener_option import ApiScreenerOption
from api.routes.api_search_symbol import ApiSearchSymbol
from api.routes.api_stock_mining_service_status import ApiStockMiningServiceStatus
from api.routes.api_subscribe_plan import ApiSubscribePlan
from api.routes.api_symbol_dividend_indicator import ApiSymbolDividendIndicator
from api.routes.api_symbol_historical_dividend import ApiSymbolHistoricalDividend
from api.routes.api_symbol_info import ApiSymbolInfo
from api.routes.api_symbol_price import ApiSymbolPrice
from api.routes.api_symbol_trend_indicator import ApiSymbolTrendIndicator
from api.routes.api_symbol_value_indicator import ApiSymbolValueIndicator
from api.routes.api_symbols_score import ApiSymbolsScore
from api.routes.api_tradingview_account import ApiTradingviewAccount
from api.routes.api_trend_performance import ApiTrendPerformance
from api.routes.api_video_info import ApiVideoInfo
from api.routes.line.api_line_webhook import ApiLineWebhook
from api.routes.market_sentiment.early_warning.api_early_warning_current import ApiEarlyWarningCurrent
from api.routes.market_sentiment.early_warning.api_early_warning_historical_details import \
    ApiEarlyWarningHistoricalDetails
from api.routes.market_sentiment.early_warning.api_early_warning_historical_signals import \
    ApiEarlyWarningHistoricalSignals
from api.routes.market_sentiment.early_warning.api_early_warning_recent_signals import ApiEarlyWarningRecentSignals
from api.routes.market_sentiment.fear_and_greed.api_fear_and_greed_current import ApiFearAndGreedCurrent
from api.routes.market_sentiment.fear_and_greed.api_fear_and_greed_historical import ApiFearAndGreedHistorical
from api.routes.market_sentiment.fear_and_greed.api_fear_and_greed_reversal_signal import ApiFearAndGreedReversalSignal
from api.routes.notificaiton.api_notification_record import ApiNotificationRecord
from api.routes.notificaiton.api_notification_record_read import ApiNotificationRecordRead
from api.routes.notificaiton.api_notification_robo import ApiNotificationRobo
from api.routes.notificaiton.api_notification_robo_status import ApiNotificationRoboStatus
from api.routes.open_api_spec import OpenApiSpec
from api.routes.stripe.api_stripe_customer_portal import ApiStripeCustomerPortal
from api.routes.stripe.api_stripe_customer_portal_update_page import ApiStripeCustomerPortalUpdatePage
from api.routes.stripe.api_stripe_webhook import ApiStripeWebhook
from api.routes.watchlist.api_watchlist import ApiWatchlist
from api.routes.watchlist.api_watchlist_reorder import ApiWatchlistReorder
from api.routes.watchlist.api_watchlist_symbol import ApiWatchlistSymbol
from config.api_config import Config


def setup_routes(app: Flask):
    if Config.ENV_SET.lower() in ["dev", 'local']:
        @app.route('/open-api-spec', defaults={'path': None})
        @app.route('/open-api-spec/', defaults={'path': None})
        @app.route('/open-api-spec/<path:path>')
        def send_open_api_spec(path: str):
            return OpenApiSpec.resolve_content(path)

    api = Api(app)
    api.add_resource(ApiHome, "/")
    api.add_resource(ApiPreview, "/preview/chip/KO")

    # 個股探勘服務狀態
    api.add_resource(ApiStockMiningServiceStatus, "/stock-mining-service/<service>")

    # 官網
    api.add_resource(ApiAiSectorOptional, "/official-website/ai-sector-optional/<oriented>")

    # User 相關
    api.add_resource(ApiLogout, "/logout")
    api.add_resource(ApiUserProfile, "/user")
    api.add_resource(ApiTradingviewAccount, "/tradingview/account")
    api.add_resource(ApiUserSubscriptionPlan, "/user/subscription/plan")
    api.add_resource(ApiLineAccountLink, "/line/account-link")
    api.add_resource(ApiLineAccountLinkStatus, "/line/account-link/status")

    # Business User
    api.add_resource(ApiBusinessAccountLogin, "/business/login")
    api.add_resource(ApiGenerateBusinessAccount, "/business/generate/user")

    # Watchlist 相關
    api.add_resource(ApiWatchlist, "/watchlist", "/watchlist/<watchlist_id>")
    api.add_resource(ApiWatchlistSymbol, "/watchlist/<watchlist_id>/<symbol>")
    api.add_resource(ApiWatchlistReorder, "/watchlist/reorder/<watchlist_id>")

    # 搜尋
    api.add_resource(ApiSearchSymbol, "/search/symbol/<keyword>")
    api.add_resource(ApiDefaultSearchSymbol, "/default/search/symbol")

    # Symbol
    api.add_resource(ApiOnlineSymbols, "/online-symbols", "/online-symbols/<oriented>")
    api.add_resource(ApiSymbolInfo, "/symbol-info/<symbol>")
    api.add_resource(ApiRelatedSymbol, "/related-symbol/<symbol>")
    api.add_resource(ApiSymbolsScore, "/symbol/score")

    # 篩選器
    api.add_resource(ApiScreenerOption, "/screener/option")
    api.add_resource(ApiScreener, "/screener")

    # 回測
    api.add_resource(ApiBacktestAction, "/backtest-action/<symbol>/<oriented>/<strategy>/<start_at>/<end_at>")
    api.add_resource(ApiBacktestResult, "/backtest-result/<symbol>/<oriented>/<strategy>")
    api.add_resource(ApiTrendPerformance, "/trend-performance/<symbol>")
    api.add_resource(ApiCumulativeRoi, "/cumulative-roi/<symbol>/<oriented>/<strategy>/<end_at>")

    # 機構
    api.add_resource(ApiChipBasicInfo, "/chip-basic-info/<symbol>")
    api.add_resource(ApiChipInstitutionHoldingInfo, "/chip-institution-holding-info/<symbol>")
    api.add_resource(ApiInsiderBuyingInfo, "/insider-buying-info/<symbol>/<page>/<page_size>")
    api.add_resource(ApiInvestorRanking, "/investor-ranking/<symbol>/<int:page>/<int:page_size>")
    api.add_resource(ApiFamousInvestorStatus, "/famous-investor-status/<symbol>")

    # 文案
    api.add_resource(ApiContent, "/content/<symbol>/<oriented>/<info>")

    # 指標
    api.add_resource(ApiSymbolDividendIndicator, "/dividend-indicator/<symbol>")
    api.add_resource(ApiSymbolTrendIndicator, "/trend-indicator/<symbol>")
    api.add_resource(ApiSymbolValueIndicator, "/value-indicator/<symbol>/<indicator>")

    # 歷史資料
    api.add_resource(ApiHistoricalRating, "/historical-rating/<symbol>/<oriented>")
    api.add_resource(ApiSymbolHistoricalDividend, "/historical-dividend/<symbol>/<nums>")
    api.add_resource(ApiSymbolPrice, "/symbol/price/<symbol>/<start_at>/<end_at>")

    # Stripe 相關
    api.add_resource(ApiSubscribePlan, "/subscribe/plan")
    api.add_resource(ApiStripeWebhook, "/stripe/webhook")
    api.add_resource(ApiStripeCustomerPortal, "/stripe/customer-portal")
    api.add_resource(ApiStripeCustomerPortalUpdatePage, "/stripe/customer-portal-update-page")

    # Line 相關
    api.add_resource(ApiLineWebhook, "/line/webhook")

    # 影音資訊相關
    api.add_resource(ApiVideoInfo, "/video-info/<category>")

    # 機構專屬優惠
    api.add_resource(ApiInstitutionExclusiveOffers, "/institution-exclusive-offers/<institution>/<collaborate>")

    # 推播
    api.add_resource(ApiNotificationRecord, "/notification/record/<int:page>/<int:page_size>",
                     "/notification/record/<int:id>", "/notification/record", endpoint="record")
    api.add_resource(ApiNotificationRecordRead, "/notification/record/unread")
    api.add_resource(ApiNotificationRobo, "/notification/robo", "/notification/robo/<int:id>")
    api.add_resource(ApiNotificationRoboStatus, "/notification/robo-status/<int:id>")

    # 市場關鍵數據
    # 市場恐懼貪婪指標
    api.add_resource(ApiFearAndGreedReversalSignal, "/market-sentiment/fear-and-greed/reversal-signal")
    api.add_resource(ApiFearAndGreedHistorical, '/market-sentiment/fear-and-greed/historical')
    api.add_resource(ApiFearAndGreedCurrent, '/market-sentiment/fear-and-greed/current')

    # 市場預警燈號
    api.add_resource(ApiEarlyWarningCurrent, '/market-sentiment/early-warning/current')
    api.add_resource(ApiEarlyWarningRecentSignals, '/market-sentiment/early-warning/recent-signals')
    api.add_resource(ApiEarlyWarningHistoricalSignals, "/market-sentiment/early-warning/historical-signals")
    api.add_resource(ApiEarlyWarningHistoricalDetails,
                     "/market-sentiment/early-warning/historical-details/<signal>/<int:page>/<int:page_size>")
