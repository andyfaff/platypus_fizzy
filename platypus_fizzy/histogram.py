import urllib
import base64
from platypus_fizzy.config import dae_config


# grab DAE server setup from config
ip = dae_config['ip']
port = dae_config['port']
auth_user = dae_config['user']
auth_password = dae_config['password']


# register for basic authentication
uri = f"http://{ip}:{port}/admin"
passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, uri, auth_user, auth_password)
authhandler = urllib.request.HTTPBasicAuthHandler(passman)
opener = urllib.request.build_opener(authhandler)
urllib.request.install_opener(opener)


def status():
    """
    Find the status of the histogram server from the textstatus.egi page
    Returns
    -------
    d : dict
        Information on the histogram status

    """
    ip = dae_config['ip']
    port = dae_config['port']
    user = dae_config['user']
    password = dae_config['password']

    request = urllib.request.Request(f"http://{ip}:{port}/admin/textstatus.egi")

    d = {}
    with urllib.request.urlopen(request) as result:
        for line in result:
            text = line.decode("utf-8")
            text = text.rstrip("\n")
            key, val = text.split(": ")
            d[key] = val

    return d
