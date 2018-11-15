import time
from queue import Queue

from haf.bus import BusServer
from haf.busclient import BusClient
from haf.message import MessageDict, InfoManager

if __name__ == "__main__":
    bus_manager = BusServer()
    bus_manager.start()
    bus_client = BusClient()
    print("here start")
    i = 0
    while True:
        i+=1
        bus_client.get_queue()
        bus_client.queue.put("queue{}".format(i))
        time.sleep(0.1)
        print(bus_client.queue.get())
        time.sleep(0.3)
