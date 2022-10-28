import logging
import zoneinfo

from celery.schedules import crontab
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, IntegrityError
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from spotifyAlbumShuffler.celery import app


class SpotifyUser(models.Model):
    id = models.AutoField(primary_key=True)
    spotify_user_id = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    token = models.JSONField(null=True, blank=True)
    last_interaction = models.DateTimeField(auto_now=True)


class SpotifyPlaylist(models.Model):
    id = models.AutoField(primary_key=True)
    spotify_playlist_id = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(SpotifyUser, on_delete=models.CASCADE)
    back_to_back = models.BooleanField()
    enabled = models.BooleanField(default=False)
    last_snapshot = models.CharField(max_length=100)
    albums_included = models.ManyToManyField("SpotifyAlbum")
    playlist_name = models.CharField(max_length=200)
    playlist_picture_url = models.URLField(blank=True)
    last_playlist_picture_update = models.DateTimeField(blank=True, null=True)
    playlist_schedule_minute = models.PositiveIntegerField(default=0, validators=[
        MaxValueValidator(59),
        MinValueValidator(0)
    ])
    playlist_schedule_hour = models.PositiveIntegerField(default=0, validators=[
        MaxValueValidator(23),
        MinValueValidator(0)
    ])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        logging.debug("Calling save method for SpotifyPlaylist")
        super().save(force_insert, force_update, using, update_fields)
        if self.enabled:
            from spotifyAlbumShuffler.spotify.tasks import debug_task
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute='*',
                hour='*',
                day_of_week='*',
                day_of_month='*',
                month_of_year='*'
            )
            try:
                periodic_task = PeriodicTask.objects.get(
                    name=f"album-shuffle-{self.id}"
                )
            except PeriodicTask.DoesNotExist:
                periodic_task = PeriodicTask(
                    name=f"album-shuffle-{self.id}",
                    task="spotifyAlbumShuffler.spotify.tasks.refresh_playlist",
                    args=self.spotify_playlist_id,
                )
            periodic_task.crontab = schedule
            periodic_task.save()
            print("Added periodic task")
        else:
            try:
                PeriodicTask.objects.filter(name=f"album-shuffle-{self.id}").delete()
            except KeyError:
                pass

    def delete(self, using=None, keep_parents=False):
        internal_id = self.id
        super().delete(using, keep_parents)
        try:
            del app.conf.beat_schedule[f"album-shuffle-{internal_id}"]
        except KeyError:
            pass


class SpotifyAlbum(models.Model):
    id = models.AutoField(primary_key=True)
    spotify_album_id = models.CharField(max_length=50, unique=True)
    album_name = models.CharField(max_length=200)
    album_cover = models.BinaryField(null=True, blank=True)


class SpotifyTrack(models.Model):
    id = models.AutoField(primary_key=True)
    related_album = models.ForeignKey(SpotifyAlbum, on_delete=models.CASCADE, related_name="tracks")
    spotify_track_id = models.CharField(max_length=50, unique=True)
    position_in_album = models.IntegerField()
