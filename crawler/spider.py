import json
import ast
from urllib.parse import urlparse

from coapthon.client.helperclient import HelperClient

metadata_key_words = ["name", "description", "title"]
url_key_words = ["href", "link"]

class Spider(object):
    def __init__(self, target_url):
        self.__to_visit = []
        self.__visted = []
        
        self.__target_url = target_url
        self.metadata = ""

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

    def __parser(self, url):   
        urls = []
        metadata = []
        url_components = urlparse(url)
        
        if str(url_components.scheme) == "coap":
            port = url_components.port
            if url_components.port is None:
                port = 5683

            server = (url_components.netloc, port)
            client = HelperClient(server)
            response = client.get(url_components.path)
            
            try:
                data_dict = (response.payload)
            except:
                data_dict = json.loads("{}")

            for word in metadata_key_words:
                metadata_result = self.__find_key(word, data_dict)
                metadata_result_list = list(metadata_result)
                metadata += metadata_result_list

            for word in url_key_words:
                url_result = self.__find_key(word, data_dict)
                url_result_list = list(url_result)
                urls += url_result_list
                
        if str(url_components.scheme) == "http":
            pass

        return metadata, urls

    def get_metadata(self):
        clean_url = self.__clean(self.__target_url)
        self.__to_visit.append(clean_url)   

        while len(self.__to_visit) > 0:
            url = self.__to_visit.pop(0)
            metadata, urls = self.__parser(url)
            self.__visted.append(url)
            
            for md in metadata:
                self.metadata += ' ' + md 
            
            for url in urls:
                if url not in self.__visted and url not in self.__to_visit:
                    self.__to_visit.append(url)

        return self.metadata