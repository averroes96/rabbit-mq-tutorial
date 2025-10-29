import pika

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()
channel.exchange_declare('main', exchange_type='direct', arguments={'alternate-exchange': 'alt'})
channel.exchange_declare('alt', exchange_type='fanout')

message = 'Hello, this message!'

channel.basic_publish(exchange='main', routing_key='simple', body=message)

channel.start_consuming()

print(f'[*] Sent Message: {message}')

connection.close()