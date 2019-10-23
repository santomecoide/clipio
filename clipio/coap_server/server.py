from coapthon.server.coap import CoAP

from clipio.coap_server.resources.metadata import Metadata
from clipio.coap_server.resources.eca import Eca
from clipio.coap_server.resources.context import Context

class Server(CoAP):
    def __init__(self, host, port=5683):
        CoAP.__init__(self, (host, port), False)
        self.add_resource('metadata', Metadata())
        self.add_resource('eca', Eca())
        self.add_resource('context', Context())

    def __add_iot_resources(self, resources):
        for obj, name in resources:
            self.add_resource(
                name, 
                obj
            )
            
    def run(self, resources):
        self.__add_iot_resources(resources)
        self.listen()

    def stop(self):
        self.close()