import pika

def request_callback(channel, method, properties, body):
    print(f' [*] Received message: {body}')
    print(f' [*] Properties: {properties}')
    channel.basic_publish('', routing_key=properties.reply_to, body=f' [*] Hey, this is your reply to corelation: {properties.correlation_id}')
    channel.basic_ack(delivery_tag=method.delivery_tag)


connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='request-queue')
channel.basic_consume(queue='request-queue', on_message_callback=request_callback)

print(' [*] Starting Server...')

channel.start_consuming()