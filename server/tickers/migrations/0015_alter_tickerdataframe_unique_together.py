# Generated by Django 4.2 on 2024-07-07 00:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0014_ticker_date_predict_ticker_prediction'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tickerdataframe',
            unique_together={('ticker', 'date')},
        ),
    ]
