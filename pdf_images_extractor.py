import fitz
import boto3
import os

IMAGES_PATH = '/tmp/images'


def extract_and_upload_images(path, event):
    if not os.path.exists(IMAGES_PATH):
        os.mkdir(IMAGES_PATH)

    extract_images(path)
    images = __upload_images(event)
    __remove_images()
    return images


def extract_images(path):
    doc = fitz.open(path)
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha < 4:  # this is GRAY or RGB
                pix.writePNG("%s/p%s-%s.png" % (IMAGES_PATH, i, xref))
            else:  # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("%s/p%s-%s.png" % (IMAGES_PATH, i, xref))
                pix1 = None
            pix = None


def __upload_images(event):
    s3_folder = event.get('queryStringParameters', {}).get('folder')
    images = os.listdir(IMAGES_PATH)
    keys = []
    for filename in images:
        absolute_path = "%s/%s" % (IMAGES_PATH, filename)
        s3_key = "%s/%s" % (s3_folder, filename)
        file = __upload_file(s3_key, absolute_path)
        keys.append(s3_key)
    return keys


def __remove_images():
    images = os.listdir(IMAGES_PATH)
    for filename in images:
        absolute_path = "%s/%s" % (IMAGES_PATH, filename)
        os.remove(absolute_path)


def __upload_file(key, file_name):
    s3 = boto3.client('s3')
    return s3.upload_file(file_name, os.environ.get(
        'S3_BUCKET'), key, ExtraArgs={'ACL': 'public-read'})
