# Generated by Django 3.2 on 2021-04-16 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shiritori', '0013_remove_shiritorigame_timer_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiritorigame',
            name='timer',
            field=models.PositiveSmallIntegerField(default=10),
        ),
    ]