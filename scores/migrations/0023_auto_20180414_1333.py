# Generated by Django 2.0.1 on 2018-04-14 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0022_name_in_graph'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='original_title',
        ),
        migrations.RemoveField(
            model_name='title',
            name='runtime_minutes',
        ),
        migrations.AddField(
            model_name='name',
            name='lowercase_name',
            field=models.CharField(db_index=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='name',
            name='primary_name',
            field=models.CharField(max_length=200),
        ),
    ]
