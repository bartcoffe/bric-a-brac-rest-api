import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct


class Vpc(cdk.Stack):
    # Vpc creates a VPC that spans a whole region.
    # It will automatically divide the provided VPC CIDR range, and create public and private subnets per Availability Zone.
    # Network routing for the public subnets will be configured to allow outbound access directly via an Internet Gateway.
    # Network routing for the private subnets will be configured to allow outbound access via a set of resilient NAT Gateways (one per AZ).
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = ec2.Vpc(
            self,
            id='my_vpc',
            cidr="10.0.0.0/16",
            # the CIDR range to use for the VPC, e.g. ‘10.0.0.0/16’.
            # Should be a minimum of /28 and maximum size of /16. The range will be split across all subnets per Availability Zone.
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='public',
                    cidr_mask=28,
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name='private_isolated',
                    cidr_mask=28,
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                )
            ],
        )
