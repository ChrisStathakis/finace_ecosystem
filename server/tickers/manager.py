from django.db import models
from django.db.models.functions import Coalesce


class TickerManager(models.Manager):

    def first_page_tickers(self):
        return self.order_by("-simply_return")[:16]



