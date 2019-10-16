import sys
import os
import socket
from importlib import import_module

class HelpManagementUtility:
    def __init__(self):
        pass

    @staticmethod
    def help():
        print("type:")
        print("clipio.py [command] [file] [options]")

class MetadataManagementUtility:
    def __init__(self, project_name):
        self.__name = project_name

    def generate_metadata(self):
        settings_module = import_module(self.__name + ".settings")
        print(settings_module.METADATA)

class ProjectManagementUtility:
    def __init__(self, project_name, root_path):
        self.__path = self.__fix(root_path)
        self.__name = project_name
    
    def __fix(self, term):
        if term[-1:] != chr(47) and term[-1:] != chr(92): 
            new_term = term + chr(92) 
        return new_term

    def generate_project(self):
        domain = socket.gethostbyname(socket.gethostname())
        port = "5683"
        name_fix = self.__fix(self.__name)

        try: os.mkdir(self.__path + self.__name)
        except FileExistsError: pass

        try: os.mkdir(self.__path + name_fix + self.__name)
        except FileExistsError: pass

        settings_file = open(self.__path + name_fix + self.__name + '/settings.py',"w+")
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