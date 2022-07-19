from bs4 import BeautifulSoup

from dspace_media_filter.filter import MediaFilterRequest
from dspace_media_filter.text import TextFilter


class FilterModule(TextFilter):
    def filter_text(self, req: MediaFilterRequest) -> str:
        return BeautifulSoup(self.read_text_file(req.abs_file)).get_text()

    @staticmethod
    def read_text_file(path: str) -> str:
        with open(path, 'r') as f:
            return f.read()


