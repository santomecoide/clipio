import ast
from abc import abstractmethod
from coapthon.resources.resource import Resource

import clipio.constants as CON

class IotResource(Resource):
    def __init__(self, name, type):
        super(IotResource, self).__init__(name)

        self.__type = type
        self.__value = self.__default_value()
        self.__listener_flag = False

    def __default_value(self):
        for accepted_type in CON.ACCEPTED_TYPES:
            if accepted_type['name'] == self.__type:
                return accepted_type['default']
        return None 

    def __py_type(self):
        for accepted_type in CON.ACCEPTED_TYPES:
            if accepted_type['name'] == self.__type:
                return accepted_type['py_type']
        return None 

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, input_value):
        if not input_value: 
            input_value = self.__default_value()
        
        if type(input_value) != self.__py_type():
            raise Exception("incorrect value type")
        
        self.__value = input_value
    
    def render_GET(self, request):
        self.payload = str(self.__value)
        return self

    def render_PUT(self, request):
        data = request.payload
        self.__value = self.__py_type()(data)
        self.__listener_flag = False
        return self

    def listener(self):
        self.__listener_flag = True
        while self.__listener_flag: pass
    