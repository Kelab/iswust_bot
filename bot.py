import sys
import iswust

config = None

try:
    import config
except ImportError:
    pass

if config is None:
    try:
        import config_base as config
    except ImportError:
        pass

if config is None:
    print('There is no configuration file!', file=sys.stderr)
    exit(1)

bot = iswust.init(config)
app = bot.asgi

if __name__ == '__main__':
    bot.run()
