import aws_cdk as core
import aws_cdk.assertions as assertions

from bric_a_brac_server.bric_a_brac_server_stack import BricABracServerStack

# example tests. To run these tests, uncomment this file along with the example
# resource in bric_a_brac_server/bric_a_brac_server_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BricABracServerStack(app, "bric-a-brac-server")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
