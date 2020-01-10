import datetime
import logging
from azure.eventhub import EventHubClient, EventData, EventPosition

# connection_str = 'Endpoint=sb://iothub-ns-lucashub-1020983-ca4c475408.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=5VOskHYDkto2sZEmgVTCMR3NhieVdsVd1URgUOLhGn4=;EntityPath=lucashub'
# event_hub_path = 'lucashub'
# client = EventHubClient.from_connection_string(connection_str, **{'event_hub_path': event_hub_path})
# consumer = client.create_consumer(consumer_group="$default", partition_id="0", event_position=EventPosition("-1"))
#
# try:
#     print("azure.eventhub")
#     with consumer:
#         received = consumer.receive(max_batch_size=100, timeout=5)
#         for event_data in received:
#             print("Message received:{}".format(event_data))
# except Exception as e:
#     raise
# finally:
#     pass

import time
from azure.eventhub import EventHubClient, EventPosition, EventHubSharedKeyCredential

HOSTNAME = 'ihsuprodhkres004dednamespace.servicebus.windows.net'  # <mynamespace>.servicebus.windows.net
EVENT_HUB = 'iothub-ehub-stm-2395944-9fd6b762ca'

USER = 'iothubowner'
KEY = '0wFJrgMqCIqIJOUBZ9tDKUxf0BSW+9TL4SvpTF/JsHQ='

EVENT_POSITION = EventPosition("-1")
PARTITION = "0"


# total = 0
last_sn = -1
last_offset = "-1"
client = EventHubClient(host=HOSTNAME, event_hub_path=EVENT_HUB, credential=EventHubSharedKeyCredential(USER, KEY),
                        network_tracing=False)

consumer = client.create_consumer(consumer_group="$default", partition_id=PARTITION,
                                  event_position=EVENT_POSITION, prefetch=5000)
with consumer:
    while True:
        total = 0
        start_time = time.time()
        batch = consumer.receive(timeout=5)
        while batch:
            for event_data in batch:
                last_offset = event_data.offset
                last_sn = event_data.sequence_number
                print("Received: {}, {}".format(last_offset, last_sn))
                print(event_data.body_as_str())
                total += 1
            batch = consumer.receive(timeout=5)
        print("[{}]Received {} messages in {} seconds".format(datetime.datetime.now(), total, time.time() - start_time))
