"""Cache configurations."""

from redis import StrictRedis, RedisError
from flask import current_app
from redis.client import Redis
import json


class RedisManager:
    """
    A singleton class to manage Redis client connections.
    It ensures that only one Redis client is initialized and reused across the application.
    """
    _redis_client = None

    @classmethod
    def get_client(cls, app=None) -> Redis:
        """
        Retrieves the Redis client, initializing it if necessary. This method ensures that
        the Redis client is a singleton and reuses the existing client once initialized.

        Parameters:
            app: Flask application instance. Defaults to Flask's `current_app` if None.

        Returns:
            An instance of Redis client, specifically a StrictRedis client.

        Raises:
            Exception: If the Redis client has not been initialized and no app context is provided.
        """
        if cls._redis_client is None:
            if app is None:
                app = current_app
            redis_url = app.config.get("REDIS_URL")
            cls._redis_client = StrictRedis.from_url(redis_url)
            app.logger.info("Redis client initiated successfully")
        return cls._redis_client
    
    @classmethod
    def handle_moved_error(cls, e: RedisError):
        new_location = e.args[0].split(' ')[-1]
        cls._redis_client = StrictRedis.from_url(new_location)
        return cls._redis_client


class Cache:
    """
    A high-level caching interface that abstracts the underlying cache mechanism. This class
    provides methods to set and get values from the cache. It dynamically decides whether to use
    Redis or a simple cache based on application configuration.
    """

    @classmethod
    def set(cls, key, value, timeout=None):
        """
        Set a value in the cache with an optional timeout. It abstracts away the details of
        whether Redis or a simple cache is being used.

        Parameters:
            key: The key under which the value is stored.
            value: The value to store.
            timeout: Optional expiration time in seconds.
        """
        value_json = json.dumps(value)  # Serialize the value to a JSON string
        try:
            RedisManager.get_client().set(key, value_json, ex=timeout)  # Store the JSON string in Redis
        except RedisError as e:
            if "MOVED" in str(e):
                redis_client = RedisManager.handle_moved_error(e)
                redis_client.set(key, value_json, ex=timeout)

    @classmethod
    def get(cls, key):
        """
        Retrieve a value from the cache. It abstracts away the details of whether Redis or
        a simple cache is being used.

        Parameters:
            key: The key whose value to retrieve.

        Returns:
            The value stored under the given key in the cache. Returns None if the key doesn't exist.
        """
        try:
            val_json = RedisManager.get_client().get(key)  # Retrieve the value as JSON string
            if val_json is not None:
                return json.loads(val_json)  # Deserialize the JSON string back into Python object
            else:
                return None
        except RedisError as e:
            if "MOVED" in str(e):
                redis_client = RedisManager.handle_moved_error(e)
                return redis_client.get(key)

