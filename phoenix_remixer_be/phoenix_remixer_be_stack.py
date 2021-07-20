from aws_cdk import core
from ec2 import AwsEc2


class PhoenixRemixerBeStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        construct_id: str,
        parameters: dict,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        AwsEc2(self).ec2(parameters.get("name"))
