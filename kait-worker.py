#!/usr/bin/env python3
from sys import argv
from kait import worker
# from imp import load_source

def load_module(name):
    return __import__(name, fromlist=[''])

if __name__ == '__main__':
    source_name = argv[1]
    handler_name = argv[2]
    handler_args = argv[3:]

    handler_module = load_module("kait.handlers."+handler_name)
    handler = handler_module.create(*handler_args)
    worker.run(source_name, handler.handle)
