# Generated by Django 2.1.3 on 2019-01-03 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20190101_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]