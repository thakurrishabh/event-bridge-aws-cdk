#!/home/rishabh/MyDrive/Softwares/python3.9

from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_events as events
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_events_targets as targets

class EventBridgeAwsCdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fn = lambda_.Function(self, "ETL_job_func",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=lambda_.Code.asset('lambda')
        )

        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='11')
        )

        queue = sqs.Queue(self, "Queue")

        rule.add_target(targets.LambdaFunction(fn,
            dead_letter_queue=queue, # Optional: add a dead letter queue
            max_event_age=cdk.Duration.hours(2), # Otional: set the maxEventAge retry policy
            retry_attempts=2
        ))
