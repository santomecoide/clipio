from nltk.corpus import wordnet as wn
import statistics

def get_wup_similarity(term_a, term_b):
    term_a_list = wn.synsets(term_a, lang="spa")
    term_b_list = wn.synsets(term_b, lang="spa")

    sim_list = [0]
    for a in term_a_list:
        for b in term_b_list:
            sim = wn.wup_similarity(a, b)
            if sim == None:
                sim = 0
            sim_list.append(sim)

    return statistics.mean(sim_list)

print(get_wup_similarity('persona', 'calefacción'))