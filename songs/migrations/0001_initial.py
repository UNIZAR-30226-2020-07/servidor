# Generated by Django 3.0.3 on 2020-04-07 15:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('podcast', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('duration', models.PositiveIntegerField()),
                ('stream_url', models.CharField(max_length=100)),
                ('genre', models.CharField(choices=[('90s', 'Ninetys'), ('Classic', 'Classic'), ('Electronic', 'Electronic'), ('Reggae', 'Reggae'), ('R&B', 'R B'), ('Latin', 'Latin'), ('Oldies', 'Oldies'), ('Country', 'Country'), ('Rap', 'Rap'), ('Rock', 'Rock'), ('Metal', 'Metal'), ('Pop', 'Pop'), ('Blues', 'Blues'), ('Jazz', 'Jazz'), ('Folk', 'Folk'), ('80s', 'Eightys')], max_length=10)),
                ('episode', models.BooleanField(default=False)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='songs', to='songs.Album')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='albums', to='songs.Artist'),
        ),
    ]
