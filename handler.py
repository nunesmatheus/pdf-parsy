import json
import boto3
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import fitz
import os
import base64


def pdf_to_text(event, context):
    key = file_key(event)
    if key == None:
        return missing_key_response()

    path = download_file(key)
    text = convert_pdf_to_txt(path)

    response = {
        "statusCode": 200,
        "body": text,
        "headers": {
            "Content-Type": "text/plain; charset=utf-8"
        }
    }

    return response

def pdf_images(event, context):
    key = file_key(event)
    if key == None:
        return missing_key_response()

    path = download_file(key)
    doc = fitz.open(path)
    images_directory = '/tmp/images'
    if not os.path.exists(images_directory):
        os.mkdir(images_directory)

    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha < 4:       # this is GRAY or RGB
                pix.writePNG("%s/p%s-%s.png" % (images_directory, i, xref))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("%s/p%s-%s.png" % (images_directory, i, xref))
                pix1 = None
            pix = None

    images = []
    for filename in os.listdir(images_directory):
        absolute_path = "%s/%s" % (images_directory, filename)
        with open(absolute_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode('ascii')
            images.append(encoded)
            os.remove(absolute_path)

    response = {
        "statusCode": 200,
        "body": {
            "images": images
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }

    return response


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    # Default LAParams: char_margin=2.0, line_margin=0.5, word_margin=0.1 all_texts=False
    laparams.line_margin = 20.0
    laparams.char_margin = 10.0
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

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
