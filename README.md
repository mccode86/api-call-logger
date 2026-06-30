# API Call Logger

A command-line tool for logging and analyzing Claude API calls. Tracks cost, latency, token usage, and model
distribution across sessions.

## Files

| File          | Purpose                                                                      |
|---------------|------------------------------------------------------------------------------|
| `api_call.py` | `APICall` dataclass - defines the structure of a single logged call          |
| `call_log.py` | `CallLog` class - manages a collection of calls with search, sort, and stats |
| `cli.py`      | Interactive CLI - the main entry point                                       |
| `calls.json`  | Persistent storage - auto-saved after every `log` command                    |

## Usage

```bash
python cli.py
```

Available commands at the `>>` prompt:

| Command  | Description                                              |
|----------|----------------------------------------------------------|
| `log`    | Add a new API call (prompts for all fields)              |
| `list`   | Show all logged calls                                    |
| `search` | Filter by `model`, `tag`, or `cost` range                |
| `stats`  | Show model distribution, cost per model, and top spender |
| `quit`   | Exit the program                                         |

## APICall Fields

| Field              | Type        | Description                                     |
|--------------------|-------------|-------------------------------------------------|
| `call_id`          | `str`       | Unique identifier per call                      |
| `model`            | `str`       | e.g. `claude-opus-4-7`                          |
| `input_tokens`     | `int`       | Tokens sent in the prompt                       |
| `output_tokens`    | `int`       | Tokens returned in the response                 |
| `cost_usd`         | `float`     | Cost in USD (must be ≥ 0)                       |
| `latency_ms`       | `int`       | Response time in milliseconds                   |
| `prompt_excerpt`   | `str`       | First ~100 chars of the prompt                  |
| `response_excerpt` | `str`       | First ~100 chars of the response                |
| `tags`             | `list[str]` | Free-form labels e.g. `["production", "debug"]` |
| `timestamp`        | `str`       | ISO 8601 format, auto-set by CLI                |

## CallLog Methods

**CRUD**

- `add(call)` - adds a call; raises `DuplicateCallID` if `call_id` already exists
- `remove(call_id)` - removes by ID; raises `CallNotFound` if missing
- `get_by_id(call_id)` - retrieves a single call by ID

**Persistence**

- `save(path)` - writes all calls to a JSON file
- `load(path)` - class method; loads calls from a JSON file

**Search & Filter**

- `find_by_model(model)` - returns calls matching the model name
- `find_by_tag(tag)` - returns calls that include the tag
- `find_by_cost_range(min, max)` - returns calls within a cost range

**Sort**

- `sorted_by_cost()` - ascending by `cost_usd`
- `sorted_by_latency()` - ascending by `latency_ms`

**Analytics**

- `model_distribution()` - `Counter` of calls per model
- `cost_by_model()` - total USD spent per model
- `top_model_by_cost()` - model with highest total spend

## Error Types

| Exception         | When raised                         |
|-------------------|-------------------------------------|
| `InvalidCost`     | `cost_usd` is negative              |
| `DuplicateCallID` | `call_id` already exists in the log |
| `CallNotFound`    | `call_id` not found in the log      |
