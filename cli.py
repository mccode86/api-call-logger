from call_log import CallLog
from pathlib import Path
from api_call import APICall, InvalidCost, DuplicateCallID
from datetime import datetime

def run_cli():
    path = Path("calls.json")
    if path.exists():
        log = CallLog.load(path)
    else:
        log = CallLog()
    while True:
        command = input(">> ").strip().lower()
        if command == "quit":
            print("Goodbye!")
            break
        elif command == "list":
            if not log.calls:
                print("No calls logged yet.")
            else:
                for call in log.calls:
                    print(call)
        elif command == "log":
            call_id = input("Call ID: ")
            model = input("Model: ")
            input_tokens = int(input("Input Tokens: "))
            output_tokens = int(input("Output Tokens: "))
            cost_usd = float(input("Cost USD: "))
            latency_ms = int(input("Latency: "))
            prompt_excerpt = input("Prompt Excerpt: ")
            response_excerpt = input("Response Excerpt: ")
            tags = input("Tags: ").split(",")
            call = APICall(call_id=call_id,
                           model=model,
                           input_tokens=input_tokens,
                           output_tokens=output_tokens,
                           cost_usd=cost_usd,
                           latency_ms=latency_ms,
                           prompt_excerpt=prompt_excerpt,
                           response_excerpt=response_excerpt,
                           tags=tags,
                           timestamp=datetime.now().isoformat())
            try:
                log.add(call)
                log.save(path)
                print("Call logged")
            except (InvalidCost, DuplicateCallID) as e:
                print(f"Error: {e}")
        elif command == "search":
            search_by = input("Search by (model/tag/cost): ").strip().lower()
            result = []
            if search_by == "model":
                model_name = input("Model name: ")
                result = log.find_by_model(model_name)
            elif search_by == "tag":
                tag = input("Tag: ")
                result = log.find_by_tag(tag)
            elif search_by == "cost":
                min_cost = float(input("Min cost: "))
                max_cost = float(input("Max cost: "))
                result = log.find_by_cost_range(min_cost, max_cost)
            else:
                print("Unknown search type.")
            if not result:
                print("No results.")
            else:
                for call in result:
                    print(call)
        elif command == "stats":
            print(log.model_distribution())
            print(log.cost_by_model())
            print(log.top_model_by_cost())
        else:
            print(f"Unknown Command: {command}")

run_cli()
