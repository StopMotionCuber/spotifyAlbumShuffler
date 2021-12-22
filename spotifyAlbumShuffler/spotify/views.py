import spotipy
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader
from spotipy import SpotifyOAuth
from rest_framework import viewsets, permissions

from spotifyAlbumShuffler.spotify import logic
from spotifyAlbumShuffler.spotify.models import SpotifyPlaylist
from spotifyAlbumShuffler.spotify.serializers import SpotifyPlaylistSerializer

scopes = ["playlist-modify-private", "playlist-read-private", "playlist-modify-public"]
client = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scopes
    )
)


class SpotifyPlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = SpotifyPlaylistSerializer
    queryset = SpotifyPlaylist.objects.all()
    permission_classes = [permissions.AllowAny]


def album_render(request):
    logic.fill_playlist_information(client)
    playlists_list = SpotifyPlaylist.objects.all()
    template = loader.get_template('album_render.html')
    context = {
        'playlists': playlists_list,
    }
    return HttpResponse(template.render(context, request))


def album_shuffle(request):
    playlists_list = SpotifyPlaylist.objects.filter(back_to_back=True).all()
    for playlist in playlists_list:
        logic.shuffle_playlist(client, playlist)
    return HttpResponse("Shuffled playlists")
