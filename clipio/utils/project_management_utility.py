import sys
import os
import socket

class ProjectManagementUtility:
    def __init__(self, project_name, root_path):
        self.__path = self.__fix(root_path)
        self.__name = project_name
    
    def __fix(self, term):
        if term[-1:] != chr(47) and term[-1:] != chr(92): 
            new_term = term + chr(92) 
        return new_term

    def __gen_settings(self, path):
        domain = socket.gethostbyname(socket.gethostname())
        port = "5683"
        
        settings_file = open(path + '/settings.py',"w+")
        
        settings_file.write('NAME = "' + self.__name + '"\n')

        settings_file.write('\n')
        
        settings_file.write('METADATA = {\n')
        settings_file.write('\t"name": "' + self.__name + '",\n')
        settings_file.write('\t"description": "",\n')
        settings_file.write('\t"resources": [\n')
        settings_file.write('\t\t{\n')
        settings_file.write('\t\t\t"name": "",\n')
        settings_file.write('\t\t\t"description": "",\n')
        settings_file.write('\t\t\t"type": "",\n')
        settings_file.write('\t\t\t"unit": ""\n')
        settings_file.write('\t\t},\n')
        settings_file.write('\t\t{\n')
        settings_file.write('\t\t\t"name": "",\n')
        settings_file.write('\t\t\t"description": "",\n')
        settings_file.write('\t\t\t"type": "",\n')
        settings_file.write('\t\t\t"unit": ""\n')
        settings_file.write('\t\t}\n')
        settings_file.write('\t]\n')
        settings_file.write('}\n')

        settings_file.write('\n')

        settings_file.write('COAP_SERVER = {\n')
        settings_file.write('\t"domain": "' + domain + '",\n')
        settings_file.write('\t"port": "' + port + '"\n')
        settings_file.write('}\n')

        settings_file.close()

    def __gen_manager(self, path):
        manager_file = open(path + '/manage.py',"w+")
                
        manager_file.write('import sys\n')
        manager_file.write('import settings\n')
        manager_file.write('from clipio.utils.metadata_management_utility import MetadataManagementUtility\n')
        manager_file.write('from clipio.utils.help_management_utility import HelpManagementUtility\n')
        manager_file.write('\n')
        manager_file.write('if __name__ == "__main__":\n')
        manager_file.write('\thelp_mu = HelpManagementUtility\n')
        manager_file.write('\ttry:\n')
        manager_file.write('\t\tcom = sys.argv[1]\n')
        manager_file.write('\t\tif com == "generate" or com == "g":\n')
        manager_file.write('\t\t\tmetadata_mu = MetadataManagementUtility(settings.METADATA)\n')
        manager_file.write('\t\t\tmetadata_mu.generate_metadata()\n')
        manager_file.write('\t\tif com == "help" or com == "h":\n')
        manager_file.write('\t\t\thelp_mu.help()\n')
        manager_file.write('\texcept IndexError:\n')
        manager_file.write('\t\thelp_mu.help()\n')

        manager_file.close()
    
    def generate_project(self):
        try: os.mkdir(self.__path + self.__name)
        except FileExistsError: pass

        try: os.mkdir(self.__path + self.__name)
        except FileExistsError: pass

        self.__gen_settings(self.__path + self.__name)
        self.__gen_manager(self.__path + self.__name)