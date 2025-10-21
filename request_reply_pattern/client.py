import pika
import uuid

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()


def reply_callback(channel, method, properties, body):
    print(f' [*] Received reply: {body}')
    channel.basic_ack(delivery_tag=method.delivery_tag)

reply_queue = channel.queue_declare(queue='', exclusive=True)
request_queue = channel.queue_declare(queue='request-queue')

channel.basic_consume(queue=reply_queue.method.queue, on_message_callback=reply_callback)

message = 'Hello, I\'m requesting a reply!'
cor_id = str(uuid.uuid4())

channel.basic_publish(
    exchange='', 
    routing_key='request-queue', 
    body=message, 
    properties=pika.BasicProperties(reply_to=reply_queue.method.queue, correlation_id=cor_id)
)

print(f' [x] Sent Message: {message} with corelation id: {cor_id}')

channel.start_consuming()