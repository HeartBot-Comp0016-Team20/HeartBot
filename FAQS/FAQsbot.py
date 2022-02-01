import nltk
from nltk.chat.util import reflections
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import random

class Chat:
    def __init__(self, pairs, reflections={}):
        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections, key=len, reverse=True)
        return re.compile(r"\b({})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE)

    def _substitute(self, str):
        return self._regex.sub(lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower())

    def _wildcards(self, response, match):
        pos = -1
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find("%")
        return response

    def respond(self, str):
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)  # pick a random response
                resp = self._wildcards(resp, match)  # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == "?.":
                    resp = resp[:-2] + "."
                if resp[-2:] == "??":
                    resp = resp[:-2] + "?"
                return resp


    def check_input(self, user_input):
        matcher = BestMatch()
        if user_input:
            while user_input[-1] in "!.":
                user_input = user_input[:-1]
            try:
                user_input = matcher.findClosestQuestion(user_input)
                if (self.respond(user_input)!= None):
                    print(self.respond(user_input))
                else:
                    print("I dont understand")
            except ZeroDivisionError:
                print("I dont understand")

    # Hold a conversation with a chatbot
    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = input(">")
            except EOFError:
                print(user_input)
            self.check_input(user_input)
            
class BestMatch:
    def __init__(self):
        self.data = []
        self.cosineSimValsList = []

    def take_data(self, filename='FAQs_q.txt'):
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

def append_data (pairs, filename='FAQs.txt'):
    with open(filename) as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        pair = []
        pair.append(str(lines[i]).strip('\n'))
        pair.append([lines[i+1].strip('\n')])
        pairs.append(pair)
        i = i + 2
    return pairs

def create_pairs (): 
    pairs = [
    [
        r"hi|hey|hello",
        ["Hello", "Hey there",]
    ], 
    [
        r"what is your name ?",
        ["I am HeartBot. you can call me crazy!",]
    ],
    [
        r"how are you ?",
        ["I'm doing goodnHow about You ?",]
    ],
    [
        r"I am fine",
        ["Great to hear that, How can I help you?",]
    ],
    [
        r"i'm (.*) doing good",
        ["How can I help you?:)",]
    ],
    [
        r"(.*) created ?",
        ["UCL CS created me using Python's NLTK library for BHF","top secret ;)",]
    ],

    [
        r"NA",
        ["i dont understand the question"]
    ],
    [
        r"quit",
        ["Bye take care. See you soon :) ","It was nice talking to you. See you soon :)","Thank you for using HeartBot FAQ"]
    ],
]
    return append_data(pairs)
    

def startChat():
    print("Welcome to HeartBot FAQ! \n")
    pairs = create_pairs()
    chat = Chat(pairs, reflections)
    chat.converse()

if __name__ == "__main__":
    startChat()


# Sources:
#   https://www.analyticsvidhya.com/blog/2021/07/build-a-simple-chatbot-using-python-and-nltk/
#   https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/
#   https://www.nltk.org/_modules/nltk/chat/util.html#Chat