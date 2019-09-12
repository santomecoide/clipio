import rdflib
from semantics.processor.preprocessor import Preprocessor
from semantics.processor.matrix import Matrix
from semantics.processor.metrics import Metrics

class SemanticIndex:
    def __init__(self, name="dogont", load_graph=True):
        self.__matrix = Matrix()
        self.__preprocessor = Preprocessor()
        self.__metrics = Metrics() 
        
        self.__name = name
        self.__max_distance_euc = 1.5
        
        if load_graph:
            self.__owl_terms = self.__get_all_owl_classes()
        
    def __get_all_owl_classes(self):
        query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            SELECT ?class ?label
            WHERE { 
                    ?class a owl:Class .
                    ?class rdfs:label ?label
                    FILTER (lang(?label) = 'es')
            }
        """
        
        graph = rdflib.Graph()
        graph.load(
            "semantics/" +
            self.__name + "/" + 
            self.__name + ".owl"
        )
        result = graph.query(query)
        filter_terms = []
        for row in result:
            for term in self.__preprocessor.get_tokens(text=row[1]):
                filter_terms.append(term)

        return filter_terms

    def __is_term_related(self, term):
        term_vector = self.__matrix.query_to_vector(term, frequency=False)
        for owl_term in self.__owl_terms:
            owl_vector_term = self.__matrix.query_to_vector(owl_term, frequency=False)
            distance_euc = self.__metrics.euclid_vectors(owl_vector_term, term_vector)
            if distance_euc < self.__max_distance_euc: 
                return True
        return False

    def __semantic_filter(self, terms):
        filter_terms = []
        for term in terms:
            if self.__is_term_related(term):
                filter_terms.append(term)
        return filter_terms

    def add_document(self, uuid, text):
        terms = self.__preprocessor.get_tokens(text=text)
        filter_terms = self.__semantic_filter(terms)
        
        self.__matrix.add_doc(     
            doc_id = uuid,
            doc_terms = filter_terms,
            frequency = True,
            do_padding = True
        )

    def save(self):
        self.__matrix.dump(self.__name)

    def load(self):
        self.__matrix.load(self.__name)

    def get_doc_hot_list(self, query):
        query_terms = self.__preprocessor.get_tokens(text=query)
        query_vector = self.__matrix.query_to_vector(query_terms, frequency=True)

        #la lista de docuemtnos debe retornar el uuid la distancia
        #falta filtrar los terminos del query por la ontología
        #arreglar lo que retorna un doc (solo son id y terms)
        short_doc = {
            "uuid": None,
            "distance": None
        }
        for doc in self.__matrix.docs:           
            distance_euc = self.__metrics.euclid_vectors(
                doc['terms'], 
                query_vector
            ) 
            if short_doc["uuid"] == None:
                short_doc["uuid"] = doc['uuid']
                short_doc["distance"] = distance_euc 
            else:
                if short_doc["distance"] > distance_euc:
                    short_doc["uuid"] = doc['uuid']
                    short_doc["distance"] = distance_euc
            
        return short_doc["uuid"]