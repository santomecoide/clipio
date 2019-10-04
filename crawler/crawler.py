import time
import ctypes
import threading

from crawler.spider import Spider

class Crawler(threading.Thread):
    def __init__(self): 
        threading.Thread.__init__(self) 
        self.__url_crawling_yet = []
        self.__spider_id_running = []
        
        #debe ir en constantes globales
        self.__contex_list = ["dogont"]
        self.__url_list = ["192.168.0.16"]     
        self.__crawl_delay_time = 3 #60000     

    def __spider(self, url):
        try:
            spider = Spider(url)
            metadata = spider.get_metadata()
            #llamar al inice semantico cargar y guardar documento
        finally: 
            self.__url_crawling_yet.remove(url)

    def __get_id(self): 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id

    def run(self):
        try: 
            while True:
                for url in self.__url_list:
                    if url not in self.__url_crawling_yet: 
                        self.__url_crawling_yet.append(url)
                        spider_thread = threading.Thread(
                            target=self.__spider, 
                            args=(url, )
                        )
                        spider_thread.start()
                        self.__spider_id_running.append(spider_thread._ident)
                time.sleep(self.__crawl_delay_time)
        finally:
            self.__spider_id_running = []
            self.__url_crawling_yet = []

    def stop(self): 
        self.__spider_id_running.append(self.__get_id())
        for thread_id in self.__spider_id_running:
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                thread_id, 
                ctypes.py_object(SystemExit)
            ) 
            if res > 1: 
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)