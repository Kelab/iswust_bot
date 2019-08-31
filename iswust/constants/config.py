import os
import time
from typing import Optional

api_url: Optional[str] = os.environ.get("API_URL")
web_url: Optional[str] = os.environ.get("WEB_URL")


class INFO():
    semester_start_day = time.strptime("2019-08-26", "%Y-%m-%d")
    semester_name = '2019-2020-1'
