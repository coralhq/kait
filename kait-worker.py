#!/usr/bin/env python3
from sys import argv
from kait import worker
from imp import load_source

if __name__ == '__main__':
    source_name = argv[1]
    handler_file = argv[2]

    callback = load_source("", handler_file).handle
    worker.run(source_name, callback)
