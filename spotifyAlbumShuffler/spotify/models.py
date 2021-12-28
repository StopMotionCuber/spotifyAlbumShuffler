from django.contrib.auth.models import User
from django.db import models


class SpotifyUser(models.Model):
    id = models.AutoField(primary_key=True)
    spotify_user_id = models.CharField(max_length=100, unique=True)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.JSONField(null=True, blank=True)
    last_interaction = models.DateTimeField(auto_now=True)


class SpotifyPlaylist(models.Model):
    id = models.AutoField(primary_key=True)
    spotify_playlist_id = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(SpotifyUser, on_delete=models.CASCADE)
    back_to_back = models.BooleanField()
    enabled = models.BooleanField()
    last_snapshot = models.CharField(max_length=100)
    albums_included = models.ManyToManyField("SpotifyAlbum")
    playlist_name = models.CharField(max_length=200)
    playlist_picture_url = models.URLField(blank=True)


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
