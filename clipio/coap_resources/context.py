from coapthon.resources.resource import Resource
from tinydb import TinyDB, Query
from clipio.semantic_index.semantic_index import SemanticIndex
from clipio.semantic_index import ontologies
from clipio import constants as CON

class Context(Resource):
    def __init__(self, ontologies_settings):
        super(Context, self).__init__("context")

        self.__semantic_index_list = []
        for ontology_settings in ontologies_settings:
            if ontology_settings['enabled']:
                for ontology in ontologies:
                    if ontology_settings['tag'] == ontology['tag']:
                        ontology_settings['file'] = ontology['file']
                        si_obj = SemanticIndex(ontology_settings, load_graph=False)
                        self.__semantic_index_list.append(si_obj)

    def __fix(self, data):
        fix_data = data.replace("'", '"')
        return fix_data

    def render_GET(self, request):
        id_ = 0
        payload = {}
        try:
            value = request._options[1]._value.split('=')
            if value[0] == 'id':
                id_ = value[1]
        except IndexError:
            pass
        
        context_db = TinyDB(CON.CONTEXT_DB_PATH)
        match = context_db.search(Query()["id"] == id_)
        if len(match) > 0:
            payload = match[0]
    
        self.payload = self.__fix(str(payload))
        return self

    def render_POST_advanced(self, request, response):
        hot_docs = []
        for semantic_index in self.__semantic_index_list:
            hot_docs = semantic_index.hot_docs(str(request.payload))

        response.payload = self.__fix(str(hot_docs))
        return self, response