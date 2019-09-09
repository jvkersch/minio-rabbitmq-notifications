minio-rabbitmq-notifications
============================

Setup
-----

Set up the containers with
```
export DATA_DIR=/where/minio/data/is/stored
CURRENT_UID=$(id -u):$(id -g) docker-compose up
```

On the host, set up a Minio configuration
```
mc config host add myminio http://localhost:9000 access secret123
```

Create a bucket named `bucket`, and add a notification rule
```
mc mb bucket
mc event add  myminio/bucket arn:minio:sqs::1:amqp
```

Limitations
-----------

After deploying the stack with Docker compose, you must restart the minio
service by
```
mc admin service restart myminio
```

To use the upload.py and download.py utilities, the ``minio`` host must resolve
to localhost. To achieve this, add the line ``127.0.0.1 minio`` to your
``/etc/hosts/`` file. This will be avoided in a future version by running the
tools inside a container that has access to the Docker DNS.
