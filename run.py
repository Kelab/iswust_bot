import sys
import iswust
import views

config = None

try:
    import config
except ImportError:
    print('There is no config file!', file=sys.stderr)

if config is None:
    try:
        import config_base as config
    except ImportError:
        print('There is no configuration file!', file=sys.stderr)
        exit(1)

bot = iswust.init(config)
app = views.init(bot, config)

if __name__ == '__main__':
    bot.run()
