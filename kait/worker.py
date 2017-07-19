from kait import config
from kait.broker import RabbitMQ
from sys import argv
from simplejson import loads

def run(plugin_name, callback):
    print("subscribing to " + plugin_name)

    def cb(channel, method, properties, body):
        callback(loads(body))
        channel.basic_ack(delivery_tag=method.delivery_tag)

    config.autoload()

    broker = RabbitMQ(config.amqp_url, config.amqp_exchange)
    broker.connect()
    broker.subscribe(plugin_name, cb)
    broker.disconnect()
