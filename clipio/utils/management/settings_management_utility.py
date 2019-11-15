from clipio.utils.log import ErrorLog, InfoLog
import clipio.constants as CON 

#falta poner lo de las ontologias
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

                if mqtt['qos'] not in CON.ACCEPTED_QOS:
                    ErrorLog.show("metadata.resource.mqtt.qos not found. Accepted values are: %s. You give: %s" % (
                        str(CON.ACCEPTED_QOS),
                        mqtt['qos']
                    ))
                    correct = False

                if not mqtt['port'].strip():
                    ErrorLog.show("metadata.resource.mqtt.port can not be empty")
                    correct = False

                if not mqtt['server'].strip():
                    ErrorLog.show("metadata.resource.mqtt.server can not be empty")
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

        if not self.__coap_server['domain'].strip():
            ErrorLog.show("coap_server.domain can not be empty")
            correct = False

        if not self.__coap_server['port']:
            ErrorLog.show("coap_server.port can not be empty")
            correct = False

        return correct

    def __crawler_val(self):
        correct = True

        if self.__crawler['enabled']:
            if self.__crawler['protocol'] not in CON.ACCEPTED_PROTOCOLS:
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
                if not mqtt['port'].strip():
                    ErrorLog.show("eca.mqtt.port can not be empty")
                    correct = False

                if not mqtt['server'].strip():
                    ErrorLog.show("eca.mqtt.server can not be empty")
                    correct = False

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

    def validate(self):
        correct = True
        
        correct = (
            self.__metadata_val() &
            self.__coap_val() &
            self.__crawler_val &
            self.__eca_val() &
            self.__ontologies_val()
        )

        return correct