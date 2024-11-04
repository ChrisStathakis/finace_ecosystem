from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.conf import settings

CURRENCY = settings.CURRENCY
User = get_user_model()


class Profile(models.Model):
    """
        current_investment:

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_investment = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)
    current_value = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)
    historic_investment = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)
    historic_value = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        qs = self.user.port.port_tickers.all()
        self.current_investment = qs.filter(is_sell=False).aggregate(Sum("starting_investment"))[
                                      "starting_investment__sum"] or 0
        self.current_value = qs.filter(is_sell=False).aggregate(Sum("current_value"))["current_value__sum"] or 0

        self.historic_investment = qs.aggregate(Sum("starting_investment"))[
                                      "starting_investment__sum"] or 0
        self.historic_value = qs.aggregate(Sum("current_value"))["current_value__sum"] or 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def tag_current_investment(self):
        return f"{round(self.current_investment, 2)} {CURRENCY}"

    def tag_current_value(self):
        return f"{round(self.current_value, 2)} {CURRENCY}"

    def tag_current_diff(self):
        return f"{round(self.current_value - self.current_investment, 2)} {CURRENCY}"

    def tag_investment(self):
        return f"{round(self.historic_investment, 2)} {CURRENCY}"

    def tag_value(self):
        return f"{round(self.historic_value -  self.historic_value, 2)} {CURRENCY}"

    def tag_diff(self):
        return f"{round(self.current_investment - self.historic_investment, 2)} {CURRENCY}"



    @property
    def portfolio_id(self):
        return self.user.port.id


