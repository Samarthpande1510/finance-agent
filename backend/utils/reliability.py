import time
from functools import wraps
import random
from enum import Enum

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

class LoopGuard:
    def __init__(self, max_calls=8):
        self.max_calls = max_calls
        self.call_count = 0
        
    def check(self, tool_name: str):
        self.call_count += 1
        if self.call_count > self.max_calls:
            raise Exception(f"Loop guard triggered after {self.max_calls} tool calls")
        print(f"Tool call {self.call_count}/{self.max_calls}: {tool_name}")
    
    def reset(self):
        self.call_count = 0

class AgentState(Enum):
    IDLE = "idle"
    UNDERSTANDING = "understanding_query"
    RETRIEVING = "retrieving"
    CALCULATING = "calculating"
    RESPONDING = "responding"

class StateMachine:
    def __init__(self):
        self.state = AgentState.IDLE
    
    def transition(self, new_state: AgentState):
        print(f"State: {self.state.value} → {new_state.value}")
        self.state = new_state
    
    def reset(self):
        self.state = AgentState.IDLE

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

    print("\n--- LoopGuard test ---")
    guard = LoopGuard(max_calls=3)
    try:
        for i in range(5):
            guard.check(f"tool_{i}")
    except Exception as e:
        print(f"Caught: {e}")

    print("\n--- StateMachine test ---")
    sm = StateMachine()
    sm.transition(AgentState.UNDERSTANDING)
    sm.transition(AgentState.RETRIEVING)
    sm.transition(AgentState.CALCULATING)
    sm.transition(AgentState.RESPONDING)
    sm.reset()
    print(f"After reset: {sm.state.value}")