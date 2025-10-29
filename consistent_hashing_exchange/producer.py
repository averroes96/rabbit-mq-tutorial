import pika

from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.queue_declare('letterbox')
channel.exchange_declare(exchange='hashing-exchange', exchange_type='x-consistent-hash')

message = 'Hello, Hash Me!'
routing_key = 'HashMelolololol123tozwhatever'

channel.basic_publish(
    exchange='hashing-exchange', 
    routing_key=routing_key, 
    body=message,
)

print(f" [x] Sent '{message}'")

connection.close()