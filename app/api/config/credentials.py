import boto3

REGION_NAME='eu-west-3'
AWS_ACCESS_KEY_ID="AKIA2KH2OIGSVTEZV4UX"
AWS_SECRET_ACCESS_KEY="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"

s3_resource = boto3.resource(
    's3',
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
s3_client =  boto3.client(
    's3',
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )