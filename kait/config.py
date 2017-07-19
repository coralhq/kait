from os import environ
from dotenv import load_dotenv, find_dotenv

def autoload():
    load_dotenv(find_dotenv())
    globals()['token'] = environ.get("KAIT_MASTER_TOKEN", None)
    globals()['debug'] = bool(int(environ.get("KAIT_MASTER_DEBUG", 1)))
    globals()['amqp_url'] = environ.get("KAIT_AMQP_URL", "tcp://localhost:5672")
    globals()['amqp_exchange'] = environ.get("KAIT_AMQP_EXCHANGE", "kait")

autoload()
