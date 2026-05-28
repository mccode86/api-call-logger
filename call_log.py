from api_call import APICall, DuplicateCallID, CallNotFound
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import Counter
from collections import defaultdict


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

    def find_by_model(self, model: str) -> list[APICall]:
        return [call for call in self.calls if call.model == model]

    def find_by_cost_range(self, min_cost: float, max_cost: float) -> list[APICall]:
        return [call for call in self.calls if min_cost <= call.cost_usd <= max_cost]

    def find_by_tag(self, tag: str) -> list[APICall]:
        return [call for call in self.calls if tag in call.tags]

    def sorted_by_cost(self) -> list[APICall]:
        return sorted(self.calls, key=lambda call: call.cost_usd)

    def sorted_by_latency(self) -> list[APICall]:
        return sorted(self.calls, key=lambda call: call.latency_ms)

    def model_distribution(self) -> Counter:
        return Counter(call.model for call in self.calls)

    def cost_by_model(self) -> dict[str, float]:
        result = defaultdict(float)
        for call in self.calls:
            result[call.model] += call.cost_usd
        return dict(result)

    def top_model_by_cost(self) -> str:
        cost = self.cost_by_model()
        return max(cost, key=lambda model: cost[model])


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

call_d = APICall(call_id="efg-001",
                 model="claude-haiku-4-5",
                 input_tokens=10000,
                 output_tokens=25000,
                 cost_usd=0.50,
                 latency_ms=1000,
                 prompt_excerpt="what was I asking?",
                 response_excerpt="You're asking about token usage",
                 tags=["production", "user-facing"],
                 timestamp="2026-05-23T14:30:00")

call_e = APICall(call_id="efg-002",
                 model="claude-sonnet-4-6",
                 input_tokens=10000,
                 output_tokens=25000,
                 cost_usd=5.00,
                 latency_ms=2000,
                 prompt_excerpt="what was I asking?",
                 response_excerpt="You're asking about token usage",
                 tags=["production", "user-facing"],
                 timestamp="2026-05-23T14:30:00")

call_f = APICall(call_id="efg-003",
                 model="claude-sonnet-4-5",
                 input_tokens=10000,
                 output_tokens=25000,
                 cost_usd=1.50,
                 latency_ms=3000,
                 prompt_excerpt="what was I asking?",
                 response_excerpt="You're asking about token usage",
                 tags=["production", "user-facing"],
                 timestamp="2026-05-23T14:30:00")

log.add(call_d)
log.add(call_e)
log.add(call_f)

print(log.find_by_model("claude-sonnet-4-6"))
print([call.cost_usd for call in log.find_by_model("claude-sonnet-4-6")])

print(len(log.calls))

find_model = log.find_by_model("gpt-4")
print(find_model)

find_model_d = log.find_by_model("claude-haiku-4-5")
print(find_model_d[0].input_tokens)

print([call.cost_usd for call in log.find_by_cost_range(0.50, 5.00)])
print(log.find_by_cost_range(0.10, 0.20))

print([call.tags for call in log.find_by_tag("production")])
print(log.find_by_tag("transformer"))

print([call.cost_usd for call in log.sorted_by_cost()])
print([call.latency_ms for call in log.sorted_by_latency()])

print(log.model_distribution())

print(log.cost_by_model())

print(log.top_model_by_cost())
