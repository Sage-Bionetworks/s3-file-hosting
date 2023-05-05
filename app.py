#!/usr/bin/env python3
import os

import aws_cdk as cdk

from serverless_backend.serverless_backend_stack import ServerlessBackendStack
import helpers

app = cdk.App(context=helpers.get_deployment_context())
ServerlessBackendStack(app, "S3FileUpload",
    )

app.synth()
