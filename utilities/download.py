""" Simple script to download file objects from the file store.

Usage::

  python utilities/download.py <file1> <file2> <...>

"""


import json
import os
import sys
import requests


def download_file(key):
    """ Two-stage file download.
    """

    # Get metadata
    response = requests.get(f"http://localhost:5000/file/{key}")
    response.raise_for_status()

    data = response.json()
    print(data)

    if data["status"] != "uploaded":
        raise RuntimeError(f"File {key} has not been fully uploaded yet")

    # Get file data
    data_url = data['url']
    with open(key, 'wb') as fp:
        response = requests.get(data_url)
        response.raise_for_status()
        fp.write(response.content)


if __name__ == '__main__':
    for key in sys.argv[1:]:
        download_file(key)
