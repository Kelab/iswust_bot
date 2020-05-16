from aiocache import Cache
from aiocache.serializers import PickleSerializer

cache = Cache(
    Cache.REDIS, endpoint="redis", namespace="nb", serializer=PickleSerializer(),
)
