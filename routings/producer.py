import pika

from pika.exchange_type import ExchangeType

conn_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.exchange_declare(exchange='topic_exchange', exchange_type=ExchangeType.topic)

all_message = 'A message for both analytics and user consumers.'

channel.basic_publish(exchange='topic_exchange', routing_key='user.europe.payments', body=all_message)

print(f" [x] Sent '{all_message}'")

analytics_only_message = 'A message for analytics consumers only.'

channel.basic_publish(exchange='topic_exchange', routing_key='analytics.europe.data', body=analytics_only_message)

print(f" [x] Sent '{analytics_only_message}'")

connection.close()