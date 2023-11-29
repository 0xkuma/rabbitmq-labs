import pika
import sys
import configparser
import os
import uuid

config = configparser.ConfigParser()
config.read('server.conf')

environment = os.environ.get('ENVIRONMENT', 'default')


class FibonacciRpcClient(object):
    def __init__(self):
        self.credentials = pika.PlainCredentials(
            config[environment]['username'], config[environment]['password'])
        self.parameters = pika.ConnectionParameters(
            config[environment]['servers'],
            int(config[environment]['port']),
            config[environment]['vhost'],
            self.credentials
        )
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='rpc',
            routing_key='',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=str(n)
        )
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fib_rpc = FibonacciRpcClient()

for i in range(1, 10):
    print(f" [x] Requesting fib({i})")
    response = fib_rpc.call(i)
    print(f" [.] Got {response}")
