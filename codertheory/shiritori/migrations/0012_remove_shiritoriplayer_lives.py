# Generated by Django 3.1.5 on 2021-03-11 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shiritori', '0011_shiritorigame_timer_expiry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shiritoriplayer',
            name='lives',
        ),
    ]
