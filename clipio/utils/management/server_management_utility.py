import threading
from coapthon.server.coap import CoAP

from clipio.coap_resources.metadata import Metadata
#from clipio.coap_resources.eca import Eca
#from clipio.coap_resources.context import Context

from clipio.utils.log import ErrorLog, InfoLog

class ServerManagementUtility():
    def __init__(self, coap_server):
        self.__coap = CoAP((coap_server['domain'], coap_server['port']))       
        
        self.__domain = coap_server['domain']
        self.__port = coap_server['port']
        self.__resources = []
        
        self.__coap.add_resource('metadata', Metadata())
        self.__resources.append('metadata')

        #self.__coap.add_resource('eca', Eca())
        self.__resources.append('eca')

        #self.__coap.add_resource('context', Context())
        self.__resources.append('context')

    def add_iot_resource(self, name):
        try:
            mod = __import__('generated.'+ name, fromlist=[name.capitalize()])
            klass = getattr(mod, name.capitalize())
            obj = klass()
            self.__coap.add_resource(name, obj)
            self.__resources.append(name)
        except ModuleNotFoundError:
            ErrorLog.show("class %s not found" % (name.capitalize()))
        finally:
            pass

    def __run(self):  
        InfoLog.show("server run in %s:%s" % (
            self.__domain,
            self.__port
        ))
        for resource in self.__resources:
            InfoLog.show("set service %s" % (resource))
            
        self.__coap.listen()
        print("Server end")

    def run(self):
        run_thread = threading.Thread(target=self.__run)
        run_thread.start()

    def stop(self):
        self.__coap.close()
        print("stopping server...")