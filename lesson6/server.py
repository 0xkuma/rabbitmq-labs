import pika
import sys
import configparser
import time

config = configparser.ConfigParser()
config.read('server.conf')

environment = 'default'

credentials = pika.PlainCredentials(
    config[environment]['username'], config[environment]['password'])
parameters = pika.ConnectionParameters(
    config[environment]['servers'],
    int(config[environment]['port']),
    config[environment]['vhost'],
    credentials
)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='rpc', exchange_type='direct', durable=True)

# result = channel.queue_declare(queue='', exclusive=True, durable=True)
queue_name = 'rpc'

channel.queue_bind(
    exchange='rpc',
    queue=queue_name,
    routing_key=''
)


def on_request(ch, method, props, body):
    n = int(body)
    print(f" [.] fib({n})")
    response = fib(n)
    print({
        "exchange": "",
        "routing_key": props.reply_to,
        "properties": {
            "correlation_id": props.correlation_id
        },
        "body": str(response)
    })
    time.sleep(3)
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=str(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-2) + fib(n-1)


channel.basic_consume(
    queue=queue_name,
    on_message_callback=on_request
)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
