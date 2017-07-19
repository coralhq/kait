import sh
import os
import sys
from kait.worker import JobErrorException, JobFailedException

def _flatten(d):
    def expand(key, value):
        if isinstance(value, dict):
            return [ (key + '_' + k, v) for k, v in _flatten(value).items() ]
        else:
            return [ (key, value) ]
    items = [ item for k, v in d.items() for item in expand(k, v) ]
    return dict(items)

def _make_envs(payload):
    tmp = _flatten(payload)
    result = dict()
    for key in tmp:
        val = tmp[key]
        if not isinstance(val, list):
            result[key] = str(val)
    return result

def _valid_script(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

class Script(object):
    def __init__(self, script):
        super(Script, self).__init__()
        self.script = script

    def handle(self, payload):
        env = os.environ.copy()
        env.update(_make_envs(payload))

        if not _valid_script(self.script):
            raise JobErrorException("script is not executable: "+self.script)

        try:
            print()
            print("running: "+self.script)
            print("---")
            cmd = sh.Command(self.script)
            cmd(_out=sys.stdout, _env=env)
        except Exception as e:
            raise JobFailedException(e)
        finally:
            print("---")

def create(script, *args, **kwargs):
    return Script(script)
