# Generated by Django 2.0.1 on 2018-01-05 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0005_auto_20180104_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='is_adult',
            field=models.IntegerField(),
        ),
    ]