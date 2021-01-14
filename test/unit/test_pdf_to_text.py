import unittest
import sys
from pdf_to_text import convert


class TestPdfToText(unittest.TestCase):
    def test_text_extraction(self):
        text = convert('fixtures/sample.pdf')
        self.assertTrue(text.find('A Simple PDF File') > 0)
        self.assertTrue(text.find('This is a small demonstration') > 0)
        self.assertTrue(text.find('Simple PDF File 2') > 0)
        self.assertTrue(text.find('...continued from page 1') > 0)
