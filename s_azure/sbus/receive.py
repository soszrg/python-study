import time
from azure.servicebus import QueueClient
from s_azure.sbus.config import connection_str, queue_name

# Create the QueueClient
connection_str = "Endpoint=sb://sbus-will-test.servicebus.windows.net/;SharedAccessKeyName=funcs-using;SharedAccessKey=eA+0Ok4GGpJ7gV9nBqMY02y+NE7ztBqCEHWE7H3/O/s="
queue_client = QueueClient.from_connection_string(connection_str, queue_name)

while True:
    # Receive the message from the queue
    with queue_client.get_receiver() as queue_receiver:
        print("Wait for new msg...")
        messages = queue_receiver.fetch_next(timeout=3)
        for message in messages:
            print(message)
            message.complete()
