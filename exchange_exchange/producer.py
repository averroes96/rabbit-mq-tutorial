import pika

from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.queue_declare('letterbox')
channel.exchange_declare(exchange='first-exchange', exchange_type=ExchangeType.direct)
channel.exchange_declare(exchange='second-exchange', exchange_type=ExchangeType.fanout)
channel.exchange_bind(destination='second-exchange', source='first-exchange')

message = 'Hello, this message has gone through multiple exchanges'

channel.basic_publish(exchange='first-exchange', routing_key='', body=message)

print(f" [x] Sent '{message}'")

connection.close()