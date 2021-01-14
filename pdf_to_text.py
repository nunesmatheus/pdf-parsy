from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


class PdfToText:
    def __init__(self, path):
        self.path = path

    def convert(self):
        file = open(self.path, 'rb')
        text = self.__process_pages(file)
        file.close()
        return text


    def __process_pages(self, file):
        retstr = StringIO()
        resource_manager = PDFResourceManager()
        interpreter = self.__interpreter(resource_manager, retstr)
        for page in PDFPage.get_pages(fp=file, pagenos=set(), maxpages=0, caching=True, check_extractable=True):
            interpreter.process_page(page)
        interpreter.device.close()
        text = retstr.getvalue()
        retstr.close()
        return text


    def __interpreter(self, resource_manager, retstr):
        device = TextConverter(resource_manager, retstr, codec='utf-8',
                               laparams=self.__layout_params())
        return PDFPageInterpreter(rsrcmgr=resource_manager, device=device)


    def __layout_params(self):
        # Default LAParams: char_margin=2.0, line_margin=0.5, word_margin=0.1 all_texts=False
        laparams = LAParams()
        laparams.line_margin = 20.0
        laparams.char_margin = 10.0
        return laparams
