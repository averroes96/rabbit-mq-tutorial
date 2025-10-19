import pika

def callback(ch, method, properties, body):
    print(f" [x] Second Consumer Received {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()
channel.exchange_declare(exchange='pubsub', exchange_type='fanout')
queue = channel.queue_declare(queue='', exclusive=True)

queue_name = queue.method.queue
channel.queue_bind(exchange='pubsub', queue=queue_name)

print(' [*] Second Consumer Waiting for messages. To exit press CTRL+C')

channel.basic_consume(queue=queue_name, on_message_callback=callback)

channel.start_consuming()
