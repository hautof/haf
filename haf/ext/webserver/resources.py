# encoding='utf-8'
from flask_restful import Resource
from haf.busclient import BusClient
from haf import globalenv
from haf.result import EndResult

globalenv._init()
globalenv.set_global("runners", {})
globalenv.set_global("results", EndResult())


class ResultResource(Resource):
    def __init__(self):
        super().__init__()
        self.bus_client = BusClient()

    def get(self):
        get_queue = self.bus_client.get_publish_result()
        results = globalenv.get_global("results")
        if not get_queue.empty():
            results = get_queue.get()
            globalenv.set_global("results", results)

        return results.deserialize()


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


