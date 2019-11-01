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
        
        self.__enabled = crawler_settings['enabled']
        self.__run_flag = False
        self.__delay_time = crawler_settings['delay_time']  
        
        self.__url_list = []
        for url in crawler_settings['url_list']:
            self.__url_list.append(self.__complete_url(
                str(url), 
                crawler_settings['protocol'],
                crawler_settings['path']
            ))

    def __complete_url(self, url, protocol, path):
        protocol_full = protocol + "://"
        path_full = "/" + path 
        if protocol_full not in url:
            url = protocol_full + url
        if path_full not in url:
            url = url + path_full
        return url

    def __store(self, metadata_list):
        context_db = TinyDB("store/contextdb.json")
        for metadata in metadata_list:
            match = context_db.search(Query()["id"] == metadata['id'])
            if len(match) > 0:
                context_db.update(metadata, Query()["id"] == metadata['id'])
            else:
                context_db.insert(metadata)        
        context_db.close()
    
    def __spider(self, url):
        spider = Spider(url)
        corpus, metadata_list = spider.metadata_corpus()
        if len(metadata_list) > 0:
            self.__store(metadata_list)
        
        #llamar al inice semantico cargar y guardar documento 
        if corpus != "":
            pass
        
        self.__url_crawling_yet.remove(url)

    def run(self):
        self.__run_flag = True
        while self.__run_flag & self.__enabled:
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

    def stop(self): 
        for thread_id in self.__spider_id_running:
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                thread_id, 
                ctypes.py_object(SystemExit)
            ) 
            if res > 1: 
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        self.__run_flag = False