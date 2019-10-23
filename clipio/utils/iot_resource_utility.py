class IoTResourceUtility:
    def __init__(self, metadata):
        self.__metadata = metadata

    def __generate_resource(self, resource):
        pass

        """ from clipio.coap_server.resources.iot_resource import IotResource

            class Temperature(IotResource):
                def __init__(self, type): 
                    super().__init__("temperature", "number") """

    def generate_resources(self):
        for resource in self.__metadata['resources']: 
            self.__generate_resource(resource)
            