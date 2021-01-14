import unittest
from pdf_to_text import PdfToText

PDF_FIXTURE_PATH = 'fixtures/sample.pdf'


class TestPdfToText(unittest.TestCase):
    def test_text_extraction(self):
        text = PdfToText(PDF_FIXTURE_PATH).convert()
        self.assertTrue(text.find('A Simple PDF File') > 0)
        self.assertTrue(text.find('This is a small demonstration') > 0)
        self.assertTrue(text.find('Simple PDF File 2') > 0)
        self.assertTrue(text.find('...continued from page 1') > 0)
