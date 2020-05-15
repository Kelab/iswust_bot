import os
from environs import Env
from dotenv import load_dotenv, find_dotenv

__all__ = ["env", "load_env"]

env = Env()


def load_env(mode="bot"):
    load_dotenv(encoding="utf8")

    os.environ["RUN_MODE"] = mode
    if mode != "bot":
        if f := find_dotenv(".env.local"):
            load_dotenv(f, encoding="utf8")
