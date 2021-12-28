from spotipy import CacheHandler

from spotifyAlbumShuffler.spotify.models import SpotifyUser


class UserCacheHandler(CacheHandler):
    def __init__(self, user: SpotifyUser):
        self._user = user

    def get_cached_token(self):
        return self._user.token

    def save_token_to_cache(self, token_info):
        self._user.token = token_info
        self._user.save()
