import pika
import sys
import configparser

config = configparser.ConfigParser()
config.read('server.conf')

environment = 'default'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(config[environment]['servers']))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue


def callback(ch, method, prop, body):
    print(f" [x] {method.routing_key}:{body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback
)
channel.start_consuming()
