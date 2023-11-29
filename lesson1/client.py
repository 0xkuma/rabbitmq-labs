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
channel.queue_declare(queue=config[environment]['queue'])


# Send a message to the queue
for i in range(1000):
    message = ' '.join(sys.argv[1:]) or f"info: Hello World!! {i}"
    channel.basic_publish(
        exchange='',
        routing_key=config[environment]['queue'],
        body=message,
    )
    print(f" [x] Sent 'Hello World! {i}'")

# Close the connection
connection.close()
