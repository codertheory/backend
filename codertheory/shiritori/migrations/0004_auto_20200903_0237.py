# Generated by Django 3.1.1 on 2020-09-03 02:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('shiritori', '0003_game_timer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Game',
            new_name='ShiritoriGame',
        ),
        migrations.RenameModel(
            old_name='GameWord',
            new_name='ShiritoriGameWord',
        ),
        migrations.RenameModel(
            old_name='Player',
            new_name='ShiritoriPlayer',
        ),
    ]
