import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

from backend.database.infrastructure import Database
from backend.vpc.infrastructure import Vpc
from backend.ec2.infrastructure import Ec2
# from backend.amplify.infrastructure import Amplify


class Backend(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = Vpc(self, 'my_vpc')

        database = Database(self, 'flashcards_postgres', vpc.vpc)

        ec2_instance = Ec2(self, 'drf_ec2', vpc=vpc.vpc, database=database)
