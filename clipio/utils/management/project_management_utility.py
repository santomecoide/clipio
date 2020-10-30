import sys
import os
import socket

import constants as CON

class ProjectManagementUtility:
    def __init__(self, project_name, root_path):
        self.__path = self.__fix(root_path)
        self.__name = project_name
    
    def __fix(self, term):
        if term[-1:] != chr(47) and term[-1:] != chr(92): 
            new_term = term + chr(92) 
        return new_term

    """ pendding: pasar la ruta a constantes """
    def __gen_settings(self, path):
        host = socket.gethostbyname(socket.gethostname())
        port = CON.DEFAULT_COAP_PORT
        
        seed = open('utils/seed/settings.txt','r')
        data = seed.read()
        seed.close()

        format_data = data.replace("{name}", self.__name)
        format_data = format_data.replace("{host}", host)
        format_data = format_data.replace("{port}", port)

        settings_file = open(path + '/settings.py','w+')
        settings_file.write(format_data)
        settings_file.close()

    """ pendding: pasar la ruta a constantes """
    def __gen_manager(self, path):
        seed = open('utils/seed/manage.txt','r')
        data = seed.read()
        seed.close()

        manage_file = open(path + '/manage.py','w+')
        manage_file.write(data)
        manage_file.close()
    
    def generate_project(self):
        try: os.mkdir(self.__path)
        except FileExistsError: pass

        try: os.mkdir(self.__path + self.__name)
        except FileExistsError: pass

        try: os.mkdir(self.__path + self.__name + "/generated")
        except FileExistsError: pass

        try: os.mkdir(self.__path + self.__name + "/app")
        except FileExistsError: pass

        self.__gen_settings(self.__path + self.__name)
        self.__gen_manager(self.__path + self.__name)