# Generated by Django 3.1.5 on 2021-03-17 12:35

import codertheory.utils.custom_fields
import codertheory.utils.generator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True, default=codertheory.utils.generator.generate_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=1000)),
                ('description', models.TextField(default=None, null=True)),
            ],
            options={
                'db_table': 'poll',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True, default=codertheory.utils.generator.generate_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('option', models.CharField(max_length=1000)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.poll')),
            ],
            options={
                'db_table': 'poll_option',
            },
        ),
        migrations.CreateModel(
            name='PollVote',
            fields=[
                ('id', codertheory.utils.custom_fields.NanoIDField(auto_created=True, default=codertheory.utils.generator.generate_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.polloption')),
            ],
            options={
                'db_table': 'poll_vote',
                'order_with_respect_to': 'option',
            },
        ),
        migrations.AddConstraint(
            model_name='polloption',
            constraint=models.UniqueConstraint(fields=('option', 'poll'), name='unique_option'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='polloption',
            order_with_respect_to='poll',
        ),
    ]
