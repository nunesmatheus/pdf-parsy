import fileinput
import os
import sys

with open('fixtures/pdf_input.json', 'r') as file:
    filedata = file.read()

s3_object = os.environ.get('S3_SAMPLE_OBJECT_KEY')
s3_images_folder = os.environ.get('S3_SAMPLE_IMAGES_FOLDER')

if (filedata.find('s3_pdf_key') == -1) or (filedata.find('s3_images_folder') == -1):
    print('It looks like the sample input has been set already... Maybe revert changes on git?')
    sys.exit()

filedata = filedata.replace('s3_pdf_key', s3_object)
filedata = filedata.replace('s3_images_folder', s3_images_folder)

with open('fixtures/pdf_input.json', 'w') as file:
    file.write(filedata)

print('Sample data has been successfully saved on fixtures/pdf_input.json! You might want to commit the changes written.')
