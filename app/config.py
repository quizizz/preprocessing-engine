import os
from sanic.log import LOGGING_CONFIG_DEFAULTS


class Configuration:
    PORT = os.environ.get('PORT', 8081)
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'


log_format = '{"serverTime": %(asctime)s, "level": [%(levelname)s], "name": %(name)s, "message": %(message)s}'

# Update the Sanic logging configuration
LOGGING_CONFIG_DEFAULTS['formatters']['generic']['format'] = log_format
