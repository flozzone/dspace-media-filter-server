from PyPDF2 import PdfFileReader

from dspace_media_filter.filter import MediaFilterRequest
from dspace_media_filter.text import TextFilter


class FilterModule(TextFilter):
    def filter_text(self, req: MediaFilterRequest) -> str:
        # read PDF contents
        with open(req.abs_file, 'rb') as pdfFile:
            pdf_reader = PdfFileReader(pdfFile)
            return '\n'.join([pdf_reader.getPage(i).extractText() for i in range(0, pdf_reader.numPages)])
