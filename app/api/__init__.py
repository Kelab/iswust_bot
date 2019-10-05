from quart import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from . import admin
from . import push
from . import push_cs_today
