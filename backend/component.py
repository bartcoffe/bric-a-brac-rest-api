import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
from constructs import Construct

cdk.Stack


class Backend(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            'my_vpc',
            cidr="10.0.0.0/16",
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='public',
                    cidr_mask=24,
                    subnet_type=ec2.SubnetType.PUBLIC,
                )
            ],
        )

        drf_sg = ec2.SecurityGroup(
            self,
            'drf_sg',
            vpc=vpc,
            allow_all_outbound=True,
        )

        drf_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description='allow HTTP traffic from anywhere',
        )

        drf_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv6(),
            connection=ec2.Port.tcp(443),
            description='allow HTTPS traffic from anywhere',
        )

        dfr_role = iam.Role(
            self,
            'drf_role',
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonSSMManagedInstanceCore'),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonS3ReadOnlyAccess'),
            ],
        )

        ec2_server = ec2.Instance(
            self,
            'ec2_instance',
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            role=dfr_role,
            security_group=drf_sg,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,
                                              ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
        )

        ec2_server.add_user_data('export MYENVVARIABLE=xdxdxdx', )
