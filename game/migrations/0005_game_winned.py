# Generated by Django 3.2.13 on 2022-04-18 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20220418_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winned',
            field=models.BooleanField(default=False),
        ),
    ]
