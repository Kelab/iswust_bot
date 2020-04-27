from os import getenv as _
from app.exceptions import EnvironmentValueNotFound


def get_env_or_raise(key):
    if _(key):
        return _(key)
    raise EnvironmentValueNotFound(key)
