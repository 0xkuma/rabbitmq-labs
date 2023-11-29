import pika
import configparser

config = configparser.ConfigParser()
config.read('server.conf')

environment = 'default'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(config[environment]['servers']))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=config[environment]['queue'],
    on_message_callback=callback
)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
