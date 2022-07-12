from bs4 import BeautifulSoup

from dspace_media_filter.filter import MediaFilterRequest
from dspace_media_filter.text import TextFilter


class HTMLTextFilter(TextFilter):
    def filter_text(self, req: MediaFilterRequest) -> str:
        text = BeautifulSoup(self.read_text_file(req.abs_file)).get_text()
        return self.clean_text(text)

    @staticmethod
    def read_text_file(path: str) -> str:
        with open(path, 'r') as f:
            return f.read()


