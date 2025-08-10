from django.test import TestCase

# Create your tests here.

from .models import Ticker


class TickerTestCase(TestCase):

    def setUp(self):
        self.ticker = Ticker.objects.create(
            title="MICROSOFT",
            ticker="MSFT"
        )
        self.ticker.soft_update()
        self.ticker.hard_update()

    def test_ticker_data(self):
        print(self.ticker)