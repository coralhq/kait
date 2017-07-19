#!/usr/bin/env python
from flask import Flask, request, make_response
from kait import config
from kait.broker import RabbitMQ
from simplejson import dumps

app = Flask(__name__)
config.autoload()
broker = RabbitMQ(config.amqp_url, config.amqp_exchange)

@app.route(u'/hooks/<plugin_name>')
def hooks(plugin_name):
    try:
        plugin = __import__(u"kait.plugins."+plugin_name, fromlist=[''])
    except ImportError as e:
        return make_response(u"Plugin not found: "+plugin_name, 404)

    payload = plugin.create_payload(request.data)
    payload[u"_plugin_name"] = plugin_name
    group = payload[u"_group"]

    try:
        print(u"publishing to: %s.%s" % (plugin_name, group))
        broker.publish(plugin_name, group, dumps(payload))
        return u"OK"
    except Exception as e:
        return str(e)

def run():
    broker.connect()
    app.run(host='0.0.0.0', port=8080, debug=config.debug)
    broker.disconnect()
