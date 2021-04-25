"""This script receives trace data from MQTT by subscribing to a topic"""
import json
from argparse import ArgumentParser
from paho.mqtt.client import Client as MqttClient
import datetime
import time
import pandas as pd
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.database import CloudantDatabase
import os


class ReceiveTopic:
    """This class subscribes to the MQTT and receivces raw data"""

    def __init__(self, topic_list, topic, params) -> None:
        """Initializes the DataReceiver object"""
        super().__init__()
        self.params = params
        self.topic = topic
        self.topic_list = topic_list

    def run(self):
        """
        Main method that creates client and executes the rest of the script

        MQTT variable in params (params["MQTT"]) define whether local, or IBM MQTT is used
        """

        if self.params["MQTT"] == "IBM":
            # create a client
            client = self.create_client(
                host=os.environ["MQTT_HOST"],
                port=os.environ["MQTT_PORT"],
                username=os.environ["MQTT_USERNAME"],
                password=os.environ["MQTT_PASSWORD"],
                clientid=os.environ["MQTT_CLIENTID"] + self.topic,
            )

        elif self.params["MQTT"] == "local":
            # create a client
            client = self.create_client(
                host="localhost",
                port=1883,
                username="NA",
                password="NA",
                clientid="NA:" + self.topic,
            )

        client.loop_forever()

    def create_client(self, host, port, username, password, clientid):
        """Creating an MQTT Client Object"""
        client = MqttClient(clientid)

        if username and password:
            client.username_pw_set(username=username, password=password)

        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(host=host, port=port)
        return client

    def on_connect(self, client, userdata, flags, resultcode):
        """Upon connecting to an MQTT server, subscribe to the topic
        The production topic is 'iot-2/type/OpenEEW/id/+/evt/+/fmt/json'"""

        region = self.params["region"]

        topic = "iot-2/type/OpenEEW/id/" + region + "/evt/" + self.topic + "/fmt/json"
        print(f"✅ Subscribed to detection topic with result code {resultcode}")
        client.subscribe(topic)

    def on_message(self, client, userdata, message):
        """When a message is sent to a subscribed topic,
        decode the message and send it to another method"""
        try:
            decoded_message = str(message.payload.decode("utf-8", "ignore"))
            data = json.loads(decoded_message)

            self.topic_list.data.append(data)

        except BaseException as exception:
            print(exception)
