import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct


class Vpc(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            id='my_vpc',
            cidr="10.0.0.0/16",
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='public',
                    cidr_mask=24,
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name='private_isolated',
                    cidr_mask=28,
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                )
            ],
        )
