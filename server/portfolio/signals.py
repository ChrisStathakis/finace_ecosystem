from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserTicker
from decimal import Decimal

"""

@receiver(post_save, sender=UserTicker)
def update_user_ticker_price(sender, instance: UserTicker, created, **kwargs):
    if created:
        current_value_of_ticker = instance.ticker.price if instance.starting_value_of_ticker == 0 \
            else instance.starting_value_of_ticker
        current_value = Decimal(instance.qty) * Decimal(instance.current_value_of_ticker)
        UserTicker.objects.filter(id=instance.id).update(
            current_value_of_ticker=current_value_of_ticker,
            current_value=current_value
        )
    instance.qty = instance.starting_investment / instance.starting_value_of_ticker if instance.starting_value_of_ticker != 0 else 0
    instance.current_value_of_ticker = instance.ticker.price
    instance.current_value = Decimal(instance.qty) * Decimal(instance.current_value_of_ticker)


"""