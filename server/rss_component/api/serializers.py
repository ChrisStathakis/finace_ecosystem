from rest_framework import serializers

from ..models import RssFeed



class RssFeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = RssFeed
        fields = ['id', 'title', 'published', "summary", "tickers", "is_analysed", "is_positive"]