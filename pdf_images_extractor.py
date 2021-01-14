import fitz
import boto3
import os
from aws import s3_client, s3_bucket

IMAGES_PATH = '/tmp/images'


class PdfImagesExtractor:
    def __init__(self, pdf_path, event):
        self.pdf_path = pdf_path
        self.event = event

    def extract_and_upload_images(self):
        self.__create_images_directory()
        self.extract_images(self.pdf_path)
        images = self.__upload_images()
        self.__remove_images()
        return images

    def extract_images(self, path):
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

    def __create_images_directory(self):
        if os.path.exists(IMAGES_PATH):
            return

        os.mkdir(IMAGES_PATH)

    def __upload_images(self):
        s3_folder = self.event.get('queryStringParameters', {}).get('folder')
        images = os.listdir(IMAGES_PATH)
        keys = []
        for filename in images:
            absolute_path = "%s/%s" % (IMAGES_PATH, filename)
            s3_key = "%s/%s" % (s3_folder, filename)
            file = self.__upload_file(key=s3_key, file_name=absolute_path)
            keys.append(s3_key)
        return keys

    def __remove_images(self):
        images = os.listdir(IMAGES_PATH)
        for filename in images:
            absolute_path = "%s/%s" % (IMAGES_PATH, filename)
            os.remove(absolute_path)

    def __upload_file(self, key, file_name):
        return s3_client().upload_file(
            file_name, s3_bucket(), key, ExtraArgs={'ACL': 'public-read'})
