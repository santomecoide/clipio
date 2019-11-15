import uuid 
import json
import clipio.constants as CON 
from datetime import datetime
from clipio.utils.log import ErrorLog, InfoLog

class MetadataManagementUtility:
    def __init__(self, settings):
        self.__metadata = settings.METADATA
        self.__coap_server = settings.COAP_SERVER
        self.__mqtt = settings.MQTT

    def __fix_metadata(self):        
        for key, value in self.__metadata.items(): 
            if isinstance(value, list):
                for v in value:
                    for key2, value2 in v.items():
                        index = value.index(v)
                        self.__metadata[key][index][key2] = value2.strip() 
            else:
                self.__metadata[key] = value.strip()

    #borrar
    """ def tags(self):
        tags = []
        for resource in self.__metadata['resources']:
            tags.append(resource['tag'])
        return tags """
            
    def generate_metadata(self):
        self.__fix_metadata()
        
        name = self.__metadata['name']
        domain = self.__coap_server["domain"]
        port = str(self.__coap_server["port"])
        
        properties = {}
        for resource in self.__metadata['resources']:
            mqtt_form = {
                "op": "readproperty",
                "protocol": "mqtt",
                "href": "mqtt://"+ domain +":"+ port +"/"+ name +"/"+ resource['tag']
            }
            
            get_coap_form = {
                "op": "readproperty",
                "protocol": "coap",
                "href": "coap://"+ domain +":"+ port +"/"+ name +"/"+ resource['tag'],
                "methodName": "GET"
            }

            put_coap_form = {
                "op": "writeproperty",
                "protocol": "coap",
                "href": "coap://"+ domain +":"+ port +"/"+ name +"/"+ resource['tag'],
                "methodName": "PUT"
            }

            forms = [get_coap_form, put_coap_form]
            if self.__mqtt['enabled']:
                forms.append(mqtt_form)
            
            properties[resource['tag']] = {
                "name": resource['name'],
                "description": resource['description'],
                "type": resource['type'],
                "unit": resource['unit'],
                "forms": forms    
            }
        
        metadata = {
            "id": str(uuid.uuid1()),
            "name": name,
            "description": self.__metadata['description'],
            "created": str(datetime.now()),
            "modified": str(datetime.now()),
            "properties": properties
        } 

        with open('generated/metadata.json', 'w') as fp:
            json.dump(metadata, fp)

        InfoLog.show("metadata generated")