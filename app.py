#!/usr/bin/env python3

from aws_cdk import core

from phoenix_remixer_be.phoenix_remixer_be_stack import PhoenixRemixerBeStack

parameters = {"name": "Remixer"}

app = core.App()
PhoenixRemixerBeStack(app, "phoenix-remixer-be", parameters)

app.synth()
