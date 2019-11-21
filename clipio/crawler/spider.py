import json
from urllib.parse import urlparse
from tinydb import TinyDB
from coapthon.client.helperclient import HelperClient
from clipio import constants as CON

class Spider(object):
    def __init__(self, target_url):
        self.__to_visit = []
        self.__visted = []
        self.__target_url = self.__clean(target_url)

    def __clean(self, url):
        idx = url.find('#')
        if idx != -1:
            url = url[:idx]
        l = len(url)
        if url[l - 1] == '/':
            url = url[:l - 1]
        return url 

    def __find_key(self, key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in self.__find_key(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in self.__find_key(key, d):
                        yield result   

    def __request(self, url):
        url_components = urlparse(url)
        data_dict = None

        if str(url_components.scheme) == "coap":
            port = url_components.port
            if url_components.port is None:
                port = CON.DEFAULT_COAP_PORT
            server = (url_components.hostname, port)
            
            try:
                client = HelperClient(server)
                response = client.get(url_components.path[1:])
                data_dict = json.loads(response.payload)
            except:
                #poner que hay problemas con la url
                client = HelperClient(("8.8.8.8", 88))
                data_dict = None
            finally:
                client.stop()
                            
        if str(url_components.scheme) == "http":
            data_dict = None

        return data_dict
    
    def __parser(self, data_dict):   
        url_list = []
        corpus = ''

        for word in CON.METADATA_KEY_WORDS:
            corpus_result = self.__find_key(word, data_dict)
            for corpus_dot in list(corpus_result):
                corpus += ' ' + corpus_dot

        for word in CON.URL_KEY_WORDS:
            url_result = self.__find_key(word, data_dict)
            url_result_list = list(url_result)
            url_list += url_result_list

        return corpus, url_list        
    
    def collect(self):
        metadata = self.__request(self.__target_url)
        
        self.__to_visit.append(self.__target_url)   
        corpus_list = []
        while len(self.__to_visit) > 0:
            components_db = TinyDB("generated/components.json")
            table_crawler = components_db.table('crawler')
            enabled = table_crawler.all()[0]['enabled']
            components_db.close()
            if not enabled:
                break
            
            url = self.__to_visit.pop(0)
            data = self.__request(url)
            
            if data:
                corpus, url_list = self.__parser(data)
                self.__visted.append(url)
            
                corpus_list.append(corpus) 

                for url in url_list:
                    if url not in self.__visted and url not in self.__to_visit:
                        self.__to_visit.append(url)

        return metadata, corpus_list