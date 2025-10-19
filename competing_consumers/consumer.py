import pika
import time
import random

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
channel.queue_declare(queue='letterbox', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    processing_time = random.randint(1, 6)
    print(f" [x] Received {body.decode()}")
    time.sleep(processing_time)
    print(f" [x] Done processing {body.decode()} in {processing_time} seconds")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='letterbox', on_message_callback=callback)

channel.start_consuming()

