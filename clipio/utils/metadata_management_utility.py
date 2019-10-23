import uuid 
import json
from datetime import datetime
import clipio.constants as CON 

class MetadataManagementUtility:
    def __init__(self, metadata, coap_server):
        self.__metadata = metadata
        self.__coap_server = coap_server

        self.__fix_metadata()
        self.__fix_tags()

    def __fix_tags(self):
        for resource in self.__metadata['resources']: 
            resource['tag'] = resource['tag'].lower()

    def __fix_metadata(self):        
        for key, value in self.__metadata.items(): 
            if isinstance(value, list):
                for v in value:
                    for key2, value2 in v.items():
                        index = value.index(v)
                        self.__metadata[key][index][key2] = value2.strip() 
            else:
                self.__metadata[key] = value.strip()

    def get_fix_metadata(self):
        return self.__metadata

    def is_data_valid(self):
        error_log = []
        
        if not self.__metadata['name'].strip():
            error_log.append("metadata.name can not be empty")

        for resource in self.__metadata['resources']:
            if not resource['tag'].strip():
                error_log.append("metadata.resource.tag can not be empty")
            if ' ' in resource['tag']:
                error_log.append("metadata.resource.tag can not have whitespace. You give: %s" % (resource['tag']))

            only_types = [ sub['name'] for sub in CON.ACCEPTED_TYPES ]
            if resource['type'] not in only_types:
                error_log.append("metadata.resource.type not found. You give: %s" % (resource['type']))
            
        only_tags = [ sub['tag'] for sub in self.__metadata['resources'] ]
        for tag in only_tags:
            if only_tags.count(tag) > 1:
                error_log.append("metadata.resource.tag can not be repeated. You give: %s" % (tag))

        if not self.__coap_server['domain'].strip():
            error_log.append("coap_server.domain can not be empty")
        if not self.__coap_server['port'].strip():
            error_log.append("coap_server.port can not be empty")

        if len(error_log) > 0:
            print("Error!")
            for error in error_log:
                print(error)
            return False
        return True  
            
    def generate_metadata(self):
        name = self.__metadata['name']
        domain = self.__coap_server["domain"]
        port = self.__coap_server["port"]
        
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

        with open('metadata.json', 'w') as fp:
            json.dump(metadata, fp)