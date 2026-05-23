from dataclasses import dataclass

class InvalidCost(Exception):
    pass


class DuplicateCallID(Exception):
    pass


class CallNotFound(Exception):
    pass


@dataclass
class APICall:
    call_id: str # Unique ID per call — lets you find/remove one specific record
    model: str # e.g. "claude-opus-4-7" — grouping/aggregation in Project 2
    input_tokens: int # What you sent
    output_tokens: int # What you got back
    cost_usd: float # Computed at call time; storing it avoids recomputing later when prices change.
    latency_ms: int # How long the call took
    prompt_excerpt: str # First ~100 chars of the prompt — for "what was I asking?"
    response_excerpt: str # First ~100 chars of the response
    tags: list[str] # Free-form labels (["debug", "production"]) for filtering
    timestamp: str # ISO-format date string ("2026-05-23T14:30:00")

    def __post_init__(self):
        if self.cost_usd < 0:
            raise InvalidCost(f"cost_usd cannot be negative, got {self.cost_usd}")


call_1 = APICall(call_id="abc-123",
                 model="claude-opus-4-7",
                 input_tokens=10000,
                 output_tokens=25000,
                 cost_usd=2.99,
                 latency_ms=5000,
                 prompt_excerpt="what was I asking?",
                 response_excerpt="You're asking about anthropic",
                 tags=["production", "user-facing"],
                 timestamp="2026-05-23T14:30:00")

print(call_1)

try:
    call_invalid = APICall(call_id="abc-456",
                           model="claude-opus-4-7",
                           input_tokens=10000,
                           output_tokens=25000,
                           cost_usd=-5.0,
                           latency_ms=5000,
                           prompt_excerpt="what was I asking?",
                           response_excerpt="You're asking about anthropic",
                           tags=["production", "user-facing"],
                           timestamp="2026-05-23T14:30:00")
except InvalidCost as e:
    print(f"Caught: {e}")

call_valid = APICall(call_id="abc-789",
                           model="claude-opus-4-7",
                           input_tokens=10000,
                           output_tokens=25000,
                           cost_usd=1.50,
                           latency_ms=5000,
                           prompt_excerpt="what was I asking?",
                           response_excerpt="You're asking about anthropic",
                           tags=["production", "user-facing"],
                           timestamp="2026-05-23T14:30:00")
print(call_valid)