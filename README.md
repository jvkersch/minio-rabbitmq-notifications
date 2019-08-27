minio-rabbitmq-notifications
============================

Set up the containers with
```
export DATA_DIR=/where/minio/data/is/stored
CURRENT_UID=$(id -u):$(id -g) docker-compose up
```

On the host, set up a Minio configuration
```
mc config host add myminio http://localhost:9000 access secret123
```

Create a bucket, and add a notification rule
```
mc mb my-bucket-name
mc event add  myminio/my-bucket-name arn:minio:sqs::1:amqp
```

Restart Minio
```
mc admin service restart myminio
```
