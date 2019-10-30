import json
import clipio.constants as CON
from clipio.utils.seed import app_resource_seed

class AppManagementUtility:
    def __init__(self, metadata):
        self.__metadata = metadata

    def __default_value(self, type_):
        for accepted_type in CON.ACCEPTED_TYPES:
            if accepted_type['name'] == type_:
                return accepted_type['default']
        return None

    def __data_file(self, tag, type_):
        busy_file = open('generated/'+ tag +'_busy.txt','w+')
        busy_file.write('0')
        busy_file.close()
        
        with open('generated/'+ tag +'.json', 'w') as fp:
            json.dump({"value": self.__default_value(type_)}, fp)
    
    def __dev_file(self, tag, type_):
        get_format_data = app_resource_seed.format(
            tag,
            tag, 
            tag,
            type_
        )
        get_file = open('app/'+ tag +'.py','w+')
        get_file.write(get_format_data)
        get_file.close()
    
    def generate_files(self):
        for resource in self.__metadata['resources']:
            self.__dev_file(resource['tag'], resource['type'])
            self.__data_file(resource['tag'], resource['type'])    