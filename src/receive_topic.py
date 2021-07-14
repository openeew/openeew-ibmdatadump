"""This script receives trace data from MQTT by subscribing to a topic"""
import json
from paho.mqtt.client import Client as MqttClient

import os
import logging

class ReceiveTopic:
    """This class subscribes to the MQTT and receivces raw data"""

    log_format = "%(asctime)s - module:%(module)s - line:%(lineno)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=log_format)
    logger = logging.getLogger(__name__)

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

        # create a client
        client = self.create_client(
            host=os.environ["MQTT_HOST"],
            port=int(os.environ["MQTT_PORT"]),
            username=os.environ["MQTT_USERNAME"],
            password=os.environ["MQTT_PASSWORD"],
            clientid=os.environ["MQTT_CLIENTID"] + self.topic,
            cafile=os.environ["MQTT_CERT"],
        )

        client.loop_forever()

    def create_client(self, host, port, username, password, clientid, cafile=None):
        """Creating an MQTT Client Object"""
        client = MqttClient(clientid)

        if username and password:
            client.username_pw_set(username=username, password=password)
        else:
            self.logger.warn("Proceeding without username and password")

        if cafile:
            client.tls_set(ca_certs=cafile)
        else:
            self.logger.warn("Proceeding without certificate file")

        try:
            client.on_connect = self.on_connect
            client.on_message = self.on_message
            client.connect(host=host, port=port)
        except OSError as error:
            self.logger.error(error)

        return client

    def on_connect(self, client, userdata, flags, resultcode):
        """Upon connecting to an MQTT server, subscribe to the topic
        The production topic is 'iot-2/type/OpenEEW/id/+/evt/+/fmt/json'"""

        topic = "iot-2/type/OpenEEW/id/+/evt/" + self.topic + "/fmt/json"
        self.logging.info(f"✅ Subscribed to detection topic with result code {resultcode}")
        self.logging.info("  Topic {}".format(topic))

        client.subscribe(topic)

    def on_message(self, client, userdata, message):
        """When a message is sent to a subscribed topic,
        decode the message and send it to another method"""
        try:
            decoded_message = str(message.payload.decode("utf-8", "ignore"))
            data = json.loads(decoded_message)

            self.topic_list.data.append(data)

        except (ValueError, BaseException) as exception:
            self.logging.error(exception)
