# Generated by Django 2.2.5 on 2019-09-28 00:37

from django.db import migrations, models
import django.db.models.deletion


def seed(apps, editor):
    MarketType = apps.get_model('market', 'MarketType')
    Market = apps.get_model('market', 'Market')
    cryptocurrency = MarketType.objects.get(name='cryptocurrency')
    Market.objects.create(name='BTCUSDT', market_type=cryptocurrency)


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('market_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='market.MarketType')),
            ],
        ),
        migrations.RunPython(seed),
    ]
