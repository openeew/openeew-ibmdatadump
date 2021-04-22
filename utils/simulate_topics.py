"""Simulates traces to an MQTT Server. Takes a .JSONL file and publishes each line to MQTT"""

import json
import glob
from argparse import ArgumentParser
from paho.mqtt.client import Client as MqttClient

import pandas as pd
import time
from datetime import datetime


def run():

    if self.params["MQTT"]=="IBM":
        # create a client
        client = create_client(
            host=os.environ["MQTT_HOST"],
            port=1883,
            username=os.environ["MQTT_USERNAME"],
            password=os.environ["MQTT_PASSWORD"],
            clientid=os.environ["MQTT_CLIENTID"]+self.topic,
        )

    elif self.params["MQTT"]=="local":
        # create a client
        client = create_client(
            host="localhost",
            port=1883,
            username="NA",
            password="NA",
            clientid="NA:"+self.topic,
        )
 
    publish_json(
        arguments.directory + "test_detections.json",
        client,
        "iot-2/type/OpenEEW/id/pr/evt/detection/fmt/json",
    )

    publish_json(
        arguments.directory + "test_events.json",
        client,
        "iot-2/type/OpenEEW/id/pr/evt/event/fmt/json",
    )


def create_client(host, port, username, password):
    """Creating an MQTT Client Object"""
    client = MqttClient()

    if username and password:
        client.username_pw_set(username=username, password=password)

    client.connect(host=host, port=port)
    return client


def publish_json(data_path, client, topic):
    """Publish each line of a jsonl given a directory"""

    # loop over all *.jsonl files in a folder
    for filepath in glob.iglob(data_path):

        print("Processing:" + filepath)

        with open(filepath, "r") as json_file:
            json_array = json.load(json_file)

            for message in json_array:
                client.publish(topic, json.dumps(message))
                print("published " + topic)


run()
