
from ...config.credentials import s3_client,s3_resource

## verify if the file exist in S3
def get_existing_fn(bucket:str, prefix:str):
    return list(s3_resource.Bucket(bucket).objects.filter(Prefix=prefix))
   

## save The file in S3
def save_file_in_S3(bucket:str, url:str, file):
    s3_resource.Object(bucket, url+'.'+file.filename.split('.')[-1]).put(Body=file.file)
    return True

##get file name in S3
def get_file_name_in_S3(url:str):
    image_name = list(s3_resource.Bucket('data354-public-assets').objects.filter(Prefix=url))[0].key
    return image_name

## get file url in S3
def get_file_url_in_S3(image_name):
    image_url = s3_client.generate_presigned_url(
                ClientMethod='get_object', 
                Params={'Bucket': 'data354-public-assets', 'Key': image_name},
                ExpiresIn=60)
    return image_url