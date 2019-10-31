import time
import ctypes
import threading

from tinydb import TinyDB, Query
from clipio.crawler.spider import Spider

class Crawler(threading.Thread):
    def __init__(self, crawler_settings): 
        threading.Thread.__init__(self) 
        self.__url_crawling_yet = []
        self.__spider_id_running = []
        
        self.__delay_time = crawler_settings['delay_time']  
        
        self.__url_list = []
        for url in crawler_settings['url_list']:
            self.__url_list.append(self.__complete_url(
                url, 
                crawler_settings['protocol'],
                crawler_settings['path']
            ))

    def __complete_url(self, url, protocol, path):
        protocol_full = protocol + "://"
        path_full = "/" + path 
        if protocol_full not in url:
            url = protocol + url
        if path_full not in url:
            url = protocol + url
        return url

    def __store(self, metadata_list):
        context_db = TinyDB("store/contextdb.json")
        for metadata in metadata_list:
            match = context_db.search(Query()["id"] == metadata['id'])
            if match > 0:
                context_db.update(metadata, Query()["id"] == metadata['id'])
            else:
                context_db.insert(metadata)        
        context_db.close()
    
    def __spider(self, url):
        try:
            spider = Spider(url)
            corpus, metadata_list = spider.metadata_corpus()
            self.__store(metadata_list)
            #llamar al inice semantico cargar y guardar documento
        finally: 
            self.__url_crawling_yet.remove(url)

    def __id(self): 
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
                time.sleep(self.__delay_time)
        finally:
            self.__spider_id_running = []
            self.__url_crawling_yet = []

    def stop(self): 
        self.__spider_id_running.append(self.__id())
        for thread_id in self.__spider_id_running:
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                thread_id, 
                ctypes.py_object(SystemExit)
            ) 
            if res > 1: 
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)