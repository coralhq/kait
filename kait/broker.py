import pika

class RabbitMQ(object):

    def __init__(self, url, exchange):
        super(RabbitMQ, self).__init__()
        self.url = url
        self.exchange = exchange

    def connect(self):
        params = pika.URLParameters(self.url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, type='topic', durable=True)

    def publish(self, source_name, group, body):
        routing_key = u"%s.%s" % (source_name, group)
        self.channel.queue_declare(queue=source_name, durable=True)
        self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=body)

    def subscribe(self, source_name, callback):
        self.channel.queue_declare(queue=source_name, durable=True)
        self.channel.queue_bind(exchange=self.exchange,
                       queue=source_name,
                       routing_key=source_name+'.#')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(callback, queue=source_name)
        self.channel.start_consuming()

    def disconnect(self):
        if self.connection:
            self.connection.close()
