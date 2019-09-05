""" Simple script to upload some files to the file storage.

Usage::

  python utilities/upload.py <file1> <file2> <...>

"""


import json
import os
import sys
import requests


def upload_file(path):
    """ Two-stage upload (metadata, followed by file data).
    """
    print(f"Uploading {path}")

    # Store metadata with a POST request
    fname = os.path.basename(path)
    response = requests.post(f"http://localhost:5000/file/{fname}",
                             json={'owner': 'foo'})
    response.raise_for_status()

    data = response.json()
    print(data)

    # Upload file data with a PUT request. Note: this is currently done by
    # reading all data into memory, which is not efficient for large
    # files. However, this can be done with any other protocol for HTTP uploads
    # (e.g. chunked iterative uploading).
    upload_url = data['url']
    with open(path, 'rb') as fp:
        response = requests.put(
            upload_url, data=fp.read(),
            headers={'Content-Type': 'application/octet-stream'})
    response.raise_for_status()


if __name__ == '__main__':
    for path in sys.argv[1:]:
        upload_file(path)
