import io

from flask import Flask
from flask import request

from dspace_media_filter.filter import MediaFilterRequest, PDFFilter

app = Flask(__name__)


@app.route("/extract", methods=['POST'])
def extract():
    media_request = request.get_json()

    req = MediaFilterRequest(media_request)

    if req.filter_type == 'pdf':
        with open(req.abs_file, 'rb') as pdfFile:
            f = PDFFilter()
        resp = f.filter(pdfFile)
        return resp.to_json()

    return f"MediaFilter: {media_request}"


@app.route("/pdf", methods=['POST'])
def pdf():
    stream = io.BufferedReader(request.stream)
    f = PDFFilter()
    resp = f.filter(stream)
    return resp.to_json()
