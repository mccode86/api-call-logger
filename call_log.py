from api_call import APICall, DuplicateCallID, CallNotFound
import json
from dataclasses import dataclass, asdict
from pathlib import Path

class CallLog:
    def __init__(self):
        self.calls: list[APICall] = []

    def add(self, call: APICall) -> None:
        for existing in self.calls:
            if existing.call_id == call.call_id:
                raise DuplicateCallID(f"Duplicate call_id: {call.call_id}")
        self.calls.append(call)

    def remove(self, call_id: str) -> None:
        for existing in self.calls:
            if existing.call_id == call_id:
                self.calls.remove(existing)
                return
        raise CallNotFound(f"Call not found: {call_id}")

    def get_by_id(self, call_id: str) -> APICall:
        for existing in self.calls:
            if existing.call_id == call_id:
                return existing
        raise CallNotFound(f"Call not found: {call_id}")

    def save(self, path: Path) -> None:
        calls_dicts = [asdict(call) for call in self.calls]
        with open(path, "w") as f:
            json.dump(calls_dicts, f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "CallLog":
        with open(path, "r") as f:
            calls_data = json.load(f)
            new_log = cls()
            new_log.calls = [APICall(**call_dict) for call_dict in calls_data]
            return new_log


log = CallLog()

call_a = APICall(call_id="abc-001",
                 model="claude-opus-4-7",
                 input_tokens=10000,
                 output_tokens=25000,
                 cost_usd=2.99,
                 latency_ms=5000,
                 prompt_excerpt="what was I asking?",
                 response_excerpt="You're asking about anthropic",
                 tags=["production", "user-facing"],
                 timestamp="2026-05-23T14:30:00")

call_b = APICall(call_id="abc-002",
                 model="claude-opus-4-7",
                 input_tokens=10000,
                 output_tokens=25000,
                 cost_usd=2.99,
                 latency_ms=5000,
                 prompt_excerpt="what was I asking?",
                 response_excerpt="You're asking about anthropic",
                 tags=["production", "user-facing"],
                 timestamp="2026-05-23T14:30:00")

log.add(call_a)
log.add(call_b)

print(len(log.calls))

call_c = APICall(call_id="abc-001",
                 model="claude-sonnet-4-6",
                 input_tokens=10000,
                 output_tokens=25000,
                 cost_usd=2.99,
                 latency_ms=5000,
                 prompt_excerpt="what was I asking?",
                 response_excerpt="You're asking about anthropic",
                 tags=["production", "user-facing"],
                 timestamp="2026-05-23T14:30:00")

try:
    log.add(call_c)
except DuplicateCallID as e:
    print(f"Caught: {e}")

print(len(log.calls))

log.remove("abc-001")
print(len(log.calls))

try:
    log.remove("xyz-999")
except CallNotFound as e:
    print(f"Caught: {e}")

print(len(log.calls))

id_test = log.get_by_id("abc-002")
print(id_test.model)

try:
    log.get_by_id("xyz-999")
except CallNotFound as e:
    print(f"Caught: {e}")

print(len(log.calls))

log.save(Path("calls.json"))

loaded_log = CallLog.load(Path("calls.json"))
print(len(loaded_log.calls))
