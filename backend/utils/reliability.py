import time
from functools import wraps
import random


def retry(max:int = 3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            for attempt in range(max):
                try:
                    return func(*args,**kwargs)
                except Exception as e:
                    if attempt == max -1:
                        raise e
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait:.2f}s")
                    time.sleep(wait)

        return wrapper
    return decorator



if __name__ == "__main__":
    call_count = 0
    @retry(max=3)
    def failing_function():
        global call_count
        call_count += 1
        if call_count < 3:
            raise Exception("Simulated failure")
        return "success on attempt 3"
    
    print(failing_function())