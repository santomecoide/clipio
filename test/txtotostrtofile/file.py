from clipio.coap_server.resources.iot_resource import IotResource

class Algo(IotResource):
    def __init__(self, type): 
        super().__init__("algo", "algo")