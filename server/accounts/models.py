from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    starting_value = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)
    current_value = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)
    withdraw_value = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)
    historic_value = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        qs = self.user.portfolios.all()
        self.starting_value = qs.aggregate(Sum("starting_investment"))["starting_investment__sum"] or 0
        self.starting_value = qs.aggregate(Sum("current_value"))["current_value__sum"] or 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username