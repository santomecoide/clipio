import os
import ctypes
import threading

from tinydb import TinyDB

from clipio.eca.greater import Greater 
from clipio.eca.less import Less
from clipio.eca.grater_or_equal import GreaterOrEqual
from clipio.eca.less_or_equal import LessOrEqual
from clipio.eca.equal import Equal
from clipio.eca.not_equal import NotEqual

""" hacer un modelo de eca """

class Eca():
    def __init__(self, settings):        
        self.__eca = settings.ECA

        self.__run_flag = False
        self.__eca_id_running = []

    def __get_id(self): 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id

    def __greater(self, eca_id):
        gt = Greater(eca_id, self.__eca)
        gt.set_listener()

    def __less(self, eca_id):
        ls = Less(eca_id, self.__eca)
        ls.set_listener()

    def __greater_or_equal(self, eca_id):
        gteq = GreaterOrEqual(eca_id, self.__eca)
        gteq.set_listener()

    def __less_or_equal(self, eca_id):
        lseq = LessOrEqual(eca_id, self.__eca)
        lseq.set_listener()

    def __equal(self, eca_id):
        eq = Equal(eca_id, self.__eca)
        eq.set_listener()

    def __not_equal(self, eca_id):
        neq = NotEqual(eca_id, self.__eca)
        neq.set_listener()

    def __handler(self, eca):
        base = eca["actions"][eca["name"]]
        condition = base["input"]["properties"]["condition"]
        
        switcher = {
            ">": self.__greater,
            "<": self.__less,
            ">=": self.__greater_or_equal,
            "<=": self.__less_or_equal,
            "==": self.__equal,
            "!=": self.__not_equal,
        }
        function = switcher.get(
            condition["properties"]["operator"]["const"], 
            lambda:"Invalid"
        )
        function(eca["id"])

    def __run(self):
        self.__run_flag = True
        while self.__run_flag:
            eca_db = TinyDB("ecadb.json")
            for eca in eca_db.all():
                if eca["id"] not in self.__eca_id_running:
                    handler_thread = threading.Thread(
                        target=self.__handler, 
                        args=(eca, )
                    )
                    handler_thread.daemon = True
                    handler_thread.start()
                    self.__eca_id_running.append(eca["id"])
            eca_db.close()

        print("Eca end")

    def run(self):
        if self.__eca['enabled']:   
            components_db = TinyDB("generated/components.json")
            eca_data = {
                "enabled": True
            }
            table_eca = components_db.table('eca')
            table_eca.purge()
            table_eca.insert(eca_data)
            components_db.close()
            
            run_thread = threading.Thread(target=self.__run)
            run_thread.start()
            
            print("eca init")

    def stop(self):
        if self.__eca['enabled']:
            components_db = TinyDB("generated/components.json")
            eca_data = {
                "enabled": False
            }
            table_eca = components_db.table('eca')
            table_eca.purge()
            table_eca.insert(eca_data)
            components_db.close()
            
            self.__run_flag = False
            print("stopping eca...")