# DSpace filter-media server

A microservice replacement for the DSpace in-built `filter-media` functionality.

# Motivation

* Use more sophisticated libraries and system tools for text extraction and text filtering
* Offload DSpace host by creating the possibilities to run this on another host
* Develop and deploy the filter-media server independently of DSpace software
* Others could make use of this in other applications then DSpace

## Installation

Currently, installation is only supported directly from the GIT repository.

### System dependencies

#### Debian and derivates

```shell
sudo apt-get install python3 python3-venv

# for image previews
sudo apt-get install poppler-utils libfile-mimeinfo-perl libimage-exiftool-perl ghostscript libsecret-1-0 zlib1g-dev libjpeg-dev imagemagick libmagic1 webp
```

### Setup

Install Python 3.8 or higher

```shell
# download the repo
git clone git@github.com:flozzone/dspace-media-filter-server.git
cd dspace-media-filter-server

# setup a virtual environment
python -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

## Usage

Start the server:

```shell
cd dspace_media_filter
flask run
# look at the console output for the port
```
Download a pdf to `/tmp/test.pdf` and execute the following in another terminal.

```shell
# To extract text from a PDF
curl -X POST -H 'Content-Type: application/json' -d '{"file":"/tmp/test.pdf"}' http://localhost:5000/text/pdf

# To generate a thumbnail image of a PDF
curl -X POST -H 'Content-Type: application/json' -d '{"file":"/tmp/test.pdf"}' http://localhost:5000/thumbnail/pdf
```
