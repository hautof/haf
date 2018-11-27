# encoding='utf-8'

from flask_restful import Resource

from haf.busclient import BusClient
from haf import globalenv

globalenv._init()
globalenv.set_global("runners", {})

class ResultResource(Resource):
    def __init__(self):
        super().__init__()

    def get(self):

        pass


class RunnerResource(Resource):
    def __init__(self):
        super().__init__()
        self.bus_client = BusClient()

    def get(self):
        get_queue = self.bus_client.get_publish_runner()
        runners = globalenv.get_global("runners")
        if not get_queue.empty():
            runner = get_queue.get()
            runners[runner.get("key")] = runner
            globalenv.set_global("runners", runners)
        return globalenv.get_global("runners")


class LoaderResource(Resource):
    def __init__(self):
        super().__init__()
        self.bus_client = BusClient()

    def get(self):
        get_queue = self.bus_client.get_publish_loader()

        if not get_queue.empty():
            loader = get_queue.get()
            globalenv.set_global("loader", loader)
        return globalenv.get_global("loader")