# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=4, choices=[(b'YES', b'Yes'), (b'NO', b'No'), (b'ABST', b'abstention')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hashcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('code', models.CharField(max_length=9)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('time_opened', models.DateTimeField()),
                ('time_closed', models.DateTimeField(blank=True)),
                ('number_of_voters', models.IntegerField(default=0)),
                ('type_of_question', models.CharField(max_length=4, choices=[(b'OPEN', b'Open question'), (b'ANON', b'Anonymous question')])),
                ('ordering', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['-ordering'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('started_at', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='session',
            field=models.ForeignKey(to='vote.Session'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hashcode',
            name='session',
            field=models.ForeignKey(to='vote.Session'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hashcode',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='hashcode',
            field=models.ForeignKey(to='vote.Hashcode'),
            preserve_default=True,
        ),
    ]
