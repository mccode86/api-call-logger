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
