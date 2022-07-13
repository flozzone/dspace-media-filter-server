FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ=Etc/UTC

RUN apt-get update && apt-get install -y python3 python3-pip \
    exiftool poppler-utils libfile-mimeinfo-perl libimage-exiftool-perl ghostscript libsecret-1-0 zlib1g-dev libjpeg-dev imagemagick libmagic1 webp && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /media-filter /tmp/media-filter-cache && \
    useradd -ms /bin/bash mediafilter && \
    chown -R mediafilter:mediafilter /media-filter /tmp/media-filter-cache && \
    chmod g=u /media-filter /tmp/media-filter-cache

# install gunicorn separately since its just used in the container atm
RUN pip install gunicorn

USER mediafilter

WORKDIR /media-filter

# copy requirements before code, so when code changes it will use cached layer for installed requirements
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN ls -la /tmp

VOLUME /tmp/media-filter-cache

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "dspace_media_filter.app:app"]
