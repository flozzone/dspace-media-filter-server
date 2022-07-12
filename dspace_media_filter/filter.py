import json
import re
from abc import ABC

from PyPDF2 import PdfFileReader
from nltk.tokenize import RegexpTokenizer


class MediaFilterRequest(object):
    def __init__(self, data):
        self.abs_file = data['file']
        self.filter_type = data['type']


class MediaFilterResponse(object):
    def __init__(self, text):
        self.text = text

    def to_json(self):
        return json.dumps({
            "text": self.text
        }, ensure_ascii=False)


class MediaFilter(ABC):
    def filter(self, req: MediaFilterRequest):
        raise NotImplementedError("MediaFilter logic not implemented")


class TextFilter(MediaFilter, ABC):
    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.expr = re.compile(r"[\w_-]{4,}")

    def clean_text(self, text: str) -> str:
        tokens = self.tokenizer.tokenize(text)
        return ' '.join(filter(lambda x: self.expr.match(x), tokens))


class PDFFilter(TextFilter):

    def filter(self, req: MediaFilterRequest) -> MediaFilterResponse:
        with open(req.abs_file, 'rb') as pdfFile:
            pdf_reader = PdfFileReader(pdfFile)
            text = ''
            for i in range(0, pdf_reader.numPages):
                # creating a page object
                page = pdf_reader.getPage(i)
                # extracting text from page
                text += page.extractText()
            return MediaFilterResponse(text=self.clean_text(text))


