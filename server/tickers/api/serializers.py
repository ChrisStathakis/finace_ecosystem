from rest_framework import serializers
from ..models import Ticker, TickerDataFrame
from portfolio.models import Portfolio, UserTicker


class TickerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticker
        fields = ['title', 'ticker', 'indices']



class TickerDataFrameSerializer(serializers.ModelSerializer):

    class Meta:
        model = TickerDataFrame
        fields = ["ticker", "date", "close", "pct_change"]







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