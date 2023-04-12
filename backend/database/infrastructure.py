import aws_cdk as cdk
import aws_cdk.aws_rds as rds
import aws_cdk.aws_ec2 as ec2
from constructs import Construct


class Database(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.db_ec2_sg = ec2.SecurityGroup(
            self,
            'db_ec2_sg',
            vpc=vpc,
            allow_all_outbound=True,
        )
        self.db_ec2_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(5432),
            description='allow db traffic',
        )
        self.db_ec2_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv6(),
            connection=ec2.Port.tcp(5432),
            description='allow db traffic',
        )

        self.db = rds.DatabaseInstance(
            self,
            'bricabrac_db',
            database_name='bricabrac',
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_15_2),
            credentials=rds.Credentials.from_password('postgres', cdk.SecretValue.unsafe_plain_text('password')),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3,
                                              ec2.InstanceSize.MICRO),
            backup_retention=cdk.Duration.days(0),
            delete_automated_backups=True,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            security_groups=[self.db_ec2_sg],
        )
