from rest_framework import serializers
from ..models import Ticker, TickerDataFrame, Portfolio, UserTicker


class PortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = ['id', "is_public", "date_investment", 
                  "title", "user", "annual_returns", "variance",
                  "starting_investment", "current_value", "maximum_cash",


                  ]


class TickerDataFrameSerializer(serializers.ModelSerializer):

    class Meta:
        model = TickerDataFrame
        fields = ["ticker", "date", "close", "pct_change"]





class UserTickerBaseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="ticker.title")
    code = serializers.CharField(source="ticker.ticker")

    class Meta:
        model = UserTicker
        fields = ["id", 'title', "ticker", "portfolio", "starting_investment", "qty", "code", "current_value"]



class TickerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticker
        fields = ['id', 'title', 'ticker', 'indices', 'beta', 'coverage', 'market_variance',
                  'camp', 'price', 'simply_return', 'log_return', 'standard_deviation',
                  'sharp'
                  ]
        



class TickerPredictionSerializer(serializers.ModelSerializer):
    my_predict = serializers.SerializerMethodField()

    class Meta:
        model = Ticker
        fields = ['id', "my_predict"]

    def get_my_predict(self, obj):
        return obj.predict_next_days()