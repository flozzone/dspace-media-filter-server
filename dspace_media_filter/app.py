import os

from flask import Flask
from flask import request

from dspace_media_filter.manager import MediaFilterManager

app = Flask(__name__)

manager = MediaFilterManager(os.getenv('MEDIA_FILTER_CACHE_DIR', "/tmp/media-filter-cache"))


@app.route("/<mediatype>", methods=['POST'], defaults={'filetype': None})
@app.route("/<mediatype>/<filetype>", methods=['POST'])
def filter_media(mediatype, filetype):
    return manager.filter(request, mediatype, filetype).to_json()
