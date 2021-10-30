from django.db import models


class SpotifyUser(models.Model):
    id = models.AutoField()
    spotify_user_id = models.CharField(100, unique=True)


class SpotifyPlaylist(models.Model):
    id = models.AutoField()
    spotify_playlist_id = models.CharField(50, unique=True)
    owner = models.ForeignKey(SpotifyUser, on_delete=models.CASCADE)
    back_to_back = models.BooleanField()
    last_snapshot = models.CharField(100)
    albums_included = models.ManyToManyField("SpotifyAlbum")
    playlist_name = models.CharField(200)
    playlist_picture_uri = models.URLField()


class SpotifyAlbum(models.Model):
    id = models.AutoField()
    spotify_album_id = models.CharField(50, unique=True)
    album_name = models.CharField(200)
    album_cover = models.URLField()


class SpotifyTokenInformation(models.Model):
    id = models.AutoField()
