# OpenEEW IBM Data Dump code

## Introduction

The algorithm subscribes to MQTT detections and events and saves them to IBM Cloudant storage.

Create an .env file that contains details for your Cloudant and MQTT
<Details to come soon>

To build this docker image execute the following command:

```
docker build --tag ibm-data-dump:dev .
```

To run the docker image locally run the following command:

```
docker run \
  --interactive \
  --detach \
  --env-file .env \
  --name ibm-data-dump \
  ibm-data-dump:dev
```