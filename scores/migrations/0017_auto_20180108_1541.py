# Generated by Django 2.0.1 on 2018-01-08 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0016_name_known_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='name',
            name='id',
            field=models.CharField(max_length=9, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='title',
            name='id',
            field=models.CharField(max_length=9, primary_key=True, serialize=False),
        ),
    ]
