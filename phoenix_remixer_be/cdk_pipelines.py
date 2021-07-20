from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import core


class CdkPipeline:
    def __init__(self, scope: core.Construct, repo: str, branch: str) -> None:
        self.scope = scope
        self.repo = repo
        self.branch = branch
        self.source_artifact = codepipeline.Artifact()
        self.build_output_artifact = codepipeline.Artifact()
        self.cloud_assembly_artifact = (
            codepipeline.Artifact()
        )  # basic unit of deployment for cdk

        self.source_action = self.github_source_action()
        self.ecr_repo = self.ecr_repository()
        self.artifact_bucket = self.get_artifact_bucket()

    def get_artifact_bucket(self) -> s3.Bucket:
        lifecycle_rule = s3.LifecycleRule(expiration=core.Duration.days(2))
        artifact_bucket = s3.Bucket(
            scope=self.scope,
            id="remixer-artifacts-bucket",
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=False,
            lifecycle_rules=[lifecycle_rule],
        )
        return artifact_bucket

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

    def ecr_repository(self) -> ecr.Repository:
        ecr_repo = ecr.Repository(
            scope=self.scope,
            id="remixer-ecr-repo",
        )
        ecr_repo.add_lifecycle_rule(max_image_age=core.Duration.days(7))
        return ecr_repo

    def _build_project_policy(self) -> iam.PolicyStatement:
        return iam.PolicyStatement(
            actions=[
                "codebuild:CreateReportGroup",
                "codebuild:CreateReport",
                "codebuild:BatchPutTestCases",
                "codebuild:UpdateReport",
                "codebuild:StartBuild",
            ],
            resources=["*"],
        )

    def codebuild_project(self) -> codebuild.PipelineProject:
        return codebuild.PipelineProject(
            scope=self.scope,
            id="remixer-build-project",
            project_name="RemixerProject",
            description="Build the docker image for remixer",
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_3_0(),
                privileged=True,
                compute_type=codebuild.ComputeType.MEDIUM,
            ),
            environment_variables={
                "REPOSITORY_URI": codebuild.BuildEnvironmentVariable(
                    value=self.ecr_repo.repository_uri
                )
            },
            timeout=core.Duration.minutes(15),
            cache=codebuild.Cache.bucket(
                self.artifact_bucket, prefix="codebuild-cache"
            ),
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yaml"),
        )

    def cdk_pipeline(self) -> codepipeline.Pipeline:
        # CDK pipeline definition
        pipeline = codepipeline.Pipeline(
            scope=self.scope,
            id="pipeline",
            artifact_bucket=self.artifact_bucket,
            pipeline_name="RemixerPipeline",
            restart_execution_on_update=True,
        )
        # source stage action
        source_action = self.github_source_action()

        # build stage action with CodeBuild
        self.ecr_repo = self.ecr_repository()
        build_project = self.codebuild_project()
        # Add policy
        build_project_policy = self._build_project_policy()
        build_project.add_to_role_policy(build_project_policy)
        self.ecr_repo.grant_pull_push(build_project)

        # Add the stages to the pipeline
        # 1. Source
        pipeline.add_stage(stage_name="GitHubSource", actions=[source_action])
        # 2. Build stage
        pipeline.add_stage(
            stage_name="BuildStage",
            actions=[
                cpactions.CodeBuildAction(
                    action_name="CodeBuildProjectAction",
                    input=self.source_artifact,
                    outputs=[self.build_output_artifact],
                    project=build_project,
                    type=cpactions.CodeBuildActionType.BUILD,
                    run_order=1,
                )
            ],
        )
        return pipeline
