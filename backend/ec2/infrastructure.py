import aws_cdk as cdk
import aws_cdk.aws_s3_assets as assets
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
import aws_cdk.aws_rds as rds
from constructs import Construct
import secrets


class Ec2(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc,
                 database: rds.DatabaseInstance, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

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

        drf_role = iam.Role(
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

        self.instance = ec2.Instance(
            self,
            'ec2_drf',
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            role=drf_role,
            security_group=drf_sg,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,
                                              ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2))

        bricabrac_drf = assets.Asset(self,
                                     "drf_asset",
                                     path='backend/ec2/bric-a-brac-drf')
        bricabrac_drf.grant_read(self.instance)

        user_data = [
            #install needed software
            "yum update -y",
            "amazon-linux-extras install python3.8 -y",
            "amazon-linux-extras install nginx1 -y",
            "PATH=$PATH:/usr/local/bin && echo PATH=$PATH:/usr/local/bin >> /etc/environment",
            #download django app
            f"aws s3 cp {bricabrac_drf.s3_object_url} srv/bricabrac_drf",
            "unzip /srv/bricabrac_drf",
            "pip3.8 install -r requirements.txt",
            #set up environment
            f"export DB_HOST={database.db.db_instance_endpoint_address} && echo export DB_HOST={database.db.db_instance_endpoint_address} >> /etc/environment",
            f"export DB_PORT={database.db.db_instance_endpoint_port} && echo export DB_PORT={database.db.db_instance_endpoint_port} >> /etc/environment",
            "export export DB_NAME=bricabrac && echo export DB_NAME=bricabrac >> /etc/environment",
            "export DB_USER=postgres && echo export DB_USER=postgres >> /etc/environment",
            "export DB_PASSWORD=password && echo export DB_PASSWORD=password >> /etc/environment",
            f"export SECRET_KEY={secrets.token_hex(100)} && echo export SECRET_KEY={secrets.token_hex(100)} >> /etc/environment",
            "env > bricabrac.env",
            #set up server
            "python3.8 manage.py migrate bricabrac",
            "ln -s /my_services/bricabrac.service /etc/systemd/system/",
            "ln -s /locations.conf /etc/nginx/default.d/",
            "rm -rf /usr/share/nginx/html",
            "ln -s /html /usr/share/nginx/",
            "systemctl start bricabrac",
            "systemctl start nginx"
        ]

        self.instance.add_user_data(*user_data)
