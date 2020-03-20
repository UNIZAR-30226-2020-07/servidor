# Generated by Django 3.0.3 on 2020-03-20 11:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('songs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='albums',
                                    to='songs.Artist'),
        ),
    ]
