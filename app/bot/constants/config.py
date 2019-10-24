import os
import time
from typing import Optional

api_url: Optional[str] = os.environ.get("API_URL")
web_url: Optional[str] = os.environ.get("WEB_URL")

if not (api_url and web_url):
    print("API_URL and WEB_URL not fount in environ!")
    exit(0)

if api_url:
    api_url = api_url.rstrip('/')

if web_url:
    web_url = web_url.rstrip('/')


class INFO:
    semester_start_day = time.strptime("2019-08-26", "%Y-%m-%d")
    semester_name = "2019-2020-1"
