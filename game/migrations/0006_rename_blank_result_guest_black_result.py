# Generated by Django 3.2.13 on 2022-04-18 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_game_winned'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guest',
            old_name='blank_result',
            new_name='black_result',
        ),
    ]
