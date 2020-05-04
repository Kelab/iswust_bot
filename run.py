import app.env  # noqa: F401
import log  # noqa: F401
import app

bot = app.init()
app = bot.asgi
