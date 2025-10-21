import pika

from pika.exchange_type import ExchangeType

def callback(ch, method, properties, body):
    print(f" [x] User Consumer Received {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

conn_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.exchange_declare(exchange='topic_exchange', exchange_type=ExchangeType.topic)

queue = channel.queue_declare(queue='', exclusive=True)

channel.queue_bind(exchange='topic_exchange', queue=queue.method.queue, routing_key='user.#')
channel.basic_consume(queue=queue.method.queue, on_message_callback=callback)

print(' [*] User Consumer Waiting for messages. To exit press CTRL+C')

channel.start_consuming()