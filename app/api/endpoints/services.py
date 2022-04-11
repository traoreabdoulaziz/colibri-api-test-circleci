#This file is responsible to write the main endpoints (Store and fetch image from Amazon S3)

from email.mime import image
from fileinput import filename
#from tkinter import image_names
from fastapi import APIRouter, File, Depends, HTTPException, UploadFile
from starlette.responses import StreamingResponse
#import boto3
from PIL import Image
import io
import requests
import datetime
from .auth import get_current_user
from .model import UserIn_Pydantic, User_Pydantic, User
from ..config.credentials import s3_client,s3_resource
from .utils.S3_service import get_file_url_in_S3,get_existing_fn,save_file_in_S3
router = APIRouter()
DT_FMT_FN = '%Y%m%d%H%M%S'
OUTPUT_BUCKET = 'data354-public-assets'


#Endpoint to store image taxpayer on S3
@router.post("/upload_taxpayer_info/", tags=["S3 api"])
async def create_taxpayer_file(id: str,type:str, file: UploadFile = File(...), current_user: User_Pydantic = Depends(get_current_user)):
    if type not in ["photo_id","face_id","certificate"]:
        return {"message": "Type not exist","code": "0"}
    # if not exist_file_in_s3(output_folder):
    #     return {"message":"File already exist","code":"-1"}
    output_folder = 'fastapi-test/TAXPAYER/Taxpayer-'+id+'/'+type+'/'
    output_fn = datetime.datetime.utcnow().strftime(DT_FMT_FN)
    image_url = output_folder+output_fn
    #Save to s3
    save_file_in_S3(OUTPUT_BUCKET, image_url,file)
    return {"message":"File upload to S3","code":"1"}

#Endpoint to store image activity on S3
@router.post("/upload_activity_info/", tags=["S3 api"])
async def create_activity_file(id: str,type:str, file: UploadFile = File(...), current_user: User_Pydantic = Depends(get_current_user)):
    if type in ["photo_activity","cadaster","certificate"]:
             return {"message": "Type not exist","code": "0"}
    # if not exist_file_in_s3(output_folder):
    #     return {"message":"File already exist","code":"-1"}
    output_folder = 'fastapi-test/ACTIVITY/Activity-'+id+'/'+type+'/'
    output_fn = datetime.datetime.utcnow().strftime(DT_FMT_FN)
    image_url = output_folder+output_fn
    #Save to s3
    save_file_in_S3(OUTPUT_BUCKET, image_url,file)
    return {"message":"File upload to S3","code":"1"}
       
#Endpoint to download taxpayer image from S3
@router.get("/download_taxpayer_info/", tags=["S3 api"])
async def get_taxpayer_file(id: str,type:str,current_user: User_Pydantic = Depends(get_current_user)):
    if type not in ["photo_id","face_id","certificate"]:
        return {"message": "Type not exist","code": "0"}
    output_folder = 'fastapi-test/TAXPAYER/Taxpayer-'+id+'/'+type+'/'
    existing_files = get_existing_fn(OUTPUT_BUCKET, output_folder)
    if not existing_files:
        return {"message": "Information not found","code": "-1"}
    key_tab=[]
    for s3_object in existing_files:
        key_tab.append(s3_object.key)
    last_file = sorted(key_tab)[-1]
    presigned_url = get_file_url_in_S3(last_file)
    return {"message": "success","code": "1","image_url":presigned_url}

#Endpoint to download taxpayer image from S3
@router.get("/download_activity_info/", tags=["S3 api"])
async def get_activity_image(id: str,type:str,current_user: User_Pydantic = Depends(get_current_user)):
    if type in ["photo_activity","cadaster","certificate"]:
        return {"message": "Type not exist","code": "0"}
    output_folder = 'fastapi-test/ACTIVITY/Activity-'+id+'/'+type+'/'
    existing_files = get_existing_fn(OUTPUT_BUCKET, output_folder)
    if not existing_files:
        return {"message": "Information not found","code": "-1"}
    key_tab=[]
    for s3_object in existing_files:
        key_tab.append(s3_object.key)
    last_file = sorted(key_tab)[-1]
    presigned_url = get_file_url_in_S3(last_file)
    return {"message": "success","code": "1","image_url":presigned_url}


#Endpoint to store image on S3
@router.post("/upload_image/", tags=["S3 api"])
async def create_file(id: str, file: UploadFile = File(...), current_user: User_Pydantic = Depends(get_current_user)):

    s3_resource.Object('data354-public-assets', 'fastapi-test/'+id+'.'+file.filename.split('.')[-1]).put(Body=file.file)
    
    return {"message": "File upload in S3"}


#Endpoint to get image from S3
@router.get("/get_image/", tags=["S3 api"])
async def get_image(id: str, current_user: User_Pydantic = Depends(get_current_user)):
    try:
        image_name = list(s3_resource.Bucket('data354-public-assets').objects.filter(Prefix='fastapi-test/'+id))[-1].key
        print(list(s3_resource.Bucket('data354-public-assets').objects.filter(Prefix='fastapi-test/'+id)))
        image_url = s3_client.generate_presigned_url(
                ClientMethod='get_object', 
                Params={'Bucket': 'data354-public-assets', 'Key': image_name},
                ExpiresIn=60)

        return {"image_url": image_url}
    except:
        return {"error": "ID is not correct"}


#Endpoint to get informations from s3
@router.get("/account/", tags=["Frontend api"])
async def get_info(id: str, current_user: User_Pydantic = Depends(get_current_user)):
    try:
        image_name = list(s3_resource.Bucket('data354-public-assets').objects.filter(Prefix='fastapi-test/'+id))[-1].key
        image_url = s3_client.generate_presigned_url(
                ClientMethod='get_object', 
                Params={'Bucket': 'data354-public-assets', 'Key': image_name},
                ExpiresIn=60)

        pdf_url = s3_client.generate_presigned_url(
                ClientMethod='get_object', 
                Params={'Bucket': 'data354-public-assets', 'Key': 'AT2345.pdf'},
                ExpiresIn=3600)

        return {"Name": "Kesse Michel", "Telephone": "0504737370", 
            "Entreprise": "Boutique de chaussure",
            "Emplacement": "Quartier Lac SAN PEDRO",
            "image_url":image_url, "pdf_url":pdf_url}
    except:
        return {"error": "ID is not correct"}

