def handler(event, context) -> str:
    print("control plane function invoked")
    print(f"event: {event}")
    print(f"context: {context}")
    return "Hello"
