#!/usr/bin/env python
from flask import Flask, request, make_response
from kait import config
from kait.broker import RabbitMQ
from simplejson import dumps

app = Flask(__name__)
config.autoload()
broker = RabbitMQ(config.amqp_url, config.amqp_exchange)

@app.route(u'/hooks/<source_name>', methods=['POST'])
def hooks(source_name):
    if config.token and config.token != request.args.get('token'):
        return make_response(u"invalid token", 400)

    try:
        source = __import__(u"kait.sources."+source_name, fromlist=[''])
    except ImportError as e:
        return make_response(u"source not found: "+source_name, 404)

    payload = source.create_payload(request.data)
    payload[u"_source_name"] = source_name
    group = payload[u"_group"]

    try:
        body = dumps(payload)
        print(u"%s.%s: %s" % (source_name, group, body))
        broker.publish(source_name, group, body)
        return u"OK"
    except Exception as e:
        return str(e)

def run():
    broker.connect()
    app.run(host='0.0.0.0', port=8080, debug=config.debug)
    broker.disconnect()
