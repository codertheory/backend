# Generated by Django 3.1.5 on 2021-03-12 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shiritori', '0012_remove_shiritoriplayer_lives'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shiritorigame',
            name='timer_expiry',
        ),
    ]
