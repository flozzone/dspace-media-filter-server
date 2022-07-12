# dspace-media-filter

## Setup

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
cd dspace_media_filter
flask run

# look at the console output for the port
```

## Using it

Download a pdf to `/tmp/test.pdf` and execute the following in another terminal.

```shell
curl -X POST -H 'Content-Type: application/json' -d '{"file":"/tmp/test.pdf"}' http://localhost:5000/pdf
```
