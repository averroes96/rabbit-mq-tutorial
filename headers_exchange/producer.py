import pika

from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.queue_declare('letterbox')
channel.exchange_declare(exchange='headers-exchange', exchange_type=ExchangeType.headers)

message = 'Hello, this message will be sent with headers..'

channel.basic_publish(
    exchange='headers-exchange', 
    routing_key='', 
    body=message,
    properties=pika.BasicProperties(
        headers={
            'name': 'brian'
        }
    )
)

print(f" [x] Sent '{message}'")

connection.close()