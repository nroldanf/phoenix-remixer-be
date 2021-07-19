from aws_cdk import (
    aws_ec2,
    aws_iam,
    core
)


class AwsEc2:
    """
    https://pypi.org/project/aws-cdk.aws-ec2/
    https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/README.html
    """
    def __init__(self, scope: core.Construct, subnet_type: aws_ec2.SubnetType = aws_ec2.SubnetType.PUBLIC,
                 instance_type: aws_ec2.InstanceType = aws_ec2.InstanceType("t3.nano")) -> None:
        self.scope = scope
        self.subnet_type = subnet_type
        self.instance_type = instance_type

    def vpc(self, name: str) -> aws_ec2.Vpc:
        return aws_ec2.Vpc(self.scope, name, nat_gateways=0, subnet_configuration=[
            aws_ec2.SubnetConfiguration(name=self.subnet_type.value.lower(), subnet_type=self.subnet_type)
        ])

    @staticmethod
    def ami() -> aws_ec2.IMachineImage:
        return aws_ec2.MachineImage.latest_amazon_linux(
            generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=aws_ec2.AmazonLinuxEdition.STANDARD,
            virtualization=aws_ec2.AmazonLinuxVirt.HVM,
            storage=aws_ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )

    def role(self, name: str) -> aws_iam.Role:
        role = aws_iam.Role(self.scope, name + "SSM", assumed_by=aws_iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))
        return role

    def instance(self, name: str, ami: aws_ec2.IMachineImage, vpc: aws_ec2.Vpc, role: aws_iam.Role
                 ) -> aws_ec2.Instance:
        return aws_ec2.Instance(self.scope, name, instance_type=self.instance_type,
                                machine_image=ami, vpc=vpc, role=role)

    def ec2(self, name: str) -> aws_ec2.Instance:
        vpc = self.vpc(name + "Vpc")
        ami = self.ami()
        role = self.role(name)
        instance = self.instance(name, ami, vpc, role)
        return instance

        """
        # Script in S3 as Asset
        from aws_cdk.aws_s3_assets import Asset
        from os import path
        dirname = path.dirname(__file__)
        asset = Asset(self.scope, "Asset", path=path.join(dirname, "configure.sh"))
        local_path = instance.user_data.add_s3_download_command(
            bucket=asset.bucket,
            bucket_key=asset.s3_object_key
        )
        # Userdata executes script from S3
        instance.user_data.add_execute_file_command(
            file_path=local_path
            )
        asset.grant_read(instance.role)
        """