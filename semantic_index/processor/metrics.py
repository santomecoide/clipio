''' 
Informations Retrieval Library
==============================
Metrics
'''

# Author: Tarek Amr <@gr33ndata> 

import math

class Metrics:

    def check_same_len(self, a=[], b=[]):
        if len(a) != len(b):
            raise ValueError('Vectors not with same length')

    def levenshtein_distance(self, str1, str2):
        d = dict()
        for i in range(len(str1) + 1):
            d[i] = dict()
            d[i][0] = i
        for i in range(len(str2) + 1):
            d[0][i] = i
        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
        return d[len(str1)][len(str2)]

    def euclid_vectors(self, a=[], b=[]):
        ''' Calculate Euclidean distance between two vectors (lists)
        ''' 
        self.check_same_len(a,b)
        euclid_sqrd = 0
        for i in range(0,a.__len__()):
            euclid_sqrd += ((a[i] - b[i])*(a[i] - b[i]))
        return math.sqrt(euclid_sqrd)

    def cos_vectors(self, a=[], b=[]):
        ''' Calculates the cosine distance between two vectors (lists)
        '''
        self.check_same_len(a,b)
        norm_a_sqrd = norm_b_sqrd = 0
        numerator = 0
        for i in range(0,len(a)):
            numerator = numerator + a[i]*b[i]
            # Do not use math.pow(), time consuming!
            norm_a_sqrd = norm_a_sqrd + (a[i]*a[i]) 
            norm_b_sqrd = norm_b_sqrd + (b[i]*b[i])
        # In some cases, when one vector is all zeros, division by zero happens
        # Normally this happens when training on small training-set
        # And all vocabulary in query is first time to be seen.
        denominator = max(0.0000001, 
            (   
                math.sqrt(norm_a_sqrd) *
                math.sqrt(norm_b_sqrd)
            )
        )
        return_value = numerator / denominator
        return return_value
    
    def jaccard_vectors(self, a=[], b=[]):
        self.check_same_len(a,b) 
        if a == b:
            return 1  
        intersection = [bool(i) and bool(j) for i,j in zip(a,b)]
        union = len(a) + len(b) - len(intersection)
        return sum(intersection) / float(union)

    def dot_product(self, a=[], b=[]):
        ''' Calculates the dot product between two vectors (lists)
        '''
        self.check_same_len(a,b)
        numerator = 0
        for i in range(0,len(a)):
            numerator = numerator + a[i]*b[i]
        if not numerator:
            return 0 
        return_value = float(numerator) 
        return return_value

if __name__ == '__main__':
    m = Metrics()
    print("Euclid:", m.euclid_vectors([1,1],[4,5]))
    print("Cosine:", m.cos_vectors([1,1,1],[1,1,1]))
    print("Dot Product:", m.dot_product([1,1,1],[1,1,1]))