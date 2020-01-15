import zmq
import simplejson as json
import time
import numpy as np
from qchart.config import config
from qchart.clients.utils import NumpyJSONEncoder


class DataSender(object):
    def __init__(self, dataId):
        self.data = {"id": dataId, "datasets": {}}

    def send_data(self, timeout=None):

        jsData = json.dumps(self.data, allow_nan=True, cls=NumpyJSONEncoder)
        encData = jsData.encode(encoding="UTF-8")

        addr = config["network"]["addr"]
        port = config["network"]["port"]
        srvr = f"tcp://{addr}:{port}"

        if timeout is None:
            timeout = config["client"]["send_timeout"]

        context = zmq.Context()
        context.setsockopt(zmq.LINGER, timeout)
        socket = context.socket(zmq.PUSH)
        socket.connect(srvr)

        t0 = time.time()
        socket.send(encData)
        socket.close()
        context.term()

        if (time.time() - t0) > (timeout / 1000.0):
            print("Timeout during sending!")
