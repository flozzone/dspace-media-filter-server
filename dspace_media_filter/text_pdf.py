from PyPDF2 import PdfFileReader

from dspace_media_filter.filter import MediaFilterRequest
from dspace_media_filter.text import TextFilter


class PDFFilter(TextFilter):
    def filter_text(self, req: MediaFilterRequest) -> str:
        text = ''

        # read PDF contents
        with open(req.abs_file, 'rb') as pdfFile:
            pdf_reader = PdfFileReader(pdfFile)
            for i in range(0, pdf_reader.numPages):
                # creating a page object
                page = pdf_reader.getPage(i)
                # extracting text from page
                text += page.extractText()

        return self.clean_text(text)
