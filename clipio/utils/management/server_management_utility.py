from coapthon.server.coap import CoAP

#from clipio.coap_resources.metadata import Metadata
#from clipio.coap_resources.eca import Eca
#from clipio.coap_resources.context import Context

from clipio.utils.log import ErrorLog, InfoLog

class ServerManagementUtility(CoAP):
    def __init__(self, coap_server):
        CoAP.__init__(self, (coap_server['domain'], coap_server['port']), False)
        self.__domain = coap_server['domain']
        self.__port = coap_server['port']
        self.__resources = []
        
        #self.add_resource('metadata', Metadata())
        self.__resources.append('metadata')

        #self.add_resource('eca', Eca())
        self.__resources.append('eca')

        #self.add_resource('context', Context())
        self.__resources.append('context')

    def add_iot_resource(self, name):
        try:
            mod = __import__('generated.'+ name, fromlist=[name.capitalize()])
            klass = getattr(mod, name.capitalize())
            obj = klass()
            self.add_resource(name, obj)
            self.__resources.append(name)
        except ModuleNotFoundError:
            ErrorLog.show("class %s not found" % (name.capitalize()))
        finally:
            pass

    def run(self):
        InfoLog.show("server run in %s %s" % (
            self.__domain,
            self.__port
        ))
        for resource in self.__resources:
            InfoLog.show("set service %s" % (resource))
            
        self.listen()

    def stop(self):
        self.close()

    