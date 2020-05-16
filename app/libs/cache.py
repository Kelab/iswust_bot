from aiocache import Cache
from aiocache.serializers import PickleSerializer

__all__ = ["cache"]
redis_kwargs = dict(endpoint="redis", namespace="nb", serializer=PickleSerializer(),)

cache = Cache(Cache.REDIS, **redis_kwargs)
