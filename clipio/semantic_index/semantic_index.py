import rdflib
import statistics
from tinydb import TinyDB, Query

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

from clipio.semantic_index.processor.matrix import Matrix
from clipio.semantic_index.processor.metrics import Metrics

from clipio import constants as CON

""" pending: falta el idioma como settings """
class SemanticIndex:
    def __init__(self, settings, load_graph=True):
        self.__matrix = Matrix()
        self.__metrics = Metrics() 
        
        self.__file = settings['file']
        self.__tag = settings['tag']
        self.__min_wup_similarity = settings['min_wup_similarity']
        self.__language = 'es'

        if load_graph:
            self.__owl_terms = self.__owl_classes()

    def __owl_classes(self):
        graph = rdflib.Graph()
        graph.load(self.__file)
        result = graph.query(CON.ONTOLOGY_QUERY)
        filter_terms = []
        for row in result:
            tokens = self.__get_tokens(row[1], CON.LANGUAGE['en']['long'])
            for term in tokens:
                filter_terms.append(term)
        filter_repeat_terms = list(dict.fromkeys(filter_terms))
        
        terms = []
        for filter_repeat_term in filter_repeat_terms:
            if len(wn.synsets(filter_repeat_term)) > 0:
                terms.append(filter_repeat_term)
        
        return terms            
    
    def __get_tokens(self, text, lang):
        tokens = word_tokenize(text, lang)
        stop_words = stopwords.words(lang)

        filter_tokens = []
        for token in tokens:
            if token not in stop_words and token.isalpha():
                filter_tokens.append(token)

        return filter_tokens

    def __expand(self, term):
        expand_list = []
        synsets = wn.synsets(term, lang=CON.LANGUAGE[self.__language]['middle'])
        for synset in synsets:
            lemmas = synset.lemma_names(CON.LANGUAGE[self.__language]['middle'])
            for lemma in lemmas:
                if lemma not in expand_list:
                    expand_list.append(lemma)
        
        return expand_list

    def __wup_similarity(self, term_a, term_b):        
        term_a_list = wn.synsets(term_a, lang=CON.LANGUAGE[self.__language]['middle'])
        term_b_list = wn.synsets(term_b)

        if len(term_a_list) > 0:
            sim_list = []
            for a in term_a_list:
                for b in term_b_list:
                    sim = wn.wup_similarity(a, b)
                    if sim == None:
                        sim = 0
                    sim_list.append(sim)

            return statistics.mean(sim_list)
        else:
            return 0

    def __is_term_in_context(self, term):        
        for owl_term in self.__owl_terms:
            similarity = self.__wup_similarity(term, owl_term)
            if similarity > self.__min_wup_similarity: 
                return True
        return False

    def __semantic_filter(self, text):
        filter_terms = []
        tokens = self.__get_tokens(text, CON.LANGUAGE[self.__language]['long'])
        for token in tokens:
            if self.__is_term_in_context(token):
                filter_terms.append(token)
        return filter_terms

    def add_document(self, uuid, text):
        filter_terms = self.__semantic_filter(text)
        filter_terms.append("")
        
        self.__matrix.add_doc(     
            doc_id = uuid,
            doc_terms = filter_terms,
            frequency = True,
            do_padding = True
        )

    def save(self):
        self.__matrix.dump(self.__tag)

    def load(self):
        self.__matrix.load(self.__tag)

    def hot_docs(self, query):
        context_db = TinyDB(CON.CONTEXT_DB_PATH)
        self.load()
        
        query_terms = self.__get_tokens(query, CON.LANGUAGE[self.__language]['long'])
        query_expand_terms = []
        for term in query_terms:
            expand_list = self.__expand(term)
            query_expand_terms.extend(expand_list)
        query_vector = self.__matrix.query_to_vector(query_expand_terms, frequency=True)

        hot_list = []
        for doc in self.__matrix.docs:         
            match = context_db.search(Query()["id"] == doc["id"])
            if len(match) > 0:
                distance_cos = self.__metrics.cos_vectors(doc['terms'], query_vector)
                doc_data = {
                    'id': doc['id'],
                    'distance': distance_cos,
                    'name': match[0]['name'],
                    'description': match[0]['description']
                }
                hot_list.append(doc_data)
        
        context_db.close()
        return sorted(hot_list, key=lambda k:k['distance'], reverse=True)