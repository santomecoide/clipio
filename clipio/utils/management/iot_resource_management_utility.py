import os
from clipio.utils.seed import iot_resource_seed

class IoTResourceManagementUtility:
    def __init__(self, settings):
        self.__metadata = settings.METADATA

    def __generate_resource(self, resource):
        format_data = iot_resource_seed.format(
            resource['tag'].capitalize(), 
            resource['tag'], 
            resource['type']
        )

        iot_resource_file = open("generated/" + resource['tag'] + '.py',"w+")
        iot_resource_file.write(format_data)
        iot_resource_file.close()

    def generate_resources(self):
        for resource in self.__metadata['resources']: 
            self.__generate_resource(resource)
            