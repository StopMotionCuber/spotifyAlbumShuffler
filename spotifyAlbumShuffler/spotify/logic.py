import random
from dataclasses import dataclass, field
from typing import List

import spotipy

from spotifyAlbumShuffler.spotify.exceptions import InvalidActionException
from spotifyAlbumShuffler.spotify.models import SpotifyPlaylist, SpotifyUser, SpotifyAlbum, SpotifyTrack


@dataclass
class InternalAlbum:
    id: str
    name: str
    cover_url: str
    tracks: List[str] = field(default_factory=list)


class InternalPlaylist:
    """
    This class represents an internal playlist state, including the albums
    """
    def __init__(self, playlist_id):
        self._playlist_id = playlist_id
        self.related_albums = []

    def is_backtoback(self, client: spotipy.Spotify):
        response = client.playlist_items(self._playlist_id)
        songs = response['items']
        self.related_albums = []
        album_finished = True
        album_idx = 1
        # Outer loop to go through all pages lazily
        # We are doing this lazily as first page might already
        # reveal that a playlist is not backtoback
        while True:
            # Inner loop for all songs per page
            for song in songs:
                song = song['track']
                if album_finished:
                    album_idx = 0
                    try:
                        cover_url = song['album']['images'][0]
                    except (KeyError, IndexError):
                        cover_url = None
                    self.related_albums.append(InternalAlbum(
                        id=song['album']['id'],
                        name=song['album']['name'],
                        cover_url=cover_url
                    ))
                    album_finished = False
                album_idx += 1
                if song["album"]['id'] != self.related_albums[-1].id or song["track_number"] != album_idx:
                    return False
                self.related_albums[-1].tracks.append(song['id'])
                if song["album"]["total_tracks"] == album_idx:
                    album_finished = True
            if not response['next']:
                return album_finished and len(self.related_albums) > 1
            response = client.next(response)
            songs = response['items']


def refresh_user_playlists(client: spotipy.Spotify):
    user_id = client.current_user()['id']
    user_object = get_user(user_id)
    response = client.current_user_playlists()
    all_playlists = response['items']
    while response['next']:
        response = client.next(response)
        all_playlists.extend(response['items'])
    # Get current playlists of that user
    available_playlists = SpotifyPlaylist.objects.filter(
        owner=user_object
    ).values_list("spotify_playlist_id", "last_snapshot")
    available_playlists = {
        item["spotify_playlist_id"]: item["last_snapshot"] for item in available_playlists
    }
    new_playlists = []
    for playlist in all_playlists:
        if playlist['owner']['id'] != user_id or playlist['id'] in available_playlists:
            if playlist['snapshot_id'] == available_playlists[playlist['id']]:
                continue
        new_playlists.append(create_or_update_playlist(playlist, client, user_object))


def create_or_update_playlist(playlist, client, owner):
    playlist_obj = InternalPlaylist(playlist['id'])
    b2bstate = playlist_obj.is_backtoback(client)
    spotify_playlist, created = SpotifyPlaylist.objects.get_or_create(
        spotify_playlist_id=playlist['id']
    )
    spotify_playlist.owner = owner
    spotify_playlist.back_to_back = b2bstate
    spotify_playlist.last_snapshot = playlist['snapshot_id']
    spotify_playlist.playlist_name = playlist['name']
    spotify_playlist.save()
    if b2bstate:
        # Include albums, this is not necessary for non-b2b playlists as they don't get used
        related_albums = fill_album_information(playlist_obj)
        album_qs = SpotifyAlbum.objects.filter(spotify_album_id__in=related_albums)
        # Duplicate management???
        spotify_playlist.albums_included.set(album_qs.all())
        spotify_playlist.save()
    return spotify_playlist


def fill_album_information(playlist: InternalPlaylist):
    albums = playlist.related_albums
    album_ids = set(map(lambda x: x.id, albums))

    present_album_ids = SpotifyAlbum.objects.filter(
        spotify_album_id__in=album_ids
    ).values_list("spotify_album_id", flat=True)
    new_albums = []
    new_tracks = []
    processed_albums = set()

    for album in albums:
        assert isinstance(album, InternalAlbum)
        if album.id in present_album_ids or album.id in processed_albums:
            # Album already created
            continue
        new_albums.append(SpotifyAlbum(
            spotify_album_id=album.id,
            album_name=album.name,
        ))
        processed_albums.add(album.id)
        track_position = 1
        for track in album.tracks:
            new_tracks.append(SpotifyTrack(
                related_album=new_albums[-1],
                spotify_track_id=track,
                position_in_album=track_position
            ))
            track_position += 1
        new_albums[-1].save()
    SpotifyTrack.objects.bulk_create(new_tracks)
    return list(map(lambda x: x.id, playlist.related_albums))


def get_user(user_id):
    to_return = SpotifyUser.objects.filter(spotify_user_id=user_id).first()
    if to_return is None:
        to_return = SpotifyUser(spotify_user_id=user_id)
        to_return.save()
    return to_return


def shuffle_playlist(client: spotipy.Spotify, playlist: SpotifyPlaylist):
    if not playlist.back_to_back:
        raise InvalidActionException()
    albums = list(playlist.albums_included.all())
    random.shuffle(albums)
    tracklist = []
    for album in albums:
        assert isinstance(album, SpotifyAlbum)
        album_tracks = album.tracks.order_by("position_in_album").values_list("spotify_track_id", flat=True)
        tracklist.extend(album_tracks)
    batch_size = 100
    client.playlist_replace_items(playlist.spotify_playlist_id, tracklist[:batch_size])
    for i in range(batch_size, len(tracklist), batch_size):
        batch = tracklist[i:i + batch_size]
        client.playlist_add_items(playlist.spotify_playlist_id, batch)

