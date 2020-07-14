import urllib
import base64
from platypus_fizzy.config import dae_config


def status():
    ip = dae_config['ip']
    port = dae_config['port']
    user = dae_config['user']
    password = dae_config['password']

    request = urllib.request.Request(f"http://{ip}:{port}/admin/textstatus.egi")
    base64string = base64.b64encode(bytes(f"{user}:{password}"), "ascii")
    request.add_header("Authorization", f"Basic {base64string.decode('utf-8')}")
    with urllib.request.urlopen(request) as result:
        text = result.read().decode(encoding='utf-8')

    return text
