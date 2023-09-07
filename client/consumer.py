import pika

class RabbitConsumer:
    def __init__(self, name) -> None:
        connection_parameters = pika.ConnectionParameters('localhost')
        self.response = None

        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()
        for method_frame, properties, body in self.channel.consume(name):
            self.response = body

            # Acknowledge the message
            self.channel.basic_ack(method_frame.delivery_tag)

            # Escape out of the loop after 10 messages
            if method_frame.delivery_tag == 1:
                break

            # Cancel the consumer and return any pending messages
            self.channel.close()
            self.connection.close()