from rest_framework import serializers

from ..models import Profile, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "id"]




class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'user', 'starting_value', 'current_value', 
                  'withdraw_value', "historic_value", "portfolio_id"
                  ]
