from rest_framework import serializers
from rest_framework.reverse import reverse
from ..models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    profile_link = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "email", "id", "profile_link"]

    def get_profile_link(self, obj):
        result = '{}'.format(reverse('profile:profile_view', request=self.context.get('request')),)
        return result


class ProfileSerializer(serializers.ModelSerializer):
    historic_withdraw_value = serializers.SerializerMethodField()
    earnings = serializers.SerializerMethodField()
    withdraw_earnings = serializers.SerializerMethodField()
    historic_earnings = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user',
                  'starting_value',
                  'current_value',
                  'starting_withdraw_value',
                  'withdraw_value',
                  "historic_withdraw_value",
                  "historic_value",
                  "portfolio_id",
                  "earnings",
                  "withdraw_earnings",
                  "historic_earnings"
                  ]

    def get_historic_withdraw_value(self, obj):
        return obj.starting_withdraw_value + obj.starting_value

    def get_earnings(self, obj: Profile):
        return obj.current_value - obj.starting_value

    def get_withdraw_earnings(self, obj: Profile):
        return obj.withdraw_value - obj.starting_withdraw_value

    def get_historic_earnings(self, obj: Profile):
        return self.get_withdraw_earnings(obj) + self.get_earnings(obj)


