# Generated by Django 3.0.8 on 2020-07-10 19:22

import django.db.models.deletion
from django.db import migrations, models

import codertheory.shiritori.models
import codertheory.general.custom_fields
import codertheory.general.generator


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', codertheory.general.custom_fields.NanoIDField(auto_created=True,
                                                                     default=codertheory.general.generator.generate_id,
                                                                     editable=False, max_length=10, primary_key=True,
                                                                     serialize=False)),
                ('name', models.CharField(max_length=512)),
                ('password', models.CharField(max_length=5, null=True)),
                ('started', models.BooleanField(default=False)),
                ('last_word',
                 models.CharField(default=codertheory.shiritori.models.random_letter_generator, max_length=512,
                                  null=True)),
                ('finished', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', codertheory.general.custom_fields.NanoIDField(auto_created=True,
                                                                     default=codertheory.general.generator.generate_id,
                                                                     editable=False, max_length=10, primary_key=True,
                                                                     serialize=False)),
                ('name', models.CharField(max_length=512)),
                ('score', models.IntegerField(default=100)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shiritori.Game')),
            ],
        ),
        migrations.CreateModel(
            name='GameWord',
            fields=[
                ('id', codertheory.general.custom_fields.NanoIDField(auto_created=True,
                                                                     default=codertheory.general.generator.generate_id,
                                                                     editable=False, max_length=10, primary_key=True,
                                                                     serialize=False)),
                ('word', models.CharField(max_length=512)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shiritori.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shiritori.Player')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='current_player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='current_player_game', to='shiritori.Player'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.UniqueConstraint(fields=('game', 'name'), name='unique_name_per_game'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.UniqueConstraint(fields=('game', 'id'), name='unique_player_per_game'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='player',
            order_with_respect_to='game',
        ),
        migrations.AddConstraint(
            model_name='gameword',
            constraint=models.UniqueConstraint(fields=('word', 'game'), name='unique_word_per_game'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='gameword',
            order_with_respect_to='game',
        ),
    ]
