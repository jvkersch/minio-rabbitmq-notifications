""" Dispatch Minio file notifications to Flask server endpoint.
"""

import json
import os
import pprint
import sys
import time
import urllib

import pika
import requests

MESSAGE_HOST = "localhost:5672"
UPLOAD_URL = "http://localhost:5000/file/status/{key}"


def _process_event(ch, method, properties, body):
    data = json.loads(body.decode())
    key = os.path.basename(data["Key"])
    pprint.pprint(data)

    try:
        _toggle_upload_status(key)
    except Exception as e:
        print(f"ERROR: {e}")


def _toggle_upload_status(key):
    url = UPLOAD_URL.format(key=urllib.parse.quote(key))
    response = requests.patch(url)
    response.raise_for_status()


def setup_channel(callback):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(
        exchange=MESSAGE_HOST, exchange_type='fanout', durable=True
    )

    result = channel.queue_declare(
        "bucket-notifications", durable=True, exclusive=False
    )
    queue_name = result.method.queue
    channel.queue_bind(
        exchange='bucket-notifications', queue=queue_name
    )
    channel.basic_consume(
        queue_name, callback, auto_ack=True
    )
    return channel


def main():
    channel = setup_channel(_process_event)
    channel.start_consuming()


if __name__ == '__main__':
    nfailures = 0
    backoffs = (1, 1) # (1, 2, 4, 8)
    for backoff in backoffs:
        try:
            main()
        except Exception as e:
            nfailures += 1
            print("fifi", e, flush=True, file=sys.stderr)
            time.sleep(backoff)
        else:
            break

    if nfailures == len(backoffs):
        raise SystemExit()
