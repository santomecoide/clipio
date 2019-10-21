from coapthon.server.coap import CoAP

from clipio.coap_resources.metadata import Metadata
from clipio.coap_resources.eca import Eca
from clipio.coap_resources.context import Context

class Server(CoAP):
    def __init__(self, host, port=5683):
        CoAP.__init__(self, (host, port), False)
        self.add_resource("metadata", Metadata())
        self.add_resource("eca", Eca())
        self.add_resource("context", Context())

    """ def __add_iot_resources(self, iot_resources=[]):
        for iot_resource in iot_resources:
            self.add_resource(
                iot_resource, 
                IotResource(iot_resource)
            ) """
            
    def run(self):
        #self.__add_iot_resources()
        self.listen()

    def stop(self):
        self.close()