import os
import sys

from flask import Flask
from flask import request

from dspace_media_filter.filter import MediaFilterRequest, MediaFilterResponse
from dspace_media_filter.text_pdf import PDFFilter
from dspace_media_filter.thumbnail import ThumbnailFilter

app = Flask(__name__)


pdf_filter = PDFFilter()
thumbnail_filter = ThumbnailFilter()


@app.route("/text/pdf", methods=['POST'])
def text_pdf():
    req = MediaFilterRequest(request.get_json())

    if not os.path.exists(req.abs_file):
        return MediaFilterResponse(error=f"File {req.abs_file} not found").to_json()

    try:
        filter_response = pdf_filter.filter(req)
    except:
        return MediaFilterResponse(error=f"An unexpected error occured {sys.exc_info()[0]}").to_json()

    return filter_response.to_json()


@app.route("/thumbnail", methods=['POST'])
def thumbnail():
    req = MediaFilterRequest(request.get_json())

    if not os.path.exists(req.abs_file):
        return MediaFilterResponse(error=f"File {req.abs_file} not found").to_json()

    try:
        filter_response = thumbnail_filter.filter(req)
    except:
        return MediaFilterResponse(error=f"An unexpected error occured {sys.exc_info()[0]}").to_json()

    return filter_response.to_json()
