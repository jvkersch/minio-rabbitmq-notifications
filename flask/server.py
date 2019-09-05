from datetime import timedelta

from flask import Flask, abort, jsonify, request
from minio import Minio


ACCESS = "access"
SECRET = "secret123"

FILEDATA = {
    "a": {  # just some sample data
        "name": "xyz",
        "status": "uploaded",
    },
    "b": {
        "name": "abc",
        "status": "uploading",
    }

}

client = Minio("minio:9000",
               access_key=ACCESS,
               secret_key=SECRET,
               secure=False)

app = Flask(__name__)


@app.route("/")
def handle_root():
    return "hello world"


@app.route("/file")
def handle_files():
    return jsonify(FILEDATA)


@app.route("/file/<key>", methods=['GET', 'POST'])
def handle_file(key):

    if request.method == "GET":
        try:
            filedata = FILEDATA[key]
        except KeyError:
            abort(404)

        url = client.presigned_get_object(
            'bucket', key, expires=timedelta(seconds=200))

        response = filedata.copy()
        response['url'] = url

        return jsonify(response)
    else:
        print(request.json)
        filedata = request.json.copy()
        filedata["status"] = "uploading"
        FILEDATA[key] = filedata

        url = client.presigned_put_object(
            'bucket', key, expires=timedelta(seconds=200))

        response = {
            'url': url
        }

        return jsonify(response)


@app.route("/file/status/<key>", methods=['PATCH'])
def handle_upload_status(key):
    try:
        filedata = FILEDATA[key]
    except KeyError:
        abort(404)

    filedata["status"] = "uploaded"
    return jsonify(filedata)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
