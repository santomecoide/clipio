import json
from urllib.parse import urlparse
from clipio.utils.log import ErrorLog, InfoLog
import clipio.constants as CON 

class SettingsManagementUtility:
    def __init__(self, settings):
        self.__metadata = settings.METADATA
        self.__coap_server = settings.COAP_SERVER
        self.__crawler = settings.CRAWLER
        self.__eca = settings.ECA
        self.__ontologies = settings.ONTOLOGIES
    
    def __metadata_val(self):
        correct = True
        
        if not self.__metadata['name'].strip():
            ErrorLog.show("metadata.name can not be empty")
            correct = False
        
        for resource in self.__metadata['resources']:
            if not resource['tag'].strip():
                ErrorLog.show("metadata.resource.tag can not be empty")
                correct = False

            if ' ' in resource['tag']:
                ErrorLog.show("metadata.resource.tag can not have whitespace. You give: %s" % (resource['tag']))
                correct = False

            if not resource['tag'].islower():
                ErrorLog.show("metadata.resource.tag can not have uppercase letters. You give: %s" % (resource['tag']))
                correct = False

            only_types = [ sub['name'] for sub in CON.ACCEPTED_TYPES ]
            if resource['type'] not in only_types:
                ErrorLog.show("metadata.resource.type not found. You give: %s" % (resource['type']))
                correct = False

            mqtt = resource['mqtt']
            if mqtt['enabled']:
                if type(mqtt['delay_time']) != int:
                    ErrorLog.show("metadata.resource.mqtt.delay_time is not int type. You give: %s" % (mqtt['delay_time']))
                    correct = False

                if mqtt['delay_time'] <= 0:
                    ErrorLog.show("metadata.resource.mqtt.delay_time must be greater than 0. You give: %s" % (mqtt['delay_time']))
                    correct = False

                if mqtt['qos'] not in CON.ACCEPTED_MQTT_QOS:
                    ErrorLog.show("metadata.resource.mqtt.qos not found. Accepted values are: %s. You give: %s" % (
                        str(CON.ACCEPTED_MQTT_QOS),
                        mqtt['qos']
                    ))
                    correct = False

                if not mqtt['host'].strip():
                    ErrorLog.show("metadata.resource.mqtt.host can not be empty")
                    correct = False

                if not mqtt['port'].strip():
                    ErrorLog.show("metadata.resource.mqtt.port can not be empty")
                    correct = False

                if mqtt['user'].strip() or mqtt['password'].strip():
                    if not mqtt['user'].strip():
                        ErrorLog.show("metadata.resource.mqtt.user can not be empty. You set password")
                        correct = False

                    if not mqtt['password'].strip():
                        ErrorLog.show("metadata.resource.mqtt.password can not be empty. You set user")
                        correct = False

        only_tags = [ sub['tag'] for sub in self.__metadata['resources'] ]
        for tag in only_tags:
            if only_tags.count(tag) > 1:
                ErrorLog.show("metadata.resource.tag can not be repeated. You give: %s" % (tag))
                correct = False

        return correct

    def __coap_val(self):
        correct = True

        if not self.__coap_server['host'].strip():
            ErrorLog.show("coap_server.host can not be empty")
            correct = False

        if not self.__coap_server['port']:
            ErrorLog.show("coap_server.port can not be empty")
            correct = False

        return correct

    def __crawler_val(self):
        correct = True

        if self.__crawler['enabled']:
            if self.__crawler['protocol'] not in CON.ACCEPTED_CRAWLER_PROTOCOLS:
                ErrorLog.show("crawler.protocol not found. You give: %s" % (self.__crawler['protocol']))
                correct = False

            if self.__crawler['delay_time'] < CON.MIN_CRAWLER_DELAY_TIME:
                ErrorLog.show("crawler.delay_time must be greater than %s. You give: %s" % (
                    str(CON.MIN_CRAWLER_DELAY_TIME),
                    self.__crawler['delay_time']
                ))
                correct = False

            if not isinstance(self.__crawler['url_list'], list): 
                ErrorLog.show("crawler.url_list not a list. You give: %s" % (self.__crawler['url_list']))
                correct = False

        return correct

    def __eca_val(self):
        correct = True
        
        if self.__eca['enabled']:
            if type(self.__eca['coap_request_delay_time']) != int:
                ErrorLog.show("eca.coap_request_delay_time is not int type. You give: %s" % (self.__eca['coap_request_delay_time']))
                correct = False

            if self.__eca['coap_request_delay_time'] <= 0:
                ErrorLog.show("eca.coap_request_delay_time must be greater than 0. You give: %s" % (self.__eca['coap_request_delay_time']))
                correct = False

            mqtt = self.__eca['mqtt']
            if mqtt['enabled']:
                if mqtt['user'].strip() or mqtt['password'].strip():
                    if not mqtt['user'].strip():
                        ErrorLog.show("eca.mqtt.user can not be empty. You set password")
                        correct = False

                    if not mqtt['password'].strip():
                        ErrorLog.show("eca.mqtt.password can not be empty. You set user")
                        correct = False

        return correct

    def __ontologies_val(self):
        correct = True

        if self.__crawler['enabled']:
            if len(self.__ontologies) > 0:
                ErrorLog.show("if enable crawler, you must be have 1 ontology at least")
                correct = False

        for ontology in self.__ontologies:
            if ontology['enabled']:

                if ontology['tag'] not in CON.ACCEPTED_ONTOLOGIES_TAGS:
                    ErrorLog.show("ontologies.tag not found. Accepted values are: %s. You give: %s" % (
                        str(CON.ACCEPTED_ONTOLOGIES_TAGS),
                        ontology['tag']
                    ))
                    correct = False

                wup = ontology['min_wup_similarity']
                if wup > 1 or wup < 0:
                    ErrorLog.show("ontologies.min_wup_similarity must be between 0 - 1. You give: %s" % (ontology['tag']))
                    correct = False

        return correct

    def validate(self, compare=False):
        correct = True
        
        correct = (
            self.__metadata_val() &
            self.__coap_val() &
            self.__crawler_val &
            self.__eca_val() &
            self.__ontologies_val()
        )

        if compare:
            metadata_file = open('generated/metadata.json','r')
            data = metadata_file.read()
            metadata_file.close()
            metadata = json.load(data)

            for resource in self.__metadata['resources']:
                tag_found = False
                for property_key in metadata['properties'].keys():
                    if property_key == resource['tag']:
                        property_ = metadata['properties'][property_key]
                        
                        if resource['type'] != property_['type']:
                            ErrorLog.show(
                                "metadata.resources.type bad generated. You give: %s. Use manage.py generate metadata" 
                                % (resource['type'])
                            )
                            correct = False

                        if resource['mqtt']['enabled']:
                            mqtt_form_found = False
                            for form in property_['forms']:
                                if form['protocol'] == 'mqtt': 
                                    url_components = urlparse(form['href'])

                                    if url_components.hostname != resource['mqtt']['host']:
                                        ErrorLog.show(
                                            "metadata.resources.mqtt.host bad generated. You give: %s. Use manage.py generate metadata" 
                                            % (resource['mqtt']['host'])
                                        )
                                        correct = False

                                    if url_components.port != resource['mqtt']['port']:
                                        ErrorLog.show(
                                            "metadata.resources.mqtt.port bad generated. You give: %s. Use manage.py generate metadata" 
                                            % (resource['mqtt']['port'])
                                        )
                                        correct = False
                                    
                                    mqtt_form_found = True

                                else:
                                    url_components = urlparse(form['href'])

                                    if url_components.hostname != self.__coap_server['host']:
                                        ErrorLog.show(
                                            "coap_server.host bad generated. You give: %s. Use manage.py generate metadata" 
                                            % (self.__coap_server['host'])
                                        )
                                        correct = False

                                    if url_components.port != self.__coap_server['port']:
                                        ErrorLog.show(
                                            "coap_server.port bad generated. You give: %s. Use manage.py generate metadata" 
                                            % (self.__coap_server['port'])
                                        )
                                        correct = False

                            if not mqtt_form_found:
                                ErrorLog.show("metadata.resources.mqtt bad generated. You enabled it. use manage.py generate metadata")
                                correct = False

                        tag_found = True
                        break                        
                
                if not tag_found:
                    ErrorLog.show(
                        "metadata.resources.tag bad generated. You give: %s. Use manage.py generate metadata" 
                        % (resource['tag'])
                    )
                    correct = False

        return correct