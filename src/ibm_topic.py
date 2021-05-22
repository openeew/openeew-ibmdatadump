# import modules
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.database import CloudantDatabase

import time
import pandas as pd
import json
import os
import datetime


class Topic2IBM:
    """This class gets the devices from Cloudant"""

    def __init__(self, topic_list, params, topic) -> None:
        """Initializes the DataReceiver object"""
        super().__init__()
        self.params = params
        self.topic = topic
        self.topic_list = topic_list

        client = Cloudant(
            os.environ["CLOUDANT_USERNAME"],
            os.environ["CLOUDANT_PASSWORD"],
            url=os.environ["CLOUDANT_URL"],
        )
        client.connect()

        if self.topic == "event":
            database_name = self.params["event_table_name"]
        elif self.topic == "detection":
            database_name = self.params["detection_table_name"]

        self.db = client[database_name]

    def message2cloudant(self, topic_list):

        data = self.topic_list.data

        if self.topic == "detection":
            for message in data:
                self.db.create_document(message)

                print("✅ Wrote " + self.topic + " to the cloudant database.")
                self.topic_list.data = []

        elif self.topic == "event":

            # get cloud time
            dt = datetime.datetime.now(datetime.timezone.utc)
            utc_time = dt.replace(tzinfo=datetime.timezone.utc)
            cloud_t = utc_time.timestamp()

            # repeat for all unique events
            unique_events = list(set([n["event_id"] for n in data]))

            for event_id in unique_events:
                event_entries = [n for n in data if n["event_id"] == event_id]
                max_time = max([n["cloud_t"] for n in event_entries])

                if max_time + self.params["max_pause"] < cloud_t:

                    out_dict = {"event_id": event_id}
                    id = 1

                    for message in event_entries:
                        out_dict[id] = message
                        id += 1

                    self.db.create_document(out_dict)

                    print("✅ Wrote " + self.topic + " to the cloudant database.")
                    self.topic_list.data = []

    def run(self):
        # run loop indefinitely
        while True:

            # try to get devices from cloud
            self.message2cloudant(self.topic_list)

            time.sleep(self.params["sleep_time_save"])
