# Generated by Django 2.0.1 on 2018-01-05 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0008_auto_20180104_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='name',
            name='professions',
            field=models.TextField(null=True),
        ),
    ]
