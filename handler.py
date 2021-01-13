import json
import boto3
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def pdftotext(event, context):
    key = event.get('queryStringParameters', {}).get('key')
    if key == None:
        return {
            "statusCode": 200,
            "body": "Missing 'key' query parameter to fetch from S3"
        }

    s3 = boto3.client('s3')
    path = '/tmp/file.pdf'
    s3.download_file('vstiba-provas', key, path)
    text = convert_pdf_to_txt(path)

    response = {
        "statusCode": 200,
        "body": text,
        "headers": {
            "Content-Type": "text/plain; charset=utf-8"
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
