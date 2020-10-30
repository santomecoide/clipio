import uuid 
import json
import clipio.constants as CON 
from datetime import datetime
from clipio.utils.log import ErrorLog, InfoLog

class MetadataManagementUtility:
    def __init__(self, settings):
        self.__metadata = settings.METADATA
        self.__coap_server = settings.COAP_SERVER

    def __fix_metadata(self):        
        for key, value in self.__metadata.items(): 
            if isinstance(value, list):
                for v in value:
                    for key2, value2 in v.items():
                        index = value.index(v)
                        if type(value2) is dict: 
                            self.__metadata[key][index][key2] = value2
                        else:
                            self.__metadata[key][index][key2] = value2.strip()
            else:
                self.__metadata[key] = value.strip()
            
    def generate_metadata(self):
        self.__fix_metadata()
        
        id_ = str(uuid.uuid1())
        coap_host = self.__coap_server["host"]
        coap_port = str(self.__coap_server["port"])
        
        properties = {}
        for resource in self.__metadata['resources']:
            mqtt_host = resource['mqtt']['host']
            mqtt_port = str(resource['mqtt']['port'])
            mqtt_form = {
                "op": "readproperty",
                "protocol": "mqtt",
                "href": f"mqtt://{mqtt_host}:{mqtt_port}/{id_}/{resource['tag']}"
            }
            
            get_coap_form = {
                "op": "readproperty",
                "protocol": "coap",
                "href": f"coap://{coap_host}:{coap_port}/{id_}/{resource['tag']}",
                "methodName": "GET"
            }

            put_coap_form = {
                "op": "writeproperty",
                "protocol": "coap",
                "href": f"coap://{coap_host}:{coap_port}/{id_}/{resource['tag']}",
                "methodName": "PUT"
            }

            forms = [get_coap_form, put_coap_form]
            if resource['mqtt']['enabled']:
                forms.append(mqtt_form)
            
            properties[resource['tag']] = {
                "name": resource['name'],
                "description": resource['description'],
                "type": resource['type'],
                "unit": resource['unit'],
                "forms": forms    
            }
        
        metadata = {
            "id": id_,
            "name": self.__metadata['name'],
            "description": self.__metadata['description'],
            "created": str(datetime.now()),
            "modified": str(datetime.now()),
            "properties": properties
        } 

        with open(CON.METADATA_PATH, 'w') as fp:
            json.dump(metadata, fp)

        InfoLog.show("metadata generated")

    def tags(self):
        tags = []
        for resource in self.__metadata['resources']:
            tags.append(resource['tag'])
        return tags