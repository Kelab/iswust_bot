from dotenv import load_dotenv

load_dotenv()

import log  # noqa: F401
import app

bot = app.init()
app = bot.asgi
