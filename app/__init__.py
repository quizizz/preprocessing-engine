from sanic import Sanic
from app.routes import setup_routes
from app.config import *


def create_app():
    application = Sanic(__name__)
    application.config.update_config(Configuration)
    setup_routes(application)
    return application.get_app(__name__)


app = create_app()
app.config.LOGGING = LOGGING_CONFIG_DEFAULTS
