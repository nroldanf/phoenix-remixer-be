import json

# import pytest
from aws_cdk import core

from phoenix_remixer_be.phoenix_remixer_be_stack import PhoenixRemixerBeStack


def get_template():
    app = core.App()
    PhoenixRemixerBeStack(app, "phoenix-remixer-be")
    return json.dumps(app.synth().get_stack("phoenix-remixer-be").template)


def test_sqs_queue_created():
    assert "AWS::SQS::Queue" in get_template()


def test_sns_topic_created():
    assert "AWS::SNS::Topic" in get_template()
