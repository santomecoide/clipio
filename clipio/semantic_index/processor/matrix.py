import sys, math, random
from tinydb import TinyDB, Query
from clipio.semantic_index.processor.superlist import SuperList

class MatrixDocs(list):

    def doc_fields(self):
        return set(['id', 'terms'])

    def is_valid_doc(self, doc):
        doc_fields = set(doc.keys())
        return self.doc_fields().issubset(doc_fields)

    def index(self, doc_id):
        for i, doc in enumerate(self):
            if doc['id'] == doc_id:
                return i
        raise IndexError

    def __contains__(self, doc_id):
        try:
            self.index(doc_id)
            return True
        except:
            return False

    def add_unique(self, doc):
        if not self.is_valid_doc(doc):
            raise ValueError
        try:
            idx = self.index(doc['id'])
            self[idx]['terms'].add(doc['terms'])
        except IndexError:
            self.append(doc)      
    
    def shuffle(self):
        random.shuffle(self)

    def split(self):
        split_point = len(self)/2
        left  = MatrixDocs(self[:split_point]) 
        right = MatrixDocs(self[split_point:]) 
        return (left,right)

class Matrix:

    def __init__(self, whitelist=[], blacklist=[]):
        ''' Initilize our matrix.
            whitelist: If not empty, discard any terms not in whitelist,
                       when adding new terms via add_doc()
            blacklist: If not empty, discard any terms in blacklist,
                       when adding new terms via add_doc() 
                       Anything in the blacklist will be discarded,
                       even if it is in the whitelist.
            terms: We will populate this with our vocabulary of terms
            docs: This is our actual 2D matrix terms/docs.
                  A list of the following dictionary,
                  { 'id': Unique ID to each document 
                    'terms': list of 1's and 0's, i.e. term Frequencies.
                  }
        '''

        self.terms = SuperList()

        self.docs = MatrixDocs()
        self.whitelist = whitelist
        self.blacklist = blacklist

    def __len__(self):
        'Returns number of loaded ducuments'
        return len(self.docs)

    def vocabulary(self, threshold_map=[]):
        '''Returns list of all unique terms if threshold_map not given.
           Otherwise, only return terms above threshold.        
        '''
        if not threshold_map:
            return self.terms
        elif len(threshold_map) == len(self.terms):
            vlist = []
            for i in range(len(self.terms)):
                if threshold_map[i] == 1:
                   vlist.append(self.terms[i])
            return vlist 
        else:
            return []
            
            
    def __str__(self):
        s  = 'Matrix:'
        s += '\n * Vocabulary read: %d' % len(self.terms)
        s += '\n * Documents read: %d' % len(self.docs)
        return s

    """ pendding: pasar la ruto a constantes """
    def dump(self, tag):
        dump_db = TinyDB(
            'generated/' + tag + '_index.json'
        )
        dump_db.drop_tables()
        dump_db.purge()
        
        terms_table = dump_db.table('terms')
        terms_table.insert({
            'values': self.terms
        })

        for doc in self.docs:
            match = dump_db.search(Query()['id'] == doc['id'])
            if len(match) > 0:
                dump_db.update(
                    {
                        'id': doc['id'],
                        'values': doc['terms']
                    }, 
                    Query()["id"] == doc['id']
                )
            else:
                dump_db.insert({
                    'id': doc['id'],
                    'values': doc['terms']
                })

        dump_db.close()
    
    """ pendding: pasar la ruto a constantes """
    def load(self, tag):
        dump_db = TinyDB(
            "generated/" + tag + "_index.json"
        )

        terms_table = dump_db.table("terms")
        if len(terms_table) > 0:
            terms_data = terms_table.all()[0]['values']
            self.terms = SuperList(terms_data)

            d_table = dump_db.table("_default")
            for d_data in d_table.all():
                doc_data = {
                    'id': d_data['id'],
                    'terms': SuperList(d_data['values'])
                }
                self.docs.append(doc_data)

        dump_db.close()
                 
    def freq_levels(self, threshold=3):
        ''' Creates two lists:
            threshold_map is a list of 0's and 1's,
            where 1 means term's freq >= threshold
            freq_map is a list of terms frequences
        '''
        threshold_map = [0] * len(self.terms)
        freq_map = [0] * len(self.terms)
        for i in range(0,len(self.terms)):
            val = 0
            for doc in self.docs:
                if doc['terms'][i] != 0:
                    #val += 1 
                    val += doc['terms'][i]
            if val >= threshold:
                threshold_map[i] = 1
            freq_map[i] = val
        return (threshold_map, freq_map)         
        
    def __contains__(self, term):
        'Checks if certain terms is loaded'
        return self.terms.__contains__(term)        
        
    def __getitem__(self, term):
        ''' If term exists in terms, retruns it position in list,
            otherwise, return -1
        '''    
        if not term in self:
            return -1
        else:
            return self.terms.index(term)
    
    def do_padding(self):
        ''' Align the length of all rows in matrix
            Each time we see a new term, list of terms is expanded,
            and the matrix row for such document is of same length too.
            But what about rows added earlier for previous documents?
            So, this method alighn all previously added rows, 
            to match the current length of the terms list.
        '''
        if len(self.docs[-1]['terms']) == len(self.docs[0]['terms']):
            return
        for doc in self.docs:
            doc['terms'].expand(new_len=len(self.terms))
                               
    def add_doc(self, doc_id='',
            doc_terms=[], 
            frequency=False, 
            do_padding=False, 
            unique_ids=False,
            meta_data={}
    ):
        ''' Add new document to our matrix:
            doc_id: Identifier for the document, eg. file name, url, etc.
            doc_terms: List of terms you got after tokenizing the document.
                       Terms can be typles; string and frequencies
            frequency: If true, term occurences is incremented by one.
                        Else, occurences is only 0 or 1 (a la Bernoulli)
            do_padding: Boolean. Check do_padding() for more info.
            unique_ids: When true, if two documents are added with same id,
                        then their terms are summed up into only one record.
            meta_data: More fields to add to the document, for your own use.
        ''' 
        if not doc_terms:
            raise ValueError('doc_terms cannot be empty')
        # Update list of terms if new term seen.
        # And document (row) with its associated data.
        my_doc_terms = SuperList()
        # Discard anything not in whitelist if it is not empty
        if self.whitelist:
            doc_terms = [t for t in doc_terms if t in self.whitelist]
        # Discard anything in stopwords if not empty
        if self.blacklist: 
            doc_terms = [t for t in doc_terms if t not in self.blacklist]
        for term in doc_terms:
            if type(term) == tuple:
                term_idx = self.terms.unique_append(term[0])
                my_doc_terms.increment_after_padding(term_idx, term[1])
            else:
                term_idx = self.terms.unique_append(term)
                if frequency:
                    my_doc_terms.increment_after_padding(term_idx,1)
                else:
                    my_doc_terms.insert_after_padding(term_idx,1)
        # In the rare event when whitelisting causes an empty doc_terms list
        # We add at least one zero in the list of my_doc_terms
        if not my_doc_terms:
            zeros = [float(0)] * len(self.vocabulary())
            my_doc_terms = SuperList(zeros)
         
        doc_data = { 
            'id': doc_id, 
            'terms': my_doc_terms
        }

        for key in meta_data:
            doc_data[key] = meta_data[key]

        if unique_ids:
            self.docs.add_unique(doc_data)              
        else:
            self.docs.append(doc_data)

        if do_padding: 
            self.do_padding()

    def query_to_vector(self, q_terms, frequency=False,):
        ''' Converts query to a list alligned with our self.terms.
            Terms not seen before will be ignored.
            q_terms: list of query terms
            frequency: return a multinomial or multivariate list?
        '''
        my_query_vector = SuperList()
        my_query_vector.expand(new_len=len(self.terms))
        for term in q_terms:
            try:
                term_idx = self.terms.index(term)
            except:
                # Term not seen before, skip
                continue
            #print term, self.terms.index(term)
            if frequency:
                my_query_vector.increment_after_padding(term_idx,1)
            else:
                my_query_vector.insert_after_padding(term_idx,1)
        return my_query_vector

if __name__ == '__main__':
    pass