import re
import tempfile
from abc import ABC, abstractmethod

from nltk import RegexpTokenizer

from dspace_media_filter.filter import MediaFilter, MediaFilterRequest, MediaFilterResponse


class TextFilter(MediaFilter, ABC):
    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.expr = re.compile(r"[\w_-]{4,}")

    def filter(self, req: MediaFilterRequest) -> MediaFilterResponse:

        text = self.filter_text(req)

        result_file = self.write_text_to_file(text)

        return MediaFilterResponse(result_file_path=result_file)

    @abstractmethod
    def filter_text(self, req: MediaFilterRequest) -> str:
        raise NotImplementedError(f"Text filtering is not implemented in {self.__class__.__name__}")

    def clean_text(self, text: str) -> str:
        tokens = self.tokenizer.tokenize(text)
        return ' '.join(filter(lambda x: self.expr.match(x), tokens))

    def write_text_to_file(self, text):
        # write filtered contents to file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as result_file:
            result_file.write(self.clean_text(text))
            return result_file.name
