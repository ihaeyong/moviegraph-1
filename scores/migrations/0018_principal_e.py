# Generated by Django 2.0.1 on 2018-01-09 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0017_auto_20180108_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='principal',
            name='e',
            field=models.BooleanField(default=False),
        ),
    ]
