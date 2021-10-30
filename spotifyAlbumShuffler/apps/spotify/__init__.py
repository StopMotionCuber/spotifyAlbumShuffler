import spotipy


def is_backtoback(client: spotipy.Spotify, playlist_id):
    songs = client.playlist_items(playlist_id)
    albums = []
    album_finished = True
    album_idx = 1
    for song in songs['items']:
        song = song['track']
        if album_finished:
            album_idx = 0
            albums.append(song['album']['id'])
            album_finished = False
        album_idx += 1
        if song["album"]['id'] != albums[-1] or song["track_number"] != album_idx:
            return False
        if song["album"]["total_tracks"] == album_idx:
            album_finished = True
    return album_finished and len(albums) > 1
