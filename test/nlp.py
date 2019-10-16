import rdflib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import statistics

owl_terms = get_all_owl_classes()

def get_wup_similarity(term_a, term_b):
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

def get_tokens(text):
    tokens = word_tokenize(text, "spanish")
    stop_words = stopwords.words("spanish")

    filter_tokens = []
    for token in tokens:
        if token not in stop_words and token.isalpha():
            filter_tokens.append(token)

    return filter_tokens

def get_all_owl_classes():
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
        "semantics/dogont/dogont.owl"
    )
    result = graph.query(query)
    filter_terms = []
    for row in result:
        for term in get_tokens(text=row[1]):
            filter_terms.append(term)

    return filter_terms

def semantic_filter(text):
    text_terms = get_tokens(text)


text1 = "Muy alejados luz, más allá alejados de las montañas los ñeros de palabras, alejados de los países lejos de las vocales y las consonantes, viven los textos simulados. viven aislados en casas de letras, en la costa de la semántica, un gran océano de lenguas. Un riachuelo llamado Pons fluye por su pueblo y los abastece con las normas necesarias."











