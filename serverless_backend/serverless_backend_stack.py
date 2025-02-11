from aws_cdk import (
    Stack,
    aws_s3 as _s3,
    aws_lambda as _lambda,
    aws_apigateway as _apigateway,

)
from constructs import Construct
import os


class ServerlessBackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        my_bucket = _s3.Bucket(self, id='s3bucket',
                               bucket_name=self.node.try_get_context("bucketName"))
        my_lambda = _lambda.Function(self, id='lambdafunction', function_name="formlambda", runtime=_lambda.Runtime.PYTHON_3_7,
                         handler='index.handler',
                         code=_lambda.Code.from_asset(
                             os.path.join("./", "lambda-handler")),
                         environment={
                             'bucket': my_bucket.bucket_name
                         }
                     )
        my_bucket.grant_read_write(my_lambda)
        my_api = _apigateway.LambdaRestApi(
            self, id='lambdaapi', rest_api_name='formapi', handler=my_lambda, proxy=True)
        postData = my_api.root.add_resource("form")
        postData.add_method("POST")
