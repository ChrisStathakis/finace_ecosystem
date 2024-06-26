# Generated by Django 4.2 on 2024-01-22 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0007_alter_portfolio_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='price_avg',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=30),
        ),
    ]
