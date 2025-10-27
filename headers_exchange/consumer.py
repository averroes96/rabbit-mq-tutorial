import pika

from pika.exchange_type import ExchangeType

def callback(channel, method, properties, body):
    print(f" [x] Received {body.decode()}")
    channel.basic_ack(delivery_tag=method.delivery_tag)

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.queue_declare(queue='letterbox')
channel.exchange_declare(exchange='headers-exchange', exchange_type=ExchangeType.headers)

bind_args = {
    'x-match': 'all',
    'name': 'brian',
    'age': '53'
}
channel.queue_bind(queue='letterbox', exchange='headers-exchange', arguments=bind_args)

channel.basic_consume(queue='letterbox', on_message_callback=callback)

print(' [*] Start consuming...')

channel.start_consuming()