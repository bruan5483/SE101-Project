import logging
from functools import wraps

# Set up the logger
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[logging.FileHandler("../logs/function_calls.log")]
    )


def log_function_calls():
    # Decorator to log function calls
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Log the function call details
            logging.info(f"Calling function '{func.__name__}' with arguments {args} and keyword arguments {kwargs}")
            result = func(*args, **kwargs)
            # Log the function return value
            logging.info(f"Function '{func.__name__}' returned {result}")
            return result
        return wrapper
    return decorator
