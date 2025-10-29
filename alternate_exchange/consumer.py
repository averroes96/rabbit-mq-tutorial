import pika

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

def alt_callback(channel, method, property, body):
    print(f'[x] Alt Received Message: {body.decode()}')

def main_callback(channel, method, property, body):
    print(f'[x] Main Received Message: {body.decode()}')

channel = connection.channel()

channel.queue_declare('main-exchange-queue')
channel.queue_declare('alt-exchange-queue')

channel.exchange_declare('main', exchange_type='direct', arguments={'alternate-exchange': 'alt'})
channel.exchange_declare('alt', exchange_type='fanout')

channel.queue_bind(queue='main-exchange-queue', exchange='main', routing_key='test')
channel.queue_bind(queue='alt-exchange-queue', exchange='alt')

channel.basic_consume(queue='main-exchange-queue', auto_ack=True, on_message_callback=main_callback)
channel.basic_consume(queue='alt-exchange-queue', auto_ack=True, on_message_callback=alt_callback)

print('[x] Start consuming...')

channel.start_consuming()