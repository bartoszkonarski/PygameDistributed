import pika

class RabbitProducer:
    def __init__(self, name) -> None:
        connection_parameters = pika.ConnectionParameters('localhost')
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=name)

    def produce_message(self, message):
        self.channel.basic_publish(exchange='', routing_key='testin', body=message)
