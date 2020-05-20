from aiocache import Cache
from aiocache.serializers import PickleSerializer
from app.config import Config

__all__ = ["cache"]
redis_kwargs = dict(
    endpoint="redis",
    password=Config.REDIS_PASSWORD,
    namespace="nb",
    serializer=PickleSerializer(),
)

cache = Cache(Cache.REDIS, **redis_kwargs)
