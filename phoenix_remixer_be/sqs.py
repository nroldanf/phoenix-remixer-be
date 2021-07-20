from aws_cdk import aws_kms as kms
from aws_cdk import aws_sqs as sqs
from aws_cdk import core


class AwsSQS:
    """
    https://pypi.org/project/aws-cdk.aws-sqs/
    https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_sqs/README.html
    """

    def __init__(
        self,
        scope: core.Construct,
        fifo: bool = False,
        retention_period: int = core.Duration.days(1),
    ) -> None:
        self.scope = scope
        self.retention_period = retention_period
        self.fifo = fifo

    def kms_key(self, name) -> kms.Key:
        key = kms.Key(self.scope, f"{name}-key")
        return key

    def sqs(self, name: str) -> sqs.Queue:
        name = f"{name}-queue.fifo" if self.fifo else f"{name}-queue"
        key = self.kms_key(name)
        queue = sqs.Queue(
            self.scope,
            name,
            encryption=sqs.QueueEncryption.KMS,
            encryption_master_key=key,
            fifo=self.fifo,
            retention_period=self.retention_period,
        )
        return queue
