from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import core, pipelines


class CdkPipeline:
    def __init__(self, scope: core.Construct, repo: str, branch: str) -> None:
        self.scope = scope
        self.repo = repo
        self.branch = branch
        self.source_artifact = codepipeline.Artifact()
        self.cloud_assembly_artifact = (
            codepipeline.Artifact()
        )  # basic unit of deployment for cdk
        self.source_action = self.github_source_action()

    def github_source_action(self) -> cpactions.GitHubSourceAction:
        source_action = cpactions.GitHubSourceAction(
            action_name="GitHub",
            output=self.source_artifact,
            oauth_token=core.SecretValue.secrets_manager("github-token"),
            owner="nroldanf",
            repo=self.repo,
            branch=self.branch,
            trigger=cpactions.GitHubTrigger.POLL,
        )
        return source_action

    # def build_image_action(self) -> cpactions.CodeBuildAction:

    #     #
    #     codepipeline.Pipeline

    #     cpactions.CodeBuildAction()
    #     return None

    def cdk_pipeline(self):
        # CDK pipeline definition
        pipeline = pipelines.CdkPipeline(
            self.scope,
            "Pipeline",
            cloud_assembly_artifact=self.cloud_assembly_artifact,
            pipeline_name="RemixerPipeline",
            source_action=self.source_action,
        )
        return pipeline
