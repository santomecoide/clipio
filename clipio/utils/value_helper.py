import json
from clipio import constants as CON

class ValueHelper:
    def __init__(self, tag, type_):
        self.__tag = tag
        self.__type = type_

    def __busy(self):
        try:
            busy_file = open('generated/'+ self.__tag +'_busy.txt', 'r')
            is_busy = bool(int(busy_file.read()))
        except:
            is_busy = True
        finally:
            busy_file.close()
            return is_busy  

    def __set_busy(self):
        busy_file = open('generated/'+ self.__tag +'_busy.txt', 'w')
        busy_file.write('1')
        busy_file.close()

    def __unset_busy(self):
        busy_file = open('generated/'+ self.__tag +'_busy.txt', 'w')
        busy_file.write('0')
        busy_file.close()

    def __py_type(self):
        for accepted_type in CON.ACCEPTED_TYPES:
            if accepted_type['name'] == self.__type:
                return accepted_type['py_type']
        return None

    def __default(self):
        for accepted_type in CON.ACCEPTED_TYPES:
            if accepted_type['name'] == self.__type:
                return accepted_type['default']
        return None 

    @property
    def value(self):
        while self.__busy(): pass
        self.__set_busy()

        try:
            with open('generated/'+ self.__tag +'.json') as fp:
                data = json.load(fp)
                value = self.__py_type()(data['value'])
        except ValueError:
            value = self.__default()
        finally:
            self.__unset_busy()
            return value

    @value.setter
    def value(self, input_value):
        if not input_value: 
            input_value = self.__default()
        
        if type(input_value) != self.__py_type():
            input_value = self.__default()
            #poner ("incorrect value type")
        else:
            while self.__busy(): pass
            self.__set_busy()
            
            with open('generated/'+ self.__tag +'.json', 'w') as fp:
                json.dump({"value": input_value}, fp)

            self.__unset_busy()
            