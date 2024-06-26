from django.apps import AppConfig


class TickersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tickers'

    def ready(self):
        import tickers.signals
        import server.celery