import urllib
import gzip

import numpy as np
from platypus_fizzy.config import dae_config


# grab DAE server setup from config
ip = dae_config["ip"]
port = dae_config["port"]
auth_user = dae_config["user"]
auth_password = dae_config["password"]


# register for basic authentication
uri = f"http://{ip}:{port}/admin"
passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, uri, auth_user, auth_password)
authhandler = urllib.request.HTTPBasicAuthHandler(passman)
opener = urllib.request.build_opener(authhandler)
urllib.request.install_opener(opener)


HISTOGRAM_VIEWS = {
    "TOTAL_HISTOGRAM_XYT": ["OAT_NXC", "OAT_NYC", "OAT_NTC"],
    "TOTAL_HISTOGRAM_XY": ["OAT_NXC", "OAT_NYC"],
    "TOTAL_HISTOGRAM_XT": ["OAT_NXC", "OAT_NTC"],
    "TOTAL_HISTOGRAM_YT": ["OAT_NYC", "OAT_NTC"],
    "TOTAL_HISTOGRAM_T": ["OAT_NTC"],
    "TOTAL_HISTOGRAM_X": ["OAT_NXC"],
    "TOTAL_HISTOGRAM_Y": ["OAT_NYC"],
}


def detector_image(view="TOTAL_HISTOGRAM_YT"):
    """
    Get the current detector image

    Parameters
    ----------
    view : str
        One of:
            - 'TOTAL_HISTOGRAM_XYT'
            - 'TOTAL_HISTOGRAM_XY'
            - 'TOTAL_HISTOGRAM_XT'
            - 'TOTAL_HISTOGRAM_YT'
            - 'TOTAL_HISTOGRAM_T'
            - 'TOTAL_HISTOGRAM_X'
            - 'TOTAL_HISTOGRAM_Y'

    Returns
    -------
    hmm : np.ndarray
        detector image
    """
    if view not in HISTOGRAM_VIEWS:
        raise ValueError(
            f"view should be one of " f"{list(HISTOGRAM_VIEWS.keys())}"
        )

    stat = status()
    axes = HISTOGRAM_VIEWS[view]
    shape = [int(stat[axis]) for axis in axes]

    request = (
        f"http://{ip}:{port}/admin/savedataview.egi?"
        f"data_saveopen_format=ZIPBIN&data_saveopen_action=OPENONLY&"
        f"type={view}"
    )
    with urllib.request.urlopen(request) as result:
        compressed_image = result.read()

    buf = gzip.decompress(compressed_image)
    hmm = np.frombuffer(buf, dtype=np.int32)
    return np.reshape(hmm, shape)


def status():
    """
    Find the status of the histogram server from the textstatus.egi page
    Returns
    -------
    d : dict
        Information on the histogram status

    """
    request = urllib.request.Request(
        f"http://{ip}:{port}/admin/textstatus.egi"
    )

    d = {}
    with urllib.request.urlopen(request) as result:
        for line in result:
            text = line.decode("utf-8")
            text = text.rstrip("\n")
            key, val = text.split(": ")
            d[key] = val

    return d


def acquisition_status():
    """
    Whether the histogram server is currently acquiring

    Returns
    -------
    status : int
       -3 - undetermined
       -2 - paused
       -1 - starting
        0 - stopped
        1 - acquiring
    """
    stat = status()["DAQ"]

    if stat == "Stopped":
        return 0
    elif stat == "Started":
        return 1
    elif stat == "Paused":
        return -2
    elif stat == "Starting":
        return -1
    else:
        return -3
