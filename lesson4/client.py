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
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Send a message to the queue
for i in range(10):
    severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    message = ' '.join(sys.argv[2:]) or f"info: Hello World!! {i}"
    channel.basic_publish(
        exchange='direct_logs',
        routing_key=severity,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.TRANSIENT_DELIVERY_MODE
        )
    )
    print(f" [x] Sent {severity}:{message}")


# Close the connection
connection.close()
