# Generated by Django 3.1.5 on 2021-02-14 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shiritori', '0007_auto_20210205_2021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shiritorigame',
            name='name',
        ),
    ]
