from aws_cdk import core
from ec2 import AwsEc2
from s3 import AwsS3
from sqs import AwsSQS


class PhoenixRemixerBeStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        construct_id: str,
        parameters: dict,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 Bucket
        BUCKET_SONGS = "{}-downloaded-songs".format(parameters.get("name"))
        AwsS3(self, parameters.get("s3_expiration_days")).bucket(BUCKET_SONGS)

        # SQS queue
        AwsSQS(self).sqs(parameters.get("name"))

        # EC2 instance within a VPC
        _ = AwsEc2(self).ec2(parameters.get("name"))
