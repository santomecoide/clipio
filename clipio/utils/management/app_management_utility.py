import json
import clipio.constants as CON
from clipio.utils.seed import app_resource_seed
from tinydb import TinyDB

class AppManagementUtility:
    def __init__(self, settings):
        self.__metadata = settings.METADATA

    def __default_value(self, type_):
        for accepted_type in CON.ACCEPTED_TYPES:
            if accepted_type['name'] == type_:
                return accepted_type['default']
        return None

    def __data(self, tag, type_):
        data = {
            "value": self.__default_value(type_)
        }

        data_db = TinyDB("generated/data.json")    
        table = data_db.table(tag)
        table.purge()
        table.insert(data)
        data_db.close()
    
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

    def __components(self):        
        components_db = TinyDB("generated/components.json")

        crawler_data = {
            "enabled": False
        }
        table_crawler = components_db.table('crawler')
        table_crawler.purge()
        table_crawler.insert(crawler_data)
        
        eca_data = {
            "enabled": False
        }
        table_eca = components_db.table('eca')
        table_eca.purge()
        table_eca.insert(eca_data)
        
        components_db.close()
    
    def generate_files(self):
        self.__components()
        for resource in self.__metadata['resources']:
            self.__dev_file(resource['tag'], resource['type'])
            self.__data(resource['tag'], resource['type'])    