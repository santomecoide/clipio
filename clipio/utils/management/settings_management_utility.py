from clipio.utils.log import ErrorLog, InfoLog
import clipio.constants as CON 

class SettingsManagementUtility:
    def __init__(self, settings):
        self.__metadata = settings['METADATA']
        self.__coap_server = settings['COAP_SERVER']
        self.__crawler = settings['CRAWLER']
    
    def validate(self):
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

        if self.__crawler['protocol'] not in CON.ACCEPTED_PROTOCOLS:
            ErrorLog.show("crawler.protocol not found. You give: %s" % (self.__crawler['protocol']))
            error = True

        if self.__crawler['delay_time'] <  CON.MIN_CRAWLER_DELAY_TIME:
            ErrorLog.show("crawler.delay_time must be greater than %s. You give: %s" % (
                CON.MIN_CRAWLER_DELAY_TIME,
                self.__crawler['delay_time']
            ))
            error = True

        if not isinstance(self.__crawler['url_list'], list): 
            ErrorLog.show("crawler.url_list not a list. You give: %s" % (self.__crawler['url_list']))
            error = True

        return not error