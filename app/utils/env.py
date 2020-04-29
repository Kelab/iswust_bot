from os import getenv as _
from app.exceptions import EnvironmentValueNotFound

from dotenv import load_dotenv

load_dotenv()


def get_env_or_raise(key):
    if _(key):
        return _(key)
    raise EnvironmentValueNotFound(key)
