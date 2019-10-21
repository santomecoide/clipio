from coapthon.server.coap import CoAP

from server.resources.metadata import Metadata
from server.resources.eca import Eca
from server.resources.context import Context

class Server(CoAP):
    def __init__(self, host, port=5683):
        CoAP.__init__(self, (host, port), False)
        self.add_resource('metadata', Metadata())
        self.add_resource('eca', Eca())
        self.add_resource('context', Context())

    def __add_iot_resources(self, iot_list=[]):
        for iot_class, iot_resource in iot_list:
            self.add_resource(
                iot_resource, 
                iot_class
            )
            
    def run(self):
        self.__add_iot_resources()
        self.listen()

    def stop(self):
        self.close()