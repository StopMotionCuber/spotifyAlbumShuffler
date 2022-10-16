import rest_framework.serializers

from spotifyAlbumShuffler.spotify.models import SpotifyPlaylist


class SpotifyPlaylistSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = SpotifyPlaylist
        fields = ['id', 'owner', 'spotify_playlist_id', 'back_to_back', 'last_snapshot', 'enabled',
                  'albums_included', 'playlist_name', 'playlist_picture_url', 'playlist_schedule_minute',
                  'playlist_schedule_hour']
        extra_kwargs = {
            "id": {"read_only": True},
            "owner": {"read_only": True},
            "spotify_playlist_id": {"read_only": True},
            "back_to_back": {"read_only": True},
            "albums_included": {"read_only": True},
            "last_snapshot": {"read_only": True},
            "playlist_picture_url": {"read_only": True},
            "playlist_name": {"read_only": True}
        }

