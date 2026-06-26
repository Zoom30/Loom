from aws_cdk import (
    CfnOutput,
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_lambda as _lambda,
)
from constructs import Construct


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        sqs.Queue(
            self,
            "InfraQueue",
            visibility_timeout=Duration.seconds(300),
        )

        # ControlPlane Lambda Function

        control_plane_function = _lambda.Function(
            self,
            "ControlPlane",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="handlers.control_plane_handler.handler",
            code=_lambda.Code.from_asset("."),
        )
        control_plane_function_url = _lambda.FunctionUrl(
            self,
            "ControlPlaneFunctionUrl",
            function=control_plane_function,
            auth_type=_lambda.FunctionUrlAuthType.NONE,
        )

        CfnOutput(self, id="CPApiUrl", value=control_plane_function_url.url)
