# Generated by Django 3.2.13 on 2022-07-23 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20220723_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='leg',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visit',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
