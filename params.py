"""
This file sets parameters used in data dump OpenEEW algorithm
"""

# MQTT
MQTT = "local"  # local or IBM

# PARAMETERS
region = "MX"
event_table_name = "events-test"
detection_table_name = "detections-test"
sleep_time_save = 2

# TEST DATA PATH
test_data_path = "../data/"


params = {
    "region": region,
    "event_table_name": event_table_name,
    "detection_table_name": detection_table_name,
    "sleep_time_save": sleep_time_save,
    "MQTT": MQTT,
    "test_data_path": test_data_path,
}
