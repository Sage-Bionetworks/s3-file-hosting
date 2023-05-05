from aws_cdk import (
    Stack,
    CfnParameter as _cfnParameter,
    aws_cognito as _cognito,
    aws_s3 as _s3,
    aws_dynamodb as _dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as _apigateway,

)
from constructs import Construct
import os


class ServerlessBackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        bucket_name = _cfnParameter(self, "el-manifests", type="String",
                                    description="Bucket to temporarily store manifest files for the EL Portal.")
        my_bucket = _s3.Bucket(self, id='s3bucket',
                               bucket_name=bucket_name.value_as_string)
        my_lambda = _lambda.Function(self, id='lambdafunction', function_name="formlambda", runtime=_lambda.Runtime.PYTHON_3_7,
                                     handler='index.handler',
                                     code=_lambda.Code.from_asset(
                                         os.path.join("./", "lambda-handler")),
                                     environment={
                                         'bucket': my_bucket.bucket_name
                                     }
                                     )
        my_bucket.grant_read_write(my_lambda)
        my_table.grant_read_write_data(my_lambda)
        my_api = _apigateway.LambdaRestApi(
            self, id='lambdaapi', rest_api_name='formapi', handler=my_lambda, proxy=True)
        postData = my_api.root.add_resource("form")
        postData.add_method("POST")  # POST images/files & metadata
