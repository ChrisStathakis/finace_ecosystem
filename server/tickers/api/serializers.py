from rest_framework import serializers
from ..models import Ticker, TickerDataFrame
from portfolio.models import Portfolio, UserTicker

class PortfolioSerializer(serializers.ModelSerializer):
    difference = serializers.DecimalField(max_digits=10, decimal_places=2, source="show_diff")
    diff_percent = serializers.DecimalField(max_digits=10, decimal_places=2, source="show_diff_percent")

    class Meta:
        model = Portfolio
        fields = ['id', "is_public", "date_investment", 
                  "title", "user", "annual_returns", "variance",
                  "starting_investment", "current_value", 
                  "difference", "diff_percent", "withdraw_value"
                  
                  ]


class TickerDataFrameSerializer(serializers.ModelSerializer):

    class Meta:
        model = TickerDataFrame
        fields = ["ticker", "date", "close", "pct_change"]



class UserTickerEditSerializier(serializers.ModelSerializer):

    class Meta:
        model = UserTicker
        fields = ["id", "ticker", "portfolio", 
                  "starting_investment", "qty", "current_value", "is_sell"
                  ]




class UserTickerBaseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="ticker.title")
    code = serializers.CharField(source="ticker.ticker")
    difference = serializers.DecimalField(source="tag_diff", decimal_places=2, max_digits=10)
    diff_percent = serializers.DecimalField(source="tag_diff_pct", decimal_places=2, max_digits=10
                                            )

    class Meta:
        model = UserTicker
        fields = ["id", 'title', "ticker", "portfolio", "starting_investment", "qty", 
                  "code", "current_value", "difference", "diff_percent",
                  "is_sell",
                  
                  ]



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