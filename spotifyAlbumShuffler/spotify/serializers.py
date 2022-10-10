import rest_framework.serializers

from spotifyAlbumShuffler.spotify.models import SpotifyPlaylist


class SpotifyPlaylistSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = SpotifyPlaylist
        fields = ['id', 'owner', 'spotify_playlist_id', 'back_to_back', 'last_snapshot', 'enabled',
                  'albums_included', 'playlist_name', 'playlist_picture_url']
