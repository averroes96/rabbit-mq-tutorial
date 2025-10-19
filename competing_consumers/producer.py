import pika
import time
import random

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()
channel.queue_declare(queue='letterbox', durable=True)

message_sent = 1

while True:
    message = f"Hello, This is a message! {message_sent}"
    channel.basic_publish(
        exchange='',
        routing_key='letterbox',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )

    print(f" [x] Sent '{message}'")

    time_to_sleep = random.randint(1, 4)
    time.sleep(time_to_sleep)

    message_sent += 1