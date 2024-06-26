from django.db import models
from django.db.models.functions import Coalesce


class PortfolioManager(models.Manager):

    def user_portfolios(self, user):
        return self.filter(user=user).all()

    def total_earnings(self, user=None):
        if user:
            self.filter(user=user).aggregate(models.Sum('current_value'))['current_value__sum'] or 0
        # return self.aggregate(earnings=Coalesce(models.Sum('current_value'), 0))
        return self.aggregate(models.Sum('current_value'))['current_value__sum'] or 0


    def total_simply_return(self, user=None):
        if user:
            self.filter(user=user).aggregate(models.Sum('annual_returns'))['annual_returns__sum'] or 0
        return self.aggregate(models.Sum('annual_returns'))['annual_returns__sum'] or 0
