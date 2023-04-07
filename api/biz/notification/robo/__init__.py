REQUIRED = [
    "strategyName",
    "strategyCategory",
    "notificationMethod",
    "finishedAt",
    "symbols",
    "settingType",
    "advancedSettings"
]

OPTIONAL = [
    "value",
    "trend",
    "swing",
    "chip",
    "dividend",
    "surfingTrendDaily",
    "surfingTrendWeekly",
    "squeezeDaily",
    "squeezeWeekly",
    "marketCap",
    "greaterThanVolume20MA",
    "lessThanVolume20MA"
]

STRATEGY_CATEGORY = [
    "buy",
    "sell"
]

NOTIFICATION_METHODS = [
    "email",
    "line"
]

SETTING_TYPE = [
    "custom",
    "value-robo",
    "swing-robo",
    "trend-robo"
]

VARIATION = [
    "crossing-up",
    "crossing-down",
    "greater-than-equal",
    "less-than-equal"
]

SCORE = [1, 2, 3, 4, 5]

SURFING_TREND = [
    "neg2pos",
    "pos2neg",
    "moving-up",
    "moving-down"
]

SQUEEZE_ACTION = [
    "energy-accumulate",
    "energy-fire"
]

SQUEEZE = [
    "any",
    "up",
    "down"
]

SQUEEZE_ENERGY = [0, 1, 2, 3]

MARKET_CAP = [
    "micro-stock",
    "small-stock",
    "medium-stock",
    "large-stock"
]
