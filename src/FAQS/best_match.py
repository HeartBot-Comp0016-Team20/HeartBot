from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class BestMatch:
    def __init__(self):
        self.data = []
        self.cosineSimValsList = []

    # Read the actual questions from FAQs_q.txt
    def take_data(self, filename='FAQS/FAQs_q.txt'):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                self.data.append(line.strip('\n'))

    def tokenize(self, X, Y):
        X_list = word_tokenize(X)
        Y_list = word_tokenize(Y)
        return X_list, Y_list

    def remove_stopwords(self,X_list,Y_list):
        # sw contains the list of stopwords
        sw = stopwords.words('english') 
        l1 =[];l2 =[]
  
        # remove stop words from the string
        X_set = {w for w in X_list if not w in sw} 
        Y_set = {w for w in Y_list if not w in sw}

        return l1,l2, X_set, Y_set

    def form_vector(self, X_set, Y_set, l1, l2):
        # form a set containing keywords of both strings 
        rvector = X_set.union(Y_set) 
        for w in rvector:
                if w in X_set: l1.append(1) # create a vector
                else: l1.append(0)
                if w in Y_set: l2.append(1)
                else: l2.append(0)

        return l1, l2, rvector

    def cosine_formula (self, l1, l2, rvector, cosineSimValsList):
        c = 0
        for i in range(len(rvector)):
            c+= l1[i]*l2[i]
        cosine = c / float((sum(l1)*sum(l2))**0.5)
        cosineSimValsList.append(cosine)

    def calculate_maxSim(self, userQ, data, cosineSimValsList):
        maxSim = max(cosineSimValsList)
        if maxSim < 0.55:
            return(userQ)
        else:
            index = cosineSimValsList.index(maxSim)
            return(data[index])
        
    def findClosestQuestion(self, userQ):
        data = self.data
        cosineSimValsList = self.cosineSimValsList
        self.take_data()

        for q in data:
        
            X_list, Y_list = self.tokenize(userQ, q)
            l1,l2, X_set,Y_set = self.remove_stopwords(X_list,Y_list)
            l1,l2, rvector = self.form_vector(X_set, Y_set, l1, l2)
            self.cosine_formula(l1,l2,rvector,cosineSimValsList)

        return self.calculate_maxSim(userQ, data, cosineSimValsList)