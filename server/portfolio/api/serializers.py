from rest_framework import serializers

from ..models import UserTicker, Portfolio


class PortfolioSerializer(serializers.ModelSerializer):
    difference = serializers.DecimalField(max_digits=10, decimal_places=2, source="show_diff")
    diff_percent = serializers.DecimalField(max_digits=10, decimal_places=2, source="show_diff_percent")

    class Meta:
        model = Portfolio
        fields = ['id', "is_public", "date_investment",
                  "title", "user", "annual_returns", "variance",
                  "starting_investment", "current_value",
                  "difference", "diff_percent", "withdraw_value",


                  ]


class UserTickerBaseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="ticker.title")
    code = serializers.CharField(source="ticker.ticker")
    difference = serializers.DecimalField(source="diff_value", decimal_places=2, max_digits=10)
    diff_percent = serializers.DecimalField(source="diff_pct", decimal_places=2, max_digits=10)
    starting_investment = serializers.DecimalField(decimal_places=2, max_digits=10)
    starting_value_of_ticker = serializers.DecimalField(decimal_places=2, max_digits=10)
    qty = serializers.DecimalField(decimal_places=2, max_digits=10)
    current_value = serializers.DecimalField(decimal_places=2, max_digits=10)
    ticker_status = serializers.SerializerMethodField()
    winning_loosing_situation = serializers.SerializerMethodField()
    current_value_of_ticker = serializers.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        model = UserTicker
        fields = ["id", 'title', "portfolio", "starting_investment", "qty", "ticker",
                  "current_value", "difference", "diff_percent",
                  "is_sell", "timestamp", "ticker_status",
                  "starting_value_of_ticker", "current_value_of_ticker",
                  "code", "winning_loosing_situation"
                  ]

    def get_ticker_status(self, obj: UserTicker):
        if obj.is_sell:
            return "Sell"
        return "Active"

    def get_winning_loosing_situation(self, obj: UserTicker):
        return obj.tag_winning_loosing_situation()


class UserTickerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTicker
        fields = [
            "ticker", "portfolio", "starting_value_of_ticker", "starting_investment", "current_value"
        ]


class UserTickerEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTicker
        fields = ["id", "ticker", "portfolio",
                  "starting_investment", "qty", "current_value", "is_sell"
                  ]


class UserTickerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTicker
        fields = ["id", ]