#!/bin/bash

# Obviously, you need to change this.
# FYI, this is just a dev environment. Use an actual HTTP server for static data and audio requests.

# And a proxy in front of the API.

conda activate slice
python -m http.server --bind 127.0.0.1 5001 --directory data/SAMPLES/sample/OLD_LIBRARY &
python -m http.server --bind 127.0.0.1 3000 --directory slice_static &
python -m flask --app slice_backend run --host 127.0.0.1 --port 5000
