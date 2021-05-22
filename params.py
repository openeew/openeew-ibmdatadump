"""
This file sets parameters used in data dump OpenEEW algorithm
"""

# MQTT
MQTT = "IBM"  # local, custom, or IBM

# PARAMETERS
region = "OE"
event_table_name = "openeew-events"
detection_table_name = "openeew-detections"
sleep_time_save = 10
max_pause = 10  # save event if there are no entries for this time

# TEST DATA PATH
test_data_path = "../data/"


params = {
    "region": region,
    "event_table_name": event_table_name,
    "detection_table_name": detection_table_name,
    "sleep_time_save": sleep_time_save,
    "MQTT": MQTT,
    "test_data_path": test_data_path,
    "max_pause": max_pause,
}
