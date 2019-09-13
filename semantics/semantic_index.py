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
        self.__max_distance = 3
        
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

    #revisar para distancia semantica https://www.geeksforgeeks.org/nlp-wupalmer-wordnet-similarity/
    #para españon https://codeday.me/es/qa/20190503/633497.html
    def __is_term_related(self, term):
        for owl_term in self.__owl_terms:
            distance = self.__metrics.levenshtein_distance(term, owl_term)
            if distance < self.__max_distance: 
                print(owl_term)
                print(term)
                print(distance)
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

        doc_list = []
        for doc in self.__matrix.docs:           
            distance_euc = self.__metrics.cos_vectors(
                doc['terms'], 
                query_vector
            )

            doc_data = {
                "uuid": doc['id'],
                "distance": distance_euc
            }

            doc_list.append(doc_data)
            
        return sorted(doc_list, key=lambda k:k['distance'], reverse=True)