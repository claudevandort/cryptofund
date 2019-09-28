# Generated by Django 2.2.5 on 2019-09-28 00:36

from django.db import migrations, models


def seed(apps, editor):
    MarketType = apps.get_model('market', 'MarketType')
    MarketType.objects.create(name='cryptocurrency')


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MarketType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'market_market_type',
            },
        ),
        migrations.RunPython(seed),
    ]
