from os import path

from aws_cdk import core
from aws_cdk.aws_s3_assets import Asset
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
        ec2 = AwsEc2(self).ec2(parameters.get("name"))

        # Script in S3 as Asset
        dirname = path.dirname(__file__)
        asset = Asset(self, "Asset", path=path.join(dirname, "ec2_asset.py"))
        _ = ec2.user_data.add_s3_download_command(
            bucket=asset.bucket, bucket_key=asset.s3_object_key
        )
        # # Userdata executes script from S3
        # ec2.user_data.add_execute_file_command(
        #     file_path=local_path
        #     )
        # asset.grant_read(ec2.role)
