"""
This is the main file that runs the OpenEEW code package
"""

# import modules
import time
from threading import Thread
import os

from params import params
from src import receive_topic, data_holders, ibm_topic


def main():
    """Does everything"""

    # Create a Detections DataFrame.
    detections = data_holders.Detections()

    # Create a Events DataFrame.
    events = data_holders.Events()

    # We create and start receive detection worker
    detection_rec = receive_topic.ReceiveTopic(
        topic_list=detections, topic="detection", params=params
    )
    det_rec_process = Thread(target=detection_rec.run)
    det_rec_process.start()

    # We create and start receive event worker
    event_rec = receive_topic.ReceiveTopic(
        topic_list=events, topic="event", params=params
    )
    ev_rec_process = Thread(target=event_rec.run)
    ev_rec_process.start()

    # We create and start publish detection worker
    detection_send = ibm_topic.Topic2IBM(
        topic_list=detections, topic="detection", params=params
    )
    det_send_process = Thread(target=detection_send.run)
    det_send_process.start()

    # We create and start publish event worker
    event_send = ibm_topic.Topic2IBM(topic_list=events, topic="event", params=params)
    ev_send_process = Thread(target=event_send.run)
    ev_send_process.start()

    # We join our Threads, i.e. we wait for them to finish before continuing
    det_rec_process.join()
    ev_rec_process.join()
    det_send_process.join()
    ev_send_process.join()


if __name__ == "__main__":

    main()
