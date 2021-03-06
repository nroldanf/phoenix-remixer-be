import setuptools

with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="phoenix_remixer_be",
    version="0.0.1",
    description="Loka Phoenix Remixer CDK Stack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Loka Phoenix Team",
    package_dir={"": "phoenix_remixer_be"},
    packages=setuptools.find_packages(where="phoenix_remixer_be"),
    install_requires=[
        "aws-cdk.core==1.112.0",
        "aws-cdk.aws_iam==1.112.0",
        "aws-cdk.aws_sqs==1.112.0",
        "aws-cdk.aws_sns==1.112.0",
        "aws-cdk.aws_sns_subscriptions==1.112.0",
        "aws-cdk.aws_s3==1.112.0",
        "aws-cdk.aws-ec2==1.112.0",
        "aws-cdk.aws-kms==1.112.0",
        "aws-cdk.pipelines==1.112.0",
        "aws-cdk.aws-codepipeline-actions==1.112.0",
        " aws-cdk.aws-codepipeline==1.112.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
