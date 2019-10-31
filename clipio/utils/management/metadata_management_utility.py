import uuid 
import json
import clipio.constants as CON 
from datetime import datetime
from clipio.utils.log import ErrorLog, InfoLog

class MetadataManagementUtility:
    def __init__(self, metadata, coap_server):
        self.__metadata = metadata
        self.__coap_server = coap_server

    def __fix_metadata(self):        
        for key, value in self.__metadata.items(): 
            if isinstance(value, list):
                for v in value:
                    for key2, value2 in v.items():
                        index = value.index(v)
                        self.__metadata[key][index][key2] = value2.strip() 
            else:
                self.__metadata[key] = value.strip()

    def tags(self):
        tags = []
        for resource in self.__metadata['resources']:
            tags.append(resource['tag'])
        return tags

    def is_data_valid(self):
        error = False
        
        if not self.__metadata['name'].strip():
            ErrorLog.show("metadata.name can not be empty")
            error = True
        for resource in self.__metadata['resources']:
            if not resource['tag'].strip():
                ErrorLog.show("metadata.resource.tag can not be empty")
                error = True
            if ' ' in resource['tag']:
                ErrorLog.show("metadata.resource.tag can not have whitespace. You give: %s" % (resource['tag']))
                error = True

            if not resource['tag'].islower():
                ErrorLog.show("metadata.resource.tag can not have uppercase letters. You give: %s" % (resource['tag']))
                error = True

            only_types = [ sub['name'] for sub in CON.ACCEPTED_TYPES ]
            if resource['type'] not in only_types:
                ErrorLog.show("metadata.resource.type not found. You give: %s" % (resource['type']))
                error = True
            
        only_tags = [ sub['tag'] for sub in self.__metadata['resources'] ]
        for tag in only_tags:
            if only_tags.count(tag) > 1:
                ErrorLog.show("metadata.resource.tag can not be repeated. You give: %s" % (tag))
                error = True

        if not self.__coap_server['domain'].strip():
            ErrorLog.show("coap_server.domain can not be empty")
            error = True
        if not self.__coap_server['port']:
            ErrorLog.show("coap_server.port can not be empty")
            error = True

        return not error  
            
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
            
            properties[resource['tag']] = {
                "name": resource['name'],
                "description": resource['description'],
                "type": resource['type'],
                "unit": resource['unit'],
                "forms": [mqtt_form, get_coap_form, put_coap_form]    
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