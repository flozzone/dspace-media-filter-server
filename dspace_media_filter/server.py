from flask import Flask
from flask import request

from dspace_media_filter.filter import MediaFilterRequest, PDFFilter

app = Flask(__name__)


@app.route("/extract", methods=['POST'])
def pdf():
    media_request = request.get_json()

    req = MediaFilterRequest(media_request)

    if req.filter_type == 'pdf':
        filter = PDFFilter()
        resp = filter.filter(req)
        return resp.to_json()

    return f"MediaFilter: {media_request}"
