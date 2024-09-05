from rest_framework import serializers

from ..models import UserTicker
class UserTickerSerializer(serializers.ModelSerializer):

    class Meta:
        model =