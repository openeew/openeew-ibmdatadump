"""Simulates traces to an MQTT Server. Takes a .JSONL file and publishes each line to MQTT"""

import json
import glob
from argparse import ArgumentParser
from paho.mqtt.client import Client as MqttClient

import pandas as pd
import time
from datetime import datetime


def run():
    """Main method that parses command options and executes the rest of the script"""
    parser = ArgumentParser()
    parser.add_argument(
        "--host", help="An MQTT host", nargs="?", const="localhost", default="localhost"
    )
    parser.add_argument(
        "--port", help="An MQTT port", nargs="?", type=int, const=1883, default=1883
    )
    parser.add_argument(
        "--directory",
        help="A directory containing *.JSONL files",
        nargs="?",
        default="../data/",
    )

    parser.add_argument("--clientid", help="MQTT clientID", default="simulator_topics")

    # If MQTT has username and password authentication on
    parser.add_argument("--username", help="A username for the MQTT Server")
    parser.add_argument("--password", help="A password for the MQTT server")

    arguments = parser.parse_args()

    client = create_client(
        arguments.host, arguments.port, arguments.username, arguments.password
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
