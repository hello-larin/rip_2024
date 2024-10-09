from django.conf import settings
from minio import Minio
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.response import *

def process_file_upload(file_object: InMemoryUploadedFile, client, image_name):
    try:
        client.put_object('lab1', image_name, file_object, file_object.size)
        return f"http://localhost:9000/lab1/{image_name}"
    except Exception as e:
        return {"error": str(e)}

def add_pic(product, pic):
    client = Minio(           
        endpoint=settings.AWS_S3_ENDPOINT_URL,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        secure=settings.MINIO_USE_SSL
    )
    i = product.id
    img_obj_name = f"{i}.png"

    if not pic:
        print("HELLO55")
        return {"error": "Нет файла для изображения логотипа."}
    result = process_file_upload(pic, client, img_obj_name)

    if 'error' in result:
        print(result)
        return result
    return {"message": result}


def del_pic(product):
    client = Minio(           
        endpoint=settings.AWS_S3_ENDPOINT_URL,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        secure=settings.MINIO_USE_SSL
    )
    result = client.remove_object(bucket_name='lab1',object_name=f'{product.id}.png')
    if result == 'None':
        print(result)
        return {"error": "File not found"}

    return {"message": "success"}