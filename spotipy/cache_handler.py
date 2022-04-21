__all__ = ['CacheHandler', 'CacheFileHandler']

import errno
import json
import logging

logger = logging.getLogger(__name__)


class CacheHandler():
    """
    An abstraction layer for handling the caching and retrieval of
    authorization tokens.

    Custom extensions of this class must implement get_cached_token
    and save_token_to_cache methods with the same input and output
    structure as the CacheHandler class.
    """

    def get_cached_token(self):
        """
        Get and return a token_info dictionary object.
        """
        # return token_info
        raise NotImplementedError()

    def save_token_to_cache(self, token_info):
        """
        Save a token_info dictionary object to the cache and return None.
        """
        raise NotImplementedError()


class CacheFileHandler(CacheHandler):
    """
    Handles reading and writing cached Spotify authorization tokens
    as json files on disk.
    """

    def __init__(self,
                 cache_path=None,
                 username=None):
        """
        Parameters:
             * cache_path: May be supplied, will otherwise be generated
                           (takes precedence over `username`)
             * username: May be supplied or set as environment variable
                         (will set `cache_path` to `.cache-{username}`)
        """

        if not cache_path:
            cache_path = ".cache"
            if username:
                cache_path += f"-{str(username)}"
        self.cache_path = cache_path

    def get_cached_token(self):
        token_info = None

        try:
            with open(self.cache_path) as f:
                token_info_string = f.read()
            token_info = json.loads(token_info_string)

        except IOError as error:
            if error.errno == errno.ENOENT:
                logger.debug("cache does not exist at: %s", self.cache_path)
            else:
                logger.warning("Couldn't read cache at: %s", self.cache_path)

        return token_info

    def save_token_to_cache(self, token_info):
        try:
            with open(self.cache_path, "w") as f:
                f.write(json.dumps(token_info))
        except IOError:
            logger.warning('Couldn\'t write token to cache at: %s',
                           self.cache_path)
