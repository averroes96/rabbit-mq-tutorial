import pika

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()
channel.exchange_declare('accept-reject-exchange', exchange_type='fanout')

message = 'Hello, this message will go to the dead letter exchange'

while True:
    channel.basic_publish(exchange='accept-reject-exchange', routing_key='test', body=message)

    print(f'[*] Sent Message: {message}')

    input("Press Enter to send another message...")