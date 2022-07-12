import os
import sys
import traceback
from abc import ABC

from dspace_media_filter.filter import MediaFilterResponse, MediaFilterRequest
from dspace_media_filter.text_pdf import PDFFilter
from dspace_media_filter.thumbnail import ThumbnailFilter


class MediaFilterManager(ABC):
    def __init__(self):
        self.pdf_text_filter = PDFFilter()
        self.thumbnail_filter = ThumbnailFilter()

    def filter(self, request, media_type, file_type) -> MediaFilterResponse:
        req = MediaFilterRequest(request.get_json())

        if not os.path.exists(req.abs_file):
            return MediaFilterResponse(error=f"File {req.abs_file} not found")

        if media_type == 'thumbnail':
            media_filter = self.thumbnail_filter
        elif media_type == 'text':
            if file_type == 'pdf':
                media_filter = self.pdf_text_filter
            else:
                return MediaFilterResponse(error=f"Cannot extract text for filetype {file_type}")
        else:
            return MediaFilterResponse(error=f"Unknown target media to handle: {media_type}")

        try:
            return media_filter.filter(req)
        except:
            traceback.print_exc()
            return MediaFilterResponse(error=f"An unexpected error occured {sys.exc_info()[0]}")
