import sys
sys.path.append('../')
import handler
import unittest


class TestPdfToText(unittest.TestCase):
    def test_text_extraction(self):
        text = handler.convert_pdf_to_txt('fixtures/sample.pdf')
        self.assertTrue(text.find('A Simple PDF File') > 0)
        self.assertTrue(text.find('This is a small demonstration') > 0)
        self.assertTrue(text.find('Simple PDF File 2') > 0)
        self.assertTrue(text.find('...continued from page 1') > 0)
