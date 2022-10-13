from celery import shared_task
import subprocess
import pysrt
import boto3
import os
from botocore.exceptions import ClientError

# Getting AWS Creds. from Env.
AWS_ACCESS_KEY_ID = str(os.getenv('AWS_ACCESS_KEY_ID'))
AWS_SECRET_ACCESS_KEY = str(os.getenv('AWS_ACCESS_KEY'))
s3_client = boto3.client('s3',aws_access_key_id =AWS_ACCESS_KEY_ID,aws_secret_access_key =AWS_SECRET_ACCESS_KEY)
dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'ap-south-1',
                                    aws_access_key_id = AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
subtitle_table = dynamo_client.Table('bezencce')

'''
Celery Task to upload any data to dynamoDB
'''


@shared_task
def dynamodb_put_data(data):
    subtitle_table.put_item(Item = data)

def get_subtitles_from_db(pkey):
    return subtitle_table.get_item(Key = {'ccextractor':pkey})
'''
Celery Task to extract subtitles using CCExtractor and upload them to DynamoDb
'''
@shared_task
def get_and_upload_to_db(filename,pkey):
    print(f"Extracting Subtitles from {filename}")
    cmd = ["ccextractor", filename, "-stdout"]
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = proc.communicate()
    data = {
        "ccextractor":str(pkey),
        "index": [],
        "start": [],
        "end": [],
        "position": [],
        "text": [],
    }
    if stdout:
        processed_titles = pysrt.from_string(stdout)
        for subtitles in processed_titles:
            st_data = subtitles.__dict__
            for key, val in st_data.items():
                data[key].append(str(val))
        dynamodb_put_data(data)
        print("Data Uploaded to DynamoDB")
        return data
    print("No data Found")
    return None


'''Celery Task for uploading video to S3 Bucket'''
@shared_task
def upload_to_bucket(file_name:str, bucket:str, object_name=None):
    print(f"Uploading {file_name} to {bucket}")

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        print(e)
        return False
    return True