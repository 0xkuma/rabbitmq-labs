# Server

import pika


def on_request(ch, method, props, body):
    # Process the request...
    print("Received request:", props, body)

    response = "Response to " + str(body)  # Generate the response

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=response
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='RequestQueue')
channel.basic_consume(queue='RequestQueue', on_message_callback=on_request)

print("Awaiting requests")
channel.start_consuming()
