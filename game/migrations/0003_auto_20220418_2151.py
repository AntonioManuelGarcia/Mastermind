# Generated by Django 3.2.13 on 2022-04-18 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20220418_2114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guest',
            old_name='code',
            new_name='guest_code',
        ),
        migrations.AddField(
            model_name='game',
            name='code',
            field=models.CharField(blank=True, max_length=4),
        ),
    ]
