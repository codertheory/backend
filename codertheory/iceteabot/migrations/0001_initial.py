# Generated by Django 3.1.1 on 2020-09-06 23:31

import django.db.models.deletion
from django.db import migrations, models

import codertheory.utils.custom_fields
import codertheory.utils.generator


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordChannel',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('blocked', models.BooleanField(default=False)),
                ('blocked_reason', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiscordGuild',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('tracking', models.BooleanField(default=True)),
                ('premium', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiscordUser',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('blocked', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True,
                                                                   default=codertheory.utils.generator.generate_id,
                                                                   editable=False, max_length=10, primary_key=True,
                                                                   serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('content', models.CharField(max_length=1500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_edited', models.DateTimeField(null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                             to='iceteabot.discorduser')),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceteabot.discordguild')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True,
                                                                   default=codertheory.utils.generator.generate_id,
                                                                   editable=False, max_length=10, primary_key=True,
                                                                   serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('finished', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceteabot.discorduser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TagLookUp',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True,
                                                                   default=codertheory.utils.generator.generate_id,
                                                                   editable=False, max_length=10, primary_key=True,
                                                                   serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                             to='iceteabot.discorduser')),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceteabot.discordguild')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceteabot.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TagCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('called_at', models.DateTimeField(auto_now_add=True)),
                ('channel',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceteabot.discordchannel')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceteabot.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True,
                                                                   default=codertheory.utils.generator.generate_id,
                                                                   editable=False, max_length=10, primary_key=True,
                                                                   serialize=False)),
                ('message', models.CharField(max_length=1500)),
                ('event', models.CharField(max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires', models.DateTimeField()),
                ('channel',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceteabot.discordchannel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceteabot.discorduser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReactionRole',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True,
                                                                   default=codertheory.utils.generator.generate_id,
                                                                   editable=False, max_length=10, primary_key=True,
                                                                   serialize=False)),
                ('message_id', models.BigIntegerField()),
                ('emoji', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('role_id', models.BigIntegerField()),
                ('guild',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discordguild')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NickName',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True,
                                                                   default=codertheory.utils.generator.generate_id,
                                                                   editable=False, max_length=10, primary_key=True,
                                                                   serialize=False)),
                ('name', models.TextField()),
                ('changed_at', models.DateTimeField(auto_now_add=True)),
                ('member',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discorduser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True,
                                                                   default=codertheory.utils.generator.generate_id,
                                                                   editable=False, max_length=10, primary_key=True,
                                                                   serialize=False)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uses', models.IntegerField(default=0)),
                ('author',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discorduser')),
                ('guild',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discordguild')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiscordResponse',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True,
                                                                   default=codertheory.utils.generator.generate_id,
                                                                   editable=False, max_length=10, primary_key=True,
                                                                   serialize=False)),
                ('content', models.TextField()),
                ('author',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discorduser')),
                ('channel',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discordchannel')),
                ('guild',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discordguild')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiscordMember',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('administrator', models.BooleanField(default=False)),
                ('guild',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discordguild')),
            ],
        ),
        migrations.AddField(
            model_name='discordchannel',
            name='guild',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discordguild'),
        ),
        migrations.CreateModel(
            name='CommandPrefix',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True,
                                                                   default=codertheory.utils.generator.generate_id,
                                                                   editable=False, max_length=10, primary_key=True,
                                                                   serialize=False)),
                ('prefix', models.CharField(max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('guild',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discordguild')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommandCall',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('command', models.CharField(max_length=100)),
                ('called_at', models.DateTimeField(auto_now_add=True)),
                ('author',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discorduser')),
                ('guild',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discordguild')),
                ('prefix',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.commandprefix')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True,
                                                                   default=codertheory.utils.generator.generate_id,
                                                                   editable=False, max_length=10, primary_key=True,
                                                                   serialize=False)),
                ('status', models.TextField()),
                ('role', models.BigIntegerField()),
                ('guild',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='iceteabot.discordguild')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='discordmember',
            constraint=models.UniqueConstraint(fields=('id', 'guild'), name='unique_member'),
        ),
    ]
