import fitz
import boto3
import os
from aws import s3_client, s3_bucket
from PIL import Image

IMAGES_PATH = '/tmp/images'


class PdfImagesExtractor:
    def __init__(self, pdf_path, s3_images_folder):
        self.pdf_path = pdf_path
        self.s3_images_folder = s3_images_folder

    def extract_and_upload_images(self):
        self.__create_images_directory()
        self.extract_images()
        images = self.__upload_images()
        self.__remove_images()
        return images

    def extract_images(self):
        doc = fitz.open(self.pdf_path)

        images = []
        for page in range(len(doc)):
            previous_rect = [-1, -1, -1, -1]
            for pdf_image in doc.getPageImageList(page, full=True):
                image_path = self.__save_image(
                    doc=doc, image=pdf_image, page=page)
                image = Image.open(image_path)
                rect = doc[page].getImageBbox(pdf_image)
                if round(rect[1], 2) == round(previous_rect[3], 2):
                    images.append(image)
                else:
                    if len(images) > 1:
                        self.__merge_images(images)
                    images = [image]
                previous_rect = rect

    def __create_images_directory(self):
        if os.path.exists(IMAGES_PATH):
            return

        os.mkdir(IMAGES_PATH)

    def __upload_images(self):
        images = os.listdir(IMAGES_PATH)
        keys = []
        for filename in images:
            absolute_path = "%s/%s" % (IMAGES_PATH, filename)
            s3_key = "%s/%s" % (self.s3_images_folder, filename)
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

    def __save_image(self, doc, image, page):
        xref = image[0]
        pix = fitz.Pixmap(doc, xref)
        image_path = "%s/p%s-%s.png" % (IMAGES_PATH, page, xref)
        if pix.n - pix.alpha < 4:  # this is GRAY or RGB
            pix.writePNG(image_path)
        else:  # CMYK: convert to RGB first
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            pix1.writePNG(image_path)
            pix1 = None
        pix = None
        return image_path

    def __merge_images(self, images):
        size = 0
        total_height = 0
        for image in images:
            total_height += image.size[1]

        x = y = 0
        new_image = Image.new('RGB', (images[0].size[0], total_height))
        for image in images:
            new_image.paste(image, (x, y))
            if os.path.exists(image.filename):
                os.remove(image.filename)
            y += image.size[1]
        new_image.save(images[0].filename, "PNG")
