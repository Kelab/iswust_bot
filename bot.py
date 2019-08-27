import os
import sys
import iswust
from dotenv import load_dotenv

# 加载.env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

config = None

try:
    import bot_config as config
except ImportError:
    print('There is no config file!', file=sys.stderr)

if config is None:
    try:
        import bot_config_base as config
    except ImportError:
        print('There is no configuration file!', file=sys.stderr)
        exit(1)

bot = iswust.init(config)

# 一定要在 bot 加载完后才能加载 views
# 否则获取不到运行中的 bot 实例
from views import api as api_blueprint
app = bot.asgi
app.register_blueprint(api_blueprint)

# 加载 logger
from log import BOT_LOGGER

if __name__ == '__main__':
    BOT_LOGGER.info('Starting')
    bot.run(use_reloader=True)
