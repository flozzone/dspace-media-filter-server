import re
from abc import ABC

from nltk import RegexpTokenizer

from dspace_media_filter.filter import MediaFilter


class TextFilter(MediaFilter, ABC):
    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.expr = re.compile(r"[\w_-]{4,}")

    def clean_text(self, text: str) -> str:
        tokens = self.tokenizer.tokenize(text)
        return ' '.join(filter(lambda x: self.expr.match(x), tokens))
