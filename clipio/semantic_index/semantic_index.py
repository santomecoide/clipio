import rdflib
import statistics
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

from semantic_index.processor.matrix import Matrix
from semantic_index.processor.metrics import Metrics

class SemanticIndex:
    def __init__(self, name="dogont", load_graph=True):
        self.__matrix = Matrix()
        self.__metrics = Metrics() 
        
        self.__name = name
        self.__max_distance = 3
        
        if load_graph:
            self.__owl_terms = self.__owl_classes()

    def __get_tokens(self, text):
        tokens = word_tokenize(text, "spanish")
        stop_words = stopwords.words("spanish")

        filter_tokens = []
        for token in tokens:
            if token not in stop_words and token.isalpha():
                filter_tokens.append(token)

        return filter_tokens

    def __wup_similarity(self, term_a, term_b):
        term_a_list = wn.synsets(term_a, lang="spa")
        term_b_list = wn.synsets(term_b, lang="spa")

        print(term_a_list)
        print(term_b_list)

        sim_list = []
        for a in term_a_list:
            for b in term_b_list:
                sim = wn.wup_similarity(a, b)
                if sim == None:
                    sim = 0
                sim_list.append(sim)

        return statistics.mean(sim_list)
        
    def __owl_classes(self):
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
            "semantic_index/" +
            self.__name + "/" + 
            self.__name + ".owl"
        )
        result = graph.query(query)
        filter_terms = []
        for row in result:
            for term in self.__get_tokens(text=row[1]):
                filter_terms.append(term)

        return filter_terms

    def __is_term_in_context(self, term):
        for owl_term in self.__owl_terms:
            similarity = self.__wup_similarity(term, owl_term)
            if similarity > 0.5: 
                return True
        return False

    def __semantic_filter(self, text):
        filter_terms = []
        text_terms = self.__get_tokens(text)
        for text_term in text_terms:
            if self.__is_term_in_context(text_term):
                filter_terms.append(text_term)
        return filter_terms

    def add_document(self, uuid, text):
        filter_terms = self.__semantic_filter(text)
        
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

    #EXPANDIR QUERY TERMS?
    def hot_list(self, query):
        query_terms = self.__get_tokens(text=query)
        query_vector = self.__matrix.query_to_vector(query_terms, frequency=True)

        doc_hot_list = []
        for doc in self.__matrix.docs:           
            distance_cos = self.__metrics.cos_vectors(
                doc['terms'], 
                query_vector
            )

            doc_data = {
                "uuid": doc['id'],
                "distance": distance_cos
            }

            doc_hot_list.append(doc_data)
            
        return sorted(doc_hot_list, key=lambda k:k['distance'], reverse=True)