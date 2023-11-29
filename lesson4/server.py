import pika
import sys
import configparser

config = configparser.ConfigParser()
config.read('server.conf')

environment = 'default'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(config[environment]['servers']))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue


def callback(ch, method, prop, body):
    print(f" [x] {method.routing_key}:{body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


severities = sys.argv[1:]
if not severities:
    print(f"Usage: {sys.argv[0]} [info] [warning] [error]")
    sys.exit(1)

for severity in severities:
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=severity)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback
)
channel.start_consuming()
