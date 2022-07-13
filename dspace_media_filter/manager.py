import os
import sys
import traceback
from abc import ABC

from dspace_media_filter.filter import MediaFilterResponse, MediaFilterRequest
from dspace_media_filter.text_docx import DOCXTextFilter
from dspace_media_filter.text_html import HTMLTextFilter
from dspace_media_filter.text_pdf import PDFFilter
from dspace_media_filter.text_pptx import PPTTextFilter
from dspace_media_filter.thumbnail import ThumbnailFilter


class MediaFilterManager(ABC):
    def __init__(self, main_cache_dir=None):
        self.pdf_text_filter = PDFFilter(cache_dir=os.path.join(main_cache_dir, "pdf-text"))
        self.thumbnail_filter = ThumbnailFilter(cache_dir=os.path.join(main_cache_dir, "thumbnails"))
        self.pptx_text_filter = PPTTextFilter(cache_dir=os.path.join(main_cache_dir, "ppt-text"))
        self.html_text_filter = HTMLTextFilter(cache_dir=os.path.join(main_cache_dir, "html-text"))
        self.docx_text_filter = DOCXTextFilter(cache_dir=os.path.join(main_cache_dir, "docx-text"))

    def filter(self, request, media_type, file_type) -> MediaFilterResponse:
        req = MediaFilterRequest(request.get_json())

        if not os.path.exists(req.abs_file):
            return MediaFilterResponse(error=f"File {req.abs_file} not found")

        if media_type == 'thumbnail':
            media_filter = self.thumbnail_filter
        elif media_type == 'text':
            if file_type == 'pdf':
                media_filter = self.pdf_text_filter
            elif file_type == 'pptx':
                media_filter = self.pptx_text_filter
            elif file_type == 'html':
                media_filter = self.html_text_filter
            elif file_type == 'docx':
                media_filter = self.docx_text_filter
            else:
                return MediaFilterResponse(error=f"Cannot extract text for filetype {file_type}")
        else:
            return MediaFilterResponse(error=f"Unknown target media to handle: {media_type}")

        try:
            return media_filter.filter(req)
        except:
            traceback.print_exc()
            sys.stderr.flush()
            return MediaFilterResponse(error=f"An unexpected error occured {sys.exc_info()}")
