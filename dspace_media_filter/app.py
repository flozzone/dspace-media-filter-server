import os
import sys

from flask import Flask
from flask import request

from dspace_media_filter.filter import MediaFilterRequest, PDFFilter, MediaFilterResponse

app = Flask(__name__)


pdf_filter = PDFFilter()


@app.route("/pdf", methods=['POST'])
def pdf():
    filter_request = request.get_json()

    req = MediaFilterRequest(filter_request)

    if not os.path.exists(req.abs_file):
        return MediaFilterResponse(error=f"File {req.abs_file} not found").to_json()

    try:
        filter_response = pdf_filter.filter(req)
    except:
        return MediaFilterResponse(error=f"An unexpected error occured {sys.exc_info()[0]}").to_json()

    return filter_response.to_json()
