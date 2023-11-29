import pika
import sys
import configparser
import os

config = configparser.ConfigParser()
config.read('server.conf')

environment = os.environ.get('ENVIRONMENT', 'default')

# Establish a connection with RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(config[environment]['servers']))
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Send a message to the queue
for i in range(100):
    message = ' '.join(sys.argv[1:]) or f"info: Hello World!! {i}"
    channel.basic_publish(
        exchange='logs',
        routing_key='',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.TRANSIENT_DELIVERY_MODE
        )
    )
    print(f" [x] Sent 'Hello World! {i}'")

# Close the connection
connection.close()
