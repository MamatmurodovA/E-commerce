# Generated by Django 2.1.3 on 2019-01-11 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20190108_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(choices=[('within_one_day', '24 соат ичида'), ('express_delivery', 'Тезкор етказиб бериш')], default='within_one_day', max_length=120),
        ),
    ]
