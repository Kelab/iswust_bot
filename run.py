from quart import Quart


def create_app(mode="bot") -> Quart:
    import log  # noqa: F401
    import app

    return app.init(mode)
