# Generated by Django 3.0.3 on 2020-03-18 16:17

from django.db import migrations, models
import django.db.models.deletion


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
                ('duration', models.IntegerField()),
                ('stream_url', models.CharField(max_length=100)),
                ('genre', models.CharField(choices=[('90s', 'Ninetys'), ('Classic', 'Classic'), ('Electronic', 'Electronic'), ('Reggase', 'Reggae'), ('R&B', 'R B'), ('Latin', 'Latin'), ('Oldies', 'Oldies'), ('Country', 'Country'), ('Rap', 'Rap'), ('Rock', 'Rock'), ('Metal', 'Metal'), ('Pop', 'Pop'), ('Blues', 'Blues'), ('Jazz', 'Jazz'), ('Folk', 'Folk'), ('80s', 'Eightys'), ('Playlist', 'Playlist')], max_length=10)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='songs', to='songs.Album')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('allSongs', models.ManyToManyField(related_name='playlists', to='songs.Song')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='albums', to='songs.Artist'),
        ),
    ]
