import boto3
import json


def handler(event, context) -> str:
    print("control plane function invoked")
    print(f"event: {event}")

    body = json.loads(event.get('body') or '{}')
    execution_id = body.get('id')

    db_client = boto3.client("dynamodb", region_name="eu-west-1")
    sqs_client = boto3.client("sqs", region_name="eu-west-1")

    db_client.put_item(TableName="LoomTable", Item={"pk": {"S": execution_id}})
    print(f"context: {context}")

    return "Hello from control plane"
