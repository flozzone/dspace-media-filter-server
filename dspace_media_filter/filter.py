import json
from abc import ABC


class MediaFilterRequest(object):
    def __init__(self, data):
        self.abs_file = data.get('file')
        self.return_text = data.get('returnText', False)
        self.data = data


class MediaFilterResponse(object):
    def __init__(self, result_file_path=None, error=None, text=None):
        self.resultFile = result_file_path
        self.error = error
        self.text = text

    def to_json(self):
        return json.dumps({
            "resultFile": self.resultFile,
            "error": self.error,
            "text": self.text
        }, ensure_ascii=False)


class MediaFilter(ABC):
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir

    def filter(self, req: MediaFilterRequest) -> MediaFilterResponse:
        raise NotImplementedError("MediaFilter logic not implemented")
