import time
from sanic.log import logger


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Function {func.__name__} executed in {elapsed_time:.2f} ms")
        return result

    return wrapper
