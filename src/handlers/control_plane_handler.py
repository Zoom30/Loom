from datetime import datetime

import boto3
import json
from uuid import uuid4

from src.settings import settings
from utils import shard_for


def handler(event, context) -> str:
    print("control plane function invoked")
    print(f"event: {event}")

    body = json.loads(event.get("body") or "{}")
    execution_id = body.get("id")

    db_client = boto3.client("dynamodb", region_name="eu-west-1")
    sqs_client = boto3.client("sqs", region_name="eu-west-1")

    exec_id = uuid4().hex
    created_at = datetime.now().strftime()
    db_client.put_item(
        TableName="LoomTable",
        Item={
            "PK": {"S": f"EXEC#{exec_id}"},
            "SK": {"S": "#META"},
            "workflow": {"S": "order"},
            "status": {"S": "SLEEPING"},
            "current_step": {"N": 2},
            "version": {"N": 3},
            "context": body,
            "GSI1PK": shard_for(exec_id=exec_id),
            # "GSI1SK":



        },
    )
    sqs_client.send_message(
        QueueUrl=settings.step_queue_url,
        MessageBody=json.dumps({"execution_id": execution_id}),
    )

    return "Hello from control plane"
