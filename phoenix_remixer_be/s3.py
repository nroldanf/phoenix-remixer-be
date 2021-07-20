from aws_cdk import aws_s3 as s3
from aws_cdk import core


class AwsS3:
    """
    References:

    https://pypi.org/project/aws-cdk.aws-s3/
    https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/README.html
    """

    def __init__(
        self,
        scope: core.Construct,
        expiration: int = 7,
        removal_policy: core.RemovalPolicy = core.RemovalPolicy.DESTROY,
    ) -> None:
        self.scope = scope
        self.expiration = expiration  # Days
        self.removal_policy = removal_policy

    def bucket(self, name: str) -> s3.Bucket:
        lifecycle_rules = [
            s3.LifecycleRule(expiration=core.Duration.days(self.expiration))
        ]
        auto_delete_objects = self.removal_policy == core.RemovalPolicy.DESTROY
        bucket = s3.Bucket(
            self.scope,
            name,
            auto_delete_objects=auto_delete_objects,
            removal_policy=self.removal_policy,
            versioned=False,
            lifecycle_rules=lifecycle_rules,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )
        # add bucket name to outputs
        core.CfnOutput(
            self.scope,
            "downloaded-songs-bucket-name",
            value=bucket.bucket_name,
        )

        return bucket
