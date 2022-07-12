FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ=Etc/UTC

RUN apt-get update && apt-get install -y python3 python3-pip \
    exiftool poppler-utils libfile-mimeinfo-perl libimage-exiftool-perl ghostscript libsecret-1-0 zlib1g-dev libjpeg-dev imagemagick libmagic1 webp && \
    rm -rf /var/lib/apt/lists/* \
    mkdir /media-filter

WORKDIR /media-filter

RUN pip install gunicorn

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /media-filter

WORKDIR /media-filter

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "dspace_media_filter.app:app"]
