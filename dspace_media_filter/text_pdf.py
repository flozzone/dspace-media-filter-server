import tempfile

from PyPDF2 import PdfFileReader

from dspace_media_filter.filter import MediaFilterResponse, MediaFilterRequest
from dspace_media_filter.text import TextFilter


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
