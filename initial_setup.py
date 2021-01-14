#!/usr/local/bin/python

import fileinput
import os

with open('fixtures/pdf_input.json', 'r') as file:
    filedata = file.read()

s3_object = os.environ.get('S3_SAMPLE_OBJECT_KEY')
s3_images_folder = os.environ.get('S3_SAMPLE_IMAGES_FOLDER')

filedata = filedata.replace('s3_pdf_key', s3_object)
filedata = filedata.replace('s3_images_folder', s3_images_folder)

with open('fixtures/pdf_input.json', 'w') as file:
    file.write(filedata)
