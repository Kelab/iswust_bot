from app.env import env
import time
from typing import Optional

api_url: Optional[str] = env("API_URL")
web_url: Optional[str] = env("WEB_URL")
api_version: str = "/api/v1"

if not (api_url and web_url):
    print("API_URL and WEB_URL not fount in environ!")
    exit(0)

if api_url:
    api_url = api_url.rstrip("/") + api_version

if web_url:
    web_url = web_url.rstrip("/")


class INFO:
    semester_start_day = time.strptime("2019-08-26", "%Y-%m-%d")
    semester_name = "2019-2020-1"
