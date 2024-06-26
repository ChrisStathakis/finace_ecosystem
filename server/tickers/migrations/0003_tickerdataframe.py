# Generated by Django 4.2 on 2024-01-06 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0002_alter_ticker_simply_return'),
    ]

    operations = [
        migrations.CreateModel(
            name='TickerDataFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('close', models.DecimalField(decimal_places=2, max_digits=10)),
                ('volume', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticker_df', to='tickers.ticker')),
            ],
        ),
    ]
