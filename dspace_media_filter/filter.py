import json
from abc import ABC


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




