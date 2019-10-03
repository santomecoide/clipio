import os
import ctypes
import threading

from tinydb import TinyDB

from eca.greater import Greater 
from eca.less import Less
from eca.grater_or_equal import GreaterOrEqual
from eca.less_or_equal import LessOrEqual
from eca.equal import Equal
from eca.not_equal import NotEqual

""" hacer un modelo de eca """

class Eca(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.__eca_id_running = []

    def __get_id(self): 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id

    def __greater(self, eca_id):
        gt = Greater(eca_id)
        gt.set_listener()

    def __less(self, eca_id):
        ls = Less(eca_id)
        ls.set_listener()

    def __greater_or_equal(self, eca_id):
        gteq = GreaterOrEqual(eca_id)
        gteq.set_listener()

    def __less_or_equal(self, eca_id):
        lseq = LessOrEqual(eca_id)
        lseq.set_listener()

    def __equal(self, eca_id):
        eq = Equal(eca_id)
        eq.set_listener()

    def __not_equal(self, eca_id):
        neq = NotEqual(eca_id)
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

    def run(self):
        try:
            while True:
                eca_db = TinyDB("ecadb.json")
                for eca in eca_db.all():
                    if eca["id"] not in self.__eca_id_running:
                        handler_thread = threading.Thread(
                            target=self.__handler, 
                            args=(eca, )
                        )
                        handler_thread.start()
                        self.__eca_id_running.append(eca["id"])
                eca_db.close()
        finally:
            self.__eca_id_running = []

    def stop(self):
        self.__eca_id_running.append(self.__get_id())
        for thread_id in self.__eca_id_running:
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                thread_id, 
                ctypes.py_object(SystemExit)
            ) 
            if res > 1: 
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)