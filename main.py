"""
This is the main file that runs the OpenEEW code package
"""

# import modules
import time
from threading import Thread
from dotenv import dotenv_values

from params import params
from src import receive_topic, data_holders, ibm_topic

__author__ = "Vaclav Kuna"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Vaclav Kuna"
__email__ = "kuna.vaclav@gmail.com"
__status__ = ""


def main():
    """Does everything"""
    ibm_cred = dotenv_values()  # take AWS S3 credentials from .env

    # Create a Detections DataFrame.
    detections = data_holders.Detections()

    # Create a Events DataFrame.
    events = data_holders.Events()

    # We create and start detection worker
    detection_rec = receive_topic.ReceiveTopic(topic_list=detections, topic="detection", params=params, ibm_cred=ibm_cred)
    det_rec_process = Thread(target=detection_rec.run)
    det_rec_process.start()

    # We create and start detection worker
    event_rec = receive_topic.ReceiveTopic(topic_list=events, topic="event", params=params, ibm_cred=ibm_cred)
    ev_rec_process = Thread(target=event_rec.run)
    ev_rec_process.start()

    # We create and start detection worker
    detection_send = ibm_topic.Topic2IBM(topic_list=detections, topic="detection", params=params, ibm_cred=ibm_cred)
    det_send_process = Thread(target=detection_send.run)
    det_send_process.start()

    # We create and start detection worker
    event_send = ibm_topic.Topic2IBM(topic_list=events, topic="event", params=params, ibm_cred=ibm_cred)
    ev_send_process = Thread(target=event_send.run)
    ev_send_process.start()

    # We join our Threads, i.e. we wait for them to finish before continuing
    det_rec_process.join()
    ev_rec_process.join()
    det_send_process.join()
    ev_send_process.join()


if __name__ == "__main__":

    main()
