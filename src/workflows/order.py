from src.engine.registry import workflow, sleep  # import the machinery


# --- the steps: each is just (context) -> dict ---


def reserve(context):
    print("Reserve called")
    return {"reservation_id": "28792bz98"}  # merges into context


def charge(context):
    print("Charge called")
    return {"payment_id": "sjhdkjhdi837"}


def ship(context):
    print("ship called")
    return {"tracking": 298080298}


def notify(context):
    print("notify called")
    return {}  # nothing to add to context


# --- the definition: bind a name to an ordered list of those steps ---


@workflow("order")
class Order:
    steps = [reserve, charge, sleep(3600), ship, notify]
