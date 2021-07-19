#!/usr/bin/env python3

from aws_cdk import core

from phoenix_remixer_be.phoenix_remixer_be_stack import PhoenixRemixerBeStack


app = core.App()
PhoenixRemixerBeStack(app, "phoenix-remixer-be")

app.synth()
