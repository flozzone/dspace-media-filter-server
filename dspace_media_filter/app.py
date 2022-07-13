import os
import logging as log

from flask import Flask
from flask import request

from dspace_media_filter.manager import MediaFilterManager

log.basicConfig(level=os.getenv('MEDIA_FILTER_LOG_LEVEL', log.WARN))

app = Flask(__name__)

manager = MediaFilterManager(
    main_cache_dir=os.getenv('MEDIA_FILTER_CACHE_DIR', "/tmp/media-filter-cache"),
    enabled_filters_csv=os.getenv('MEDIA_FILTER_ENABLED_MODULES', None)
)


@app.route("/<mediatype>", methods=['POST'], defaults={'filetype': None})
@app.route("/<mediatype>/<filetype>", methods=['POST'])
def filter_media(mediatype, filetype):
    return manager.filter(request, mediatype, filetype).to_json()
