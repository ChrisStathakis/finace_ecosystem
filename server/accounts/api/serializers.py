from rest_framework import serializers

from ..models import Profile, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "id"]


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'user', 'current_investment', 'current_value',
                  'historic_investment', "historic_value", "portfolio_id"
                  ]
