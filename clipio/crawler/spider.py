import json
import ast
from urllib.parse import urlparse

from coapthon.client.helperclient import HelperClient
from clipio import constants as CON

class Spider(object):
    def __init__(self, target_url):
        self.__to_visit = []
        self.__visted = []
        self.__target_url = target_url

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
                port = CON.COAP_PORT
            server = (url_components.netloc.split(':')[0], port)
            
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
        urls = []
        metadata_corpus = ''

        for word in CON.METADATA_KEY_WORDS:
            metadata_result = self.__find_key(word, data_dict)
            for metadata_dot in list(metadata_result):
                metadata_corpus += ' ' + metadata_dot

        for word in CON.URL_KEY_WORDS:
            url_result = self.__find_key(word, data_dict)
            url_result_list = list(url_result)
            urls += url_result_list

        return metadata_corpus, urls        

    def metadata_corpus(self):
        clean_url = self.__clean(self.__target_url)
        self.__to_visit.append(clean_url)   

        corpus = ""
        metadata_list = []
        while len(self.__to_visit) > 0:
            url = self.__to_visit.pop(0)
            data = self.__request(url)
            
            if data:
                metadata_list.append(data)
                _corpus, urls = self.__parser(data)
                self.__visted.append(url)
            
                corpus += _corpus 

                for url in urls:
                    if url not in self.__visted and url not in self.__to_visit:
                        self.__to_visit.append(url)

        return corpus, metadata_list