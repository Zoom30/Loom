def handler(event, context) -> str:
    print(f"event: {event}")
    print(f"context: {context}")
    return "Hello from sweeper"
