import pika

from pika.exchange_type import ExchangeType

conn_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

message = 'Hello, I want to broadcast to all consumers!'

channel.basic_publish(exchange='pubsub', routing_key='', body=message)

print(f" [x] Sent '{message}'")

connection.close()