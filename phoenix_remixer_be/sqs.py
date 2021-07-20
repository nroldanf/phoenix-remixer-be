from aws_cdk import aws_iam as iam
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
        removal_policy: core.RemovalPolicy = core.RemovalPolicy.DESTROY,
    ) -> None:
        self.scope = scope
        self.retention_period = retention_period
        self.fifo = True if fifo else None
        self.removal_policy = removal_policy

    def key_policy(self) -> iam.PolicyDocument:
        """
        https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_kms/Key.html
        https://aws.amazon.com/es/premiumsupport/knowledge-center/update-key-policy-future/
        """
        policy_document = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    sid="Allow administration of the key",
                    effect=iam.Effect.ALLOW,
                    # principals=[
                    #     iam.ArnPrincipal(f"aws:iam::{core.Aws.ACCOUNT_ID}:nrf-cdk"),
                    # ],
                    principals=[iam.AccountPrincipal(core.Aws.ACCOUNT_ID)],
                    actions=[
                        "kms:Create*",
                        "kms:Describe*",
                        "kms:Enable*",
                        "kms:List*",
                        "kms:Put*",
                        "kms:Update*",
                        "kms:Revoke*",
                        "kms:Disable*",
                        "kms:Get*",
                        "kms:Delete*",
                        "kms:ScheduleKeyDeletion",
                        "kms:CancelKeyDeletion",
                    ],
                    resources=["*"],
                ),
                iam.PolicyStatement(
                    sid="Allow use of the key",
                    effect=iam.Effect.ALLOW,
                    # principals=[
                    #     iam.ArnPrincipal(f"aws:iam::{core.Aws.ACCOUNT_ID}:nrf-cdk"),
                    # ],
                    principals=[iam.AccountPrincipal(core.Aws.ACCOUNT_ID)],
                    actions=[
                        "kms:Encrypt",
                        "kms:Decrypt",
                        "kms:ReEncrypt*",
                        "kms:GenerateDataKey*",
                        "kms:DescribeKey",
                    ],
                    resources=["*"],
                ),
                iam.PolicyStatement(
                    sid="Allow attachment of persistent resources",
                    effect=iam.Effect.ALLOW,
                    principals=[iam.AccountPrincipal(core.Aws.ACCOUNT_ID)],
                    actions=[
                        "kms:CreateGrant",
                        "kms:ListGrants",
                        "kms:RevokeGrant",
                    ],
                    resources=["*"],
                    conditions={"Bool": {"kms:GrantIsForAWSResource": "true"}},
                ),
            ]
        )
        return policy_document

    def kms_key(self, name) -> kms.Key:
        policy = self.key_policy()
        key = kms.Key(
            self.scope,
            f"{name}-key",
            description="Remixer SQS CMK for encryption",
            policy=policy,
            removal_policy=self.removal_policy,
        )
        return key

    def sqs(self, name: str) -> sqs.Queue:
        name = f"{name}-queue.fifo" if self.fifo else f"{name}-queue"
        # encryption_master_key = self.kms_key(name)
        queue = sqs.Queue(
            self.scope,
            name,
            queue_name=name,
            encryption=sqs.QueueEncryption.KMS_MANAGED,
            # encryption_master_key=encryption_master_key,
            fifo=self.fifo,
            retention_period=self.retention_period,
            removal_policy=self.removal_policy,
        )
        return queue
