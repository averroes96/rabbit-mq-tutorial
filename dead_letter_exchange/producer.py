import pika

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()
channel.exchange_declare('main-exchange', exchange_type='direct')

message = 'Hello, this message will go to the dead letter exchange'

channel.basic_publish(exchange='main-exchange', routing_key='test', body=message)

print(f'[*] Sent Message: {message}')

connection.close()