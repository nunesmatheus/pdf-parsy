import os
from pdf_to_text import PdfToText
from pdf_images_extractor import PdfImagesExtractor
from aws import s3_client, s3_bucket
import json


def pdf_to_text(event, context):
    # TODO: query param name should be more meaningful, like pdf_s3_key
    # TODO: folder query param name should be more meaningful, like images_s3_folder
    key = file_key(event)
    if key == None:
        return missing_key_response()

    path = download_file(key)
    text = PdfToText(path).convert()

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
    s3_folder = event.get('queryStringParameters', {}).get('s3_images_folder')
    images = PdfImagesExtractor(
        pdf_path=path, s3_images_folder=s3_folder).extract_and_upload_images()

    response = {
        "statusCode": 200,
        "body": json.dumps({"images": images}),
        "headers": {
            "Content-Type": "application/json"
        }
    }

    return response


def file_key(event):
    return event.get('queryStringParameters', {}).get('s3_pdf_key')


def missing_key_response():
    return {
        "statusCode": 200,
        "body": json.dumps({"error": "Missing 'key' query parameter to fetch from S3"}),
        "headers": {
            "Content-Type": "application/json"
        }
    }


def download_file(key):
    path = '/tmp/file.pdf'
    s3_client().download_file(s3_bucket(), key, path)
    return path
