# Generated by Django 3.2.13 on 2022-07-23 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20220723_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='leg',
            name='winner',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='visit',
            name='throw1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='visit',
            name='throw2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='visit',
            name='throw3',
            field=models.IntegerField(default=0),
        ),
    ]