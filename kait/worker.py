from kait import config
from kait.broker import RabbitMQ
from sys import argv
from simplejson import loads

class JobErrorException(Exception):
    pass

class JobFailedException(Exception):
    pass

def run(source_name, callback):
    print("subscribing to " + source_name)

    def cb(channel, method, properties, body):
        payload = loads(body)
        try:
            callback(payload)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print("ERROR: "+str(e))
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    config.autoload()

    broker = RabbitMQ(config.amqp_url, config.amqp_exchange)
    broker.connect()
    broker.subscribe(source_name, cb)
    broker.disconnect()
