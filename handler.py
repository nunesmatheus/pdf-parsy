import boto3
import os
from pdf_to_text import convert as convert_to_text
from pdf_images_extractor import extract_and_upload_images
import json


def pdf_to_text(event, context):
    key = file_key(event)
    if key == None:
        return missing_key_response()

    path = download_file(key)
    text = convert_to_text(path)

    response = {
        "statusCode": 200,
        "body": json.dumps({"text": text}),
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
        }
    }

    return response


def pdf_images(event, context):
    key = file_key(event)
    if key == None:
        return missing_key_response()

    path = download_file(key)
    images = extract_and_upload_images(path, event)

    response = {
        "statusCode": 200,
        "body": json.dumps({"images": images}),
        "headers": {
            "Content-Type": "application/json"
        }
    }

    return response


def file_key(event):
    return event.get('queryStringParameters', {}).get('key')


def missing_key_response():
    {
        "statusCode": 200,
        "body": "Missing 'key' query parameter to fetch from S3"
    }


def download_file(key):
    s3 = boto3.client('s3')
    path = '/tmp/file.pdf'
    s3.download_file(os.environ.get('S3_BUCKET'), key, path)
    return path
