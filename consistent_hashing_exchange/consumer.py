import pika

from pika.exchange_type import ExchangeType

def first_callback(channel, method, properties, body):
    print(f" [x] Received in hashing-queue-1: {body.decode()}")
    channel.basic_ack(delivery_tag=method.delivery_tag)

def second_callback(channel, method, properties, body):
    print(f" [x] Received in hashing-queue-2: {body.decode()}")
    channel.basic_ack(delivery_tag=method.delivery_tag)

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.queue_declare(queue='hashing-queue-1')
channel.queue_declare(queue='hashing-queue-2')
channel.exchange_declare(exchange='hashing-exchange', exchange_type='x-consistent-hash')

channel.queue_bind(queue='hashing-queue-1', exchange='hashing-exchange', routing_key='1')
channel.queue_bind(queue='hashing-queue-2', exchange='hashing-exchange', routing_key='4')

channel.basic_consume(queue='hashing-queue-1', on_message_callback=first_callback)
channel.basic_consume(queue='hashing-queue-2', on_message_callback=second_callback)

print(' [*] Start consuming...')

channel.start_consuming()