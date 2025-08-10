from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.conf import settings

CURRENCY = settings.CURRENCY
User = get_user_model()


class Profile(models.Model):
    """
        starting_value: is the current value you deposit on active tickers
        current_value: is the current value after the profit/loss of the tickers
        starting_withdraw_value: is the deposit value of the tickers already selled
        withdraw_value: is the total value of the tickers you have withdraw
        historic_value: is all the values together
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    starting_value = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)
    current_value = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)
    starting_withdraw_value = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)
    withdraw_value = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)
    historic_value = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        qs = self.user.port.port_tickers.all()
        self.starting_value = qs.filter(is_sell=False).aggregate(Sum("starting_investment"))\
                                  ["starting_investment__sum"] or 0
        self.current_value = qs.filter(is_sell=False).aggregate(Sum("current_value"))["current_value__sum"] or 0
        self.starting_withdraw_value = qs.filter(is_sell=True).aggregate(Sum("starting_investment"))\
                                          ["starting_investment__sum"] or 0
        self.withdraw_value = qs.filter(is_sell=True).aggregate(Sum("current_value"))["current_value__sum"] or 0
        self.historic_value = self.current_value + self.withdraw_value
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def tag_withdraw_starting_value(self):
        return f"{round(self.starting_withdraw_value, 2)} {CURRENCY}"

    def tag_withdraw_value(self):
        return f"{round(self.withdraw_value, 2)} {CURRENCY}"

    def tag_withdraw_earnings(self):
        earnings = self.withdraw_value - self.starting_withdraw_value
        return f"{round(earnings, 2)} {CURRENCY}"

    def tag_starting_value(self):
        return f"{round(self.starting_value, 2)} {CURRENCY}"

    def tag_current_value(self):
        return f"{round(self.current_value, 2)} {CURRENCY}"

    def tag_earnings(self):
        earnings = self.current_value - self.starting_value
        return f"{round(earnings, 2)} {CURRENCY}"

    def tag_historic_deposits(self):
        return f"{round(self.starting_withdraw_value + self.starting_value, 2)} {CURRENCY}"

    def tag_historic_value(self):
        return f"{round(self.historic_value, 2)} {CURRENCY}"

    def tag_historic_earnings(self):
        return f"{round(self.historic_value - self.starting_value - self.starting_withdraw_value, 2)} {CURRENCY}"

    @property
    def portfolio_id(self):
        return self.user.port.id


