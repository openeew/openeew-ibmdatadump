# import modules
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.database import CloudantDatabase

from dotenv import dotenv_values
import time
import pandas as pd
import json

ibm_cred = dotenv_values()

SERVICE_USERNAME = ibm_cred["SERVICE_USERNAME"]
SERVICE_PASSWORD = ibm_cred["SERVICE_PASSWORD"]
SERVICE_URL = ibm_cred["SERVICE_URL"]


class Topic2IBM:
    """This class gets the devices from Cloudant"""

    def __init__(self, topic_list, params, topic, ibm_cred) -> None:
        """Initializes the DataReceiver object"""
        super().__init__()
        self.params = params
        self.topic = topic
        self.ibm_cred = ibm_cred
        self.topic_list = topic_list

        client = Cloudant(SERVICE_USERNAME, SERVICE_PASSWORD, url=SERVICE_URL)
        client.connect()

        if self.topic == "event":
            database_name = self.params["event_table_name"]
        elif self.topic == "detection":
            database_name = self.params["detection_table_name"]

        self.db = client[database_name]

    def message2cloudant(self, topic_list):

        data = self.topic_list.data

        for message in data:
            self.db.create_document(message)

        self.topic_list.data = []

    def run(self):
        # run loop indefinitely
        while True:

            # try to get devices from cloud
            self.message2cloudant(self.topic_list)

            print("✅ Wrote topic to the cloudant database.")

            time.sleep(self.params["sleep_time_save"])
