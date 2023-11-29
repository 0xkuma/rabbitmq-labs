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
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# Send a message to the queue
for i in range(1):
    routing_key = sys.argv[1] if len(sys.argv) > 2 else '#'
    message = ' '.join(sys.argv[2:]) or f"Hello World!! {i}"
    channel.basic_publish(
        exchange='topic_logs',
        routing_key=routing_key,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.TRANSIENT_DELIVERY_MODE
        )
    )
    print(f" [x] Sent {routing_key}:{message}")


# Close the connection
connection.close()
