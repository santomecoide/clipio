import time
import threading
from tinydb import TinyDB, Query
from clipio.crawler.spider import Spider
from clipio.semantic_index.semantic_index import SemanticIndex
from clipio.semantic_index import ontologies
from clipio import constants as CON

class Crawler():
    def __init__(self, settings):
        self.__crawler = settings.CRAWLER
        self.__ontologies = settings.ONTOLOGIES
        
        self.__run_flag = False
        self.__url_crawling_yet = []
        self.__delay_time = self.__crawler['delay_time']

        self.__semantic_index_list = []
        for ontology_settings in self.__ontologies:
            if ontology_settings['enabled']:
                for ontology in ontologies:
                    if ontology_settings['tag'] == ontology['tag']:
                        ontology_settings['file'] = ontology['file']
                        si_obj = SemanticIndex(ontology_settings)
                        self.__semantic_index_list.append(si_obj)  
        
        self.__url_list = []
        for url in self.__crawler['url_list']:
            self.__url_list.append(self.__complete_url(
                str(url), 
                self.__crawler['protocol'],
                self.__crawler['path']
            ))

    def __validate_metadata(self, metadata):
        validate = False
        if metadata:
            validate = True
            if "id" not in metadata:
                validate = False
            if "properties" not in metadata:
                validate = False
        return validate

    def __complete_url(self, url, protocol, path):
        protocol_full = protocol + "://"
        path_full = "/" + path 
        if protocol_full not in url:
            url = protocol_full + url
        if path_full not in url:
            url = url + path_full
        return url

    def __store(self, metadata):
        context_db = TinyDB(CON.CONTEXT_DB_PATH)
        match = context_db.search(Query()["id"] == metadata['id'])
        if len(match) > 0:
            context_db.update(metadata, Query()["id"] == metadata['id'])
        else:
            context_db.insert(metadata)        
        context_db.close()
    
    def __spider(self, url):
        spider = Spider(url)
        metadata, corpus_list = spider.collect()
        
        if self.__validate_metadata(metadata) and self.__run_flag:
            self.__store(metadata)  
        
            if len(corpus_list) > 0:
                corpus_str = ' '.join(corpus_list)
                for semantic_index in self.__semantic_index_list:
                    semantic_index.load()
                    semantic_index.add_document(metadata['id'], corpus_str) 
                    semantic_index.save()
        
        self.__url_crawling_yet.remove(url)

    def __run(self):
        self.__run_flag = True
        while self.__run_flag:
            for url in self.__url_list:
                if url not in self.__url_crawling_yet: 
                    self.__url_crawling_yet.append(url)
                    spider_thread = threading.Thread(
                        target=self.__spider, 
                        args=(url, )
                    )
                    spider_thread.daemon = True
                    spider_thread.start()
            
            for i in range(self.__delay_time):
                if i > 0 and not self.__run_flag:
                    break
                time.sleep(1)
        print("Crawler end")

    def run(self):
        if self.__crawler['enabled']:
            components_db = TinyDB(CON.COMPONENTS_PATH)
            crawler_data = {
                "enabled": True
            }
            table_crawler = components_db.table('crawler')
            table_crawler.purge()
            table_crawler.insert(crawler_data)
            components_db.close()
            
            run_thread = threading.Thread(target=self.__run)
            run_thread.start()

            print("crawler init")

    def stop(self):
        if self.__crawler['enabled']:
            components_db = TinyDB(CON.COMPONENTS_PATH)
            crawler_data = {
                "enabled": False
            }
            table_crawler = components_db.table('crawler')
            table_crawler.purge()
            table_crawler.insert(crawler_data)
            components_db.close()
            
            self.__run_flag = False
            print("stopping crawler...")