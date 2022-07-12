import json
import os
import re
from abc import ABC
import tempfile

from PyPDF2 import PdfFileReader
from nltk.tokenize import RegexpTokenizer
from preview_generator.manager import PreviewManager


class MediaFilterRequest(object):
    def __init__(self, data):
        self.abs_file = data['file']


class MediaFilterResponse(object):
    def __init__(self, result_file_path=None, error=None):
        self.resultFile = result_file_path
        self.error = error

    def to_json(self):
        return json.dumps({
            "resultFile": self.resultFile,
            "error": self.error
        }, ensure_ascii=False)


class MediaFilter(ABC):
    def filter(self, req: MediaFilterRequest) -> MediaFilterResponse:
        raise NotImplementedError("MediaFilter logic not implemented")


class TextFilter(MediaFilter, ABC):
    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.expr = re.compile(r"[\w_-]{4,}")

    def clean_text(self, text: str) -> str:
        tokens = self.tokenizer.tokenize(text)
        return ' '.join(filter(lambda x: self.expr.match(x), tokens))


cache_path = '/tmp/preview_cache'


class PDFFilter(TextFilter):
    def filter(self, req: MediaFilterRequest) -> MediaFilterResponse:
        text = ''

        # read PDF contents
        with open(req.abs_file, 'rb') as pdfFile:
            pdf_reader = PdfFileReader(pdfFile)
            for i in range(0, pdf_reader.numPages):
                # creating a page object
                page = pdf_reader.getPage(i)
                # extracting text from page
                text += page.extractText()

        # write filtered contents to file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as result_file:
            result_file.write(self.clean_text(text))

            return MediaFilterResponse(result_file_path=result_file.name)


class ThumbnailFilter(MediaFilter):
    manager = PreviewManager(cache_path, create_folder=True)

    def filter(self, req: MediaFilterRequest) -> MediaFilterResponse:
        return MediaFilterResponse(result_file_path=self.manager.get_jpeg_preview(req.abs_file))
