import importlib
import os
import subprocess
import sys
import traceback
from abc import ABC
import logging as log

from dspace_media_filter.filter import MediaFilterResponse, MediaFilterRequest, MediaFilter


class MediaFilterManager(ABC):
    def __init__(self, main_cache_dir: str = "/tmp/filter-media-cache", enabled_filters_csv: str = None):
        self.filters = {}
        self.filter_modules = []
        self.main_cache_dir = main_cache_dir
        self.enabled_filters = None
        if enabled_filters_csv:
            self.enabled_filters = enabled_filters_csv.split(",")

        self.register_module("text_pdf")
        self.register_module("thumbnail")
        self.register_module("text_pptx")
        self.register_module("text_html")
        self.register_module("text_docx")

        self.import_modules()

    def register_module(self, filter_module_name: str):
        if self.enabled_filters and filter_module_name not in self.enabled_filters:
            log.info(f"Filter {filter_module_name} is disabled")
            return

        log.info(f"Enabling media-filter module {filter_module_name}")
        self.filter_modules.append(filter_module_name)

    def import_modules(self):
        for filter_module in self.filter_modules:
            log.info(f"Importing {filter_module}")

            media_filter = self.create_filter_from_module(filter_module)
            self.filters[filter_module] = media_filter

    def create_filter_from_module(self, filter_module: str) -> MediaFilter:
        media_filter_module = importlib.import_module(f"dspace_media_filter.{filter_module}")
        return media_filter_module.FilterModule(cache_dir=os.path.join(self.main_cache_dir, filter_module))

    def get_media_filter(self, media_type, file_type):
        filter_name = media_type
        if file_type:
            filter_name += f"_{file_type}"

        return self.filters.get(filter_name, None)

    def filter(self, request, media_type, file_type) -> MediaFilterResponse:
        req = MediaFilterRequest(request.get_json())

        if not os.path.exists(req.abs_file):
            return MediaFilterResponse(error=f"File {req.abs_file} not found")

        media_filter = self.get_media_filter(media_type, file_type)
        if media_filter is None:
            return MediaFilterResponse(error=f"No media filter for {media_type} and {file_type} found or enabled")

        try:
            return media_filter.filter(req)
        except subprocess.CalledProcessError as e:
            traceback.print_exc()
            sys.stderr.flush()
            sys.stdout.flush()
            outp = "Check server logs"
            if e.output and len(e.output) > 0:
                outp = e.output
            return MediaFilterResponse(error=f"A process exited with {e.returncode} while calling "
                                             f"'{' '.join(e.cmd)}'\n OUTPUT: {outp}\nSTACKTRACE: {sys.exc_info()[0]}")
        except:
            traceback.print_exc()
            sys.stderr.flush()
            return MediaFilterResponse(error=f"An unexpected error occured {sys.exc_info()[0]}")
