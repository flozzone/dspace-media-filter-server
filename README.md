# DSpace filter-media server

A microservice replacement for the DSpace in-built `filter-media` functionality.

# Motivation

* Use more sophisticated libraries and system tools for text extraction and text filtering
* Offload DSpace host by creating the possibilities to run this on another host
* Develop and deploy the filter-media server independently of DSpace software
* Others could make use of this in other applications then DSpace

# Features

* Can extract text from PDF, PPTX, HTML files.
* Can create thumbnails of various file types (see 
[supported-mimetypes](https://github.com/algoo/preview-generator/blob/develop/doc/supported_mimetypes.rst) from `preview-generator`)

## Installation

Currently, installation is only supported directly from the GIT repository. So you need to checkout
the repository somewhere.

```shell
# clone the repo
git clone git@github.com:flozzone/dspace-media-filter-server.git
```

### Docker container

The easiest way to build the dspace-filter-media-server is to build the container using the Dockerfile
inside the GIT repository. But you need to copy the files in and out from the container.

```shell
docker build -t media-filter .
```

Run the resulting container with:

```shell
docker run --rm -p 5000:5000 --name media-filter media-filter
```

And copy files in and out.

```shell
# copy files into container
docker cp /tmp/test.pdf media-filter:/tmp

# copy output file (according to the filter response) from container out to the host
docker cp media-filter:/tmp/tmp2lyp8vem /tmp/out.text

# or directly watch the file
docker exec -it media-filter cat /tmp/tmp2lyp8vem
```

### Local setup

#### Dependencies for Debian and derivates

```shell
# install Python 3.8 or higher
sudo apt-get install python3 python3-venv

# for image previews get the following
sudo apt-get install exiftool poppler-utils libfile-mimeinfo-perl libimage-exiftool-perl ghostscript libsecret-1-0 zlib1g-dev libjpeg-dev imagemagick libmagic1 webp
```

### Setup

```shell
# cd into it
cd dspace-media-filter-server

# setup a virtual environment
python -m venv venv

# and use it
source venv/bin/activate

# to install python dependencies
pip install -r requirements.txt
```

## Usage

Start the server:

```shell
# if you've not sourced your venv yet
source venv/bin/activate

# enter the subdirectory
cd dspace_media_filter

# and let flask find your app.py, look at the console output for the port
flask run
```
Download the required files to `/tmp` and execute the proper command in another terminal.

```shell
# To extract text from a PDF
curl -X POST -H 'Content-Type: application/json' -d '{"file":"/tmp/test.pdf"}' http://localhost:5000/text/pdf

# To extract text from a PPTX presentation
curl -X POST -H 'Content-Type: application/json' -d '{"file":"/tmp/test.pptx"}' http://localhost:5000/text/pptx

# To extract text from a HTML file
curl -X POST -H 'Content-Type: application/json' -d '{"file":"/tmp/test.html"}' http://localhost:5000/text/html

# You can let text also directly be passed inside the response object
curl -X POST -H 'Content-Type: application/json' -d '{"file":"/tmp/test.html", "returnText":true}' http://localhost:5000/text/html

# To generate a thumbnail image of a PDF
curl -X POST -H 'Content-Type: application/json' -d '{"file":"/tmp/test.pdf"}' http://localhost:5000/thumbnail
```
