from aws_cdk import (
    aws_logs as logs,
    aws_lambda as _lambda,
    aws_iam as iam,
    core,
)


class MyStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a Lambda function to process the log data
        my_lambda = _lambda.Function(
            self,
            "MyLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_inline("def lambda_handler(event, context):\n    print(event)"),
        )

        # Define the subscription filter
        logs_subscription_filter = logs.SubscriptionFilter(
            self,
            "LogsSubscriptionFilter",
            log_group=logs.LogGroup.from_log_group_arn(
                self,
                "LogGroup",
                log_group_arn="arn:aws:logs:us-east-1:123456789012:log-group:/my/log/group:*",
            ),
            destination=_lambda.FunctionDestination(my_lambda),
            filter_pattern=logs.FilterPattern.any_term("ERROR", "WARNING"),
        )

        # Grant the necessary permissions to the Lambda function
        my_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["logs:CreateLogStream", "logs:PutLogEvents"],
                resources=[logs_subscription_filter.log_group.log_group_arn],
            )
        )
