import logging

import spotipy
from celery import shared_task
from django.db import transaction
from django.utils import timezone

from spotifyAlbumShuffler.spotify.cache_handler import UserCacheHandler
from spotifyAlbumShuffler.spotify.logic import InternalPlaylist, refresh_user_playlists
from spotifyAlbumShuffler.spotify.models import SpotifyPlaylist, SpotifyUser

bucket_name = "spotifyAlbumShuffler"


def get_spotipy_client(user: SpotifyUser):
    scopes = ["playlist-modify-private", "playlist-read-private", "playlist-modify-public"]
    return spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            scope=scopes,
            cache_handler=UserCacheHandler(user)
        )
    )


@shared_task
def refresh_playlist(playlist_id: str):
    playlist = SpotifyPlaylist.objects.get(spotify_playlist_id=playlist_id)
    client = get_spotipy_client(playlist.owner)
    internal_playlist = InternalPlaylist(playlist)
    playlist.back_to_back = internal_playlist.is_backtoback(client)
    if playlist.back_to_back:
        playlist.albums_included = internal_playlist.related_albums


@shared_task
def playlists_for_user(user_id: str):
    user = SpotifyUser.objects.get(spotify_user_id=user_id)
    client = get_spotipy_client(user)
    refresh_user_playlists(client)


@shared_task
def refresh_image(playlist_id: str):
    playlist = SpotifyPlaylist.objects.get(spotify_playlist_id=playlist_id)
    client = get_spotipy_client(playlist.owner)
    raise NotImplementedError()


def pick_image(img_list):
    if not img_list:
        return None
    # for img in reversed(img_list):
    #     if img['height'] >= 300:
    #         return img['url']
    return img_list[0]['url']


@shared_task
def batch_refresh_image(user_id: str):
    user = SpotifyUser.objects.get(spotify_user_id=user_id)
    client = get_spotipy_client(user)
    response = client.current_user_playlists()
    all_playlists = response['items']
    while response['next']:
        response = client.next(response)
        all_playlists.extend(response['items'])
    # Batch all updates into single transaction
    with transaction.atomic():
        for playlist in all_playlists:
            try:
                db_object = SpotifyPlaylist.objects.get(spotify_playlist_id=playlist['id'])
            except SpotifyPlaylist.DoesNotExist:
                continue
            if 'images' not in playlist:
                continue
            picture_url = pick_image(playlist['images'])
            if picture_url is None:
                continue
            db_object.playlist_picture_url = picture_url
            db_object.last_playlist_picture_update = timezone.now()
            logging.debug(f"Updated Picture URL to {picture_url}")
            db_object.save()
