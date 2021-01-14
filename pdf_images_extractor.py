import fitz
import boto3
import os
from aws import s3_client, s3_bucket
from PIL import Image
import io

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
        pdf_file = fitz.open(self.pdf_path)

        for page_index in range(len(pdf_file)):
            page = pdf_file[page_index]
            image_list = page.getImageList()
            for image_index, img in enumerate(image_list, start=1):
                # get the XREF of the image
                xref = img[0]
                # extract the image bytes
                base_image = pdf_file.extractImage(xref)
                image_bytes = base_image["image"]
                # get the image extension
                image_ext = base_image["ext"]
                # load it to PIL
                image = Image.open(io.BytesIO(image_bytes))
                # save it to local disk
                image.save(
                    open(f"{IMAGES_PATH}/image{page_index+1}_{image_index}.{image_ext}", "wb"))

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
