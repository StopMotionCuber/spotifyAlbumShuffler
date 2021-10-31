

from django.template.defaulttags import register

from spotifyAlbumShuffler.spotify.models import SpotifyPlaylist


@register.filter
def album_names_from_playlist(playlist: SpotifyPlaylist):
    return playlist.albums_included.values_list("album_name", flat=True)
