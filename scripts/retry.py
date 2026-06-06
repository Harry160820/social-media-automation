import time
import functools
from logger import get_logger

logger = get_logger("retry")

def retry(max_attempts=3, delay=5, exceptions=(Exception,)):
    """Retry decorator for any function"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f" {func.__name__} failed after {max_attempts} attempts: {e}")
                        raise
                    logger.warning(f" {func.__name__} attempt {attempts} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

# Test
if __name__ == "__main__":
    @retry(max_attempts=3, delay=2)
    def test_function():
        print("Function executed!")
        return True
    
    test_function()
    print(" Retry logic working!")
