import pika

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

def main_callback(channel, method, property, body):
    if method.delivery_tag % 5 == 0:
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False, multiple=True)
    
    print(f'[x] Main Received Message: {body.decode()}')

channel = connection.channel()

channel.exchange_declare('accept-reject-exchange', exchange_type='fanout')
channel.queue_declare('accept-reject-queue')

channel.queue_bind(queue='accept-reject-queue', exchange='accept-reject-exchange')

channel.basic_consume(queue='accept-reject-queue', on_message_callback=main_callback)

print('[x] Start consuming...')

channel.start_consuming()