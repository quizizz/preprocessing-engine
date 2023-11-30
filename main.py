from sanic.log import logger
from sanic import exceptions
from app import app
from app_initializer import init


@app.listener('before_server_start')
async def before_server_start(app, loop):
    try:
        await init(app)
    except Exception as e:
        logger.error(f"Error during app initialization: {e}")
        raise exceptions.SanicException(f"Initialization failure: {e}")


def main():
    try:
        app.run(host="0.0.0.0", port=app.config.PORT, debug=app.config.DEBUG)
    except Exception as e:
        logger.error(f"Error in starting the app: {e}")


if __name__ == "__main__":
    main()
