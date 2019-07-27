from quart import Blueprint

api = Blueprint('api', __name__, url_prefix='/api/v1')

from . import push
# from . import admin
