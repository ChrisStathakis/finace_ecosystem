# Generated by Django 4.2 on 2024-08-16 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0017_remove_portfolio_maximum_cash_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='wikipedia_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=240)),
                ('label', models.CharField(max_length=240)),
            ],
            options={
                'unique_together': {('title', 'label')},
            },
        ),
    ]
