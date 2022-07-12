from flask import Flask
from flask import request

from dspace_media_filter.manager import MediaFilterManager

app = Flask(__name__)

manager = MediaFilterManager()


@app.route("/<mediatype>", methods=['POST'])
@app.route("/<mediatype>/<filetype>", methods=['POST'])
def filter_media(mediatype, filetype):
    return manager.filter(request, mediatype, filetype).to_json()
