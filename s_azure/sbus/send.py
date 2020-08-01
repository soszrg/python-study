import time

from azure.servicebus import Message, ServiceBusClient

from s_azure.sbus.config import connection_str, queue_name
connection_str = "Endpoint=sb://sbus-will-test.servicebus.windows.net/;SharedAccessKeyName=sending;SharedAccessKey=G2RAJ3NCB+K934MTbO5y8b4BfAtH5pydinzG6KbafoQ="
sb_client = ServiceBusClient.from_connection_string(connection_str)
queue_client = sb_client.get_queue(queue_name)
message = Message("Hello World")
queue_client.send(message)
count = 0
while True:
    new_message = Message(f"id[{count}]")
    queue_client.send([new_message])
    print(f"Send msg:{new_message}")
    count += 1
    time.sleep(3)
