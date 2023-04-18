import aws_cdk as cdk
import aws_cdk.aws_rds as rds
import aws_cdk.aws_ec2 as ec2
from constructs import Construct


class Database(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        db_ec2_sg = ec2.SecurityGroup(
            self,
            'db_ec2_sg',
            vpc=vpc,
            allow_all_outbound=False,
        )
        db_ec2_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4('10.0.0.0/24'),
            connection=ec2.Port.tcp(5432),
            description='allow ingress db traffic',
        )
        db_ec2_sg.add_egress_rule(
            peer=ec2.Peer.ipv4('10.0.0.0/24'),
            connection=ec2.Port.all_traffic(),
            description='allow egress db traffic',
        )

        self.db = rds.DatabaseInstance(
            self,
            'bricabrac_db',
            database_name='bricabrac',
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_15_2),
            allocated_storage=5,
            credentials=rds.Credentials.from_password('postgres', cdk.SecretValue.unsafe_plain_text('password')),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3,
                                              ec2.InstanceSize.MICRO),
            backup_retention=cdk.Duration.days(0),
            delete_automated_backups=True,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            security_groups=[db_ec2_sg],
        )
