#!/usr/bin/env python3
import os

import aws_cdk as cdk

from backend.component import Backend

app = cdk.App()

Backend(
    app,
    "BackendServer",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                        region=os.getenv('CDK_DEFAULT_REGION')),
)

app.synth()
