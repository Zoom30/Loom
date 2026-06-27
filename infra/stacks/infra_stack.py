from aws_cdk import (
    CfnOutput,
    Stack,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_lambda_event_sources as event_sources,
    aws_events_targets as events_targets,
    aws_events as events,
    aws_dynamodb as dynamodb,
    Duration,
)
from constructs import Construct

from infra.utilities.utils import CODE_EXCLUDES


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ControlPlane Lambda Function

        control_plane_function = _lambda.Function(
            self,
            "LoomControlPlane",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="src.handlers.control_plane_handler.handler",
            code=_lambda.Code.from_asset(path=".", exclude=CODE_EXCLUDES),
        )
        control_plane_function_url = _lambda.FunctionUrl(
            self,
            "LoomControlPlaneFunctionUrl",
            function=control_plane_function,
            auth_type=_lambda.FunctionUrlAuthType.NONE,
        )

        CfnOutput(self, id="LCPApiUrl", value=control_plane_function_url.url)

        # Worker Lambda Function

        step_queue = sqs.Queue(self, "LoomStepQueue")

        worker_function = _lambda.Function(
            self,
            "LoomWorker",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="src.handlers.worker_handler.handler",
            code=_lambda.Code.from_asset(path=".", exclude=CODE_EXCLUDES),
        )
        worker_function.add_event_source(event_sources.SqsEventSource(step_queue))
        step_queue.grant_consume_messages(worker_function)
        step_queue.grant_send_messages(control_plane_function)
        step_queue.grant_send_messages(worker_function)

        # DynamoDB Table

        table = dynamodb.TableV2(
            self,
            "LoomTable",
            table_name="LoomTable",
            billing=dynamodb.Billing.provisioned(
                read_capacity=dynamodb.Capacity.fixed(25),
                write_capacity=dynamodb.Capacity.autoscaled(max_capacity=25),
            ),
            partition_key={"name": "pk", "type": dynamodb.AttributeType.STRING},
        )

        table.grant_write_data(control_plane_function)
        table.grant_write_data(worker_function)

        #         sweeper function
        sweeper_function = _lambda.Function(
            self,
            "LoomSweeper",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="src.handlers.sweeper_handler.handler",
            code=_lambda.Code.from_asset(path=".", exclude=CODE_EXCLUDES),
        )

        sweeper_schedule = events.Schedule.rate(
            Duration.hours(1)
        )  # TODO: change to minutes once done implementing
        sweeper_target = events_targets.LambdaFunction(handler=sweeper_function)

        events.Rule(
            self, "LoomSweeperTick", targets=[sweeper_target], schedule=sweeper_schedule
        )
