import json
from clipio import constants as CON
from tinydb import TinyDB
from clipio.utils.log import ErrorLog

class ValueHelper:
    def __init__(self, tag, type_):
        self.__tag = tag
        self.__type = type_

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
        data_db = TinyDB(CON.DATA_PATH)    
        try:
            table = data_db.table(self.__tag)
            value = self.__py_type()(table.all()[0]['value'])
        except ValueError:
            value = self.__default()
        data_db.close()
        return value

    @value.setter
    def value(self, input_value):        
        data_db = TinyDB(CON.DATA_PATH)
        try:
            data = {
                "value": self.__py_type()(input_value)
            }
            table = data_db.table(self.__tag)
            table.truncate()
            table.insert(data)
            success = True
        except ValueError:
            success = False
            ErrorLog.show("incorrect value type. Give: {}. Need: {}" 
                .format(type(input_value), self.__py_type()) 
            )
        data_db.close()
        return success
            
            