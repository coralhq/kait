from simplejson import loads

PLUGIN_NAME = "dockerhub"

def create_payload(raw_data, content_type="application/json"):
    data = loads(raw_data)

    repo_name = data["repository"]["repo_name"]
    tag = data["push_data"]["tag"]
    timestamp = data["push_data"]["pushed_at"]
    image = "{repo_name}:{tag}".format(**locals())

    group = repo_name.replace('/', '.')

    return {
        "_raw": data,
        "_group": group,
        "repo_name": repo_name,
        "tag": tag,
        "image": image,
        "timestamp": timestamp
    }
