import docx

from dspace_media_filter.filter import MediaFilterRequest
from dspace_media_filter.text import TextFilter


class FilterModule(TextFilter):
    @staticmethod
    def filter_name():
        return "text_docx"

    def filter_text(self, req: MediaFilterRequest) -> str:
        doc = docx.Document(req.abs_file)

        return '\n'.join([para.text for para in doc.paragraphs])
