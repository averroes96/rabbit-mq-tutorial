import pika

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

def dead_letter_callback(channel, method, property, body):
    print(f'[x] Dead Letter Received Message: {body.decode()}')

def main_callback(channel, method, property, body):
    print(f'[x] Main Received Message: {body.decode()}')

channel = connection.channel()

channel.exchange_declare('main-exchange', exchange_type='direct')
channel.exchange_declare('dead-letter-exchange', exchange_type='fanout')

channel.queue_declare('main-queue', arguments={
    'x-dead-letter-exchange': 'dead-letter-exchange',
    'x-message-ttl': 1000
})
channel.queue_declare('dead-letter-queue')

channel.queue_bind(queue='main-queue', exchange='main-exchange', routing_key='test')
channel.queue_bind(queue='dead-letter-queue', exchange='dead-letter-exchange')

channel.basic_consume(queue='main-queue', auto_ack=True, on_message_callback=main_callback)
channel.basic_consume(queue='dead-letter-queue', auto_ack=True, on_message_callback=dead_letter_callback)

print('[x] Start consuming...')

channel.start_consuming()