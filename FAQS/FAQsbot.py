#https://www.analyticsvidhya.com/blog/2021/07/build-a-simple-chatbot-using-python-and-nltk/
#https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/
#https://www.nltk.org/_modules/nltk/chat/util.html#Chat
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

    # Hold a conversation with a chatbot
    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                while user_input[-1] in "!.":
                    user_input = user_input[:-1]
                try:
                    user_input = findClosestQuestion(user_input)
                    if (self.respond(user_input)!= None):
                        print(self.respond(user_input))
                    else:
                        print("I dont understand")
                except ZeroDivisionError:
                    print("I dont understand")


def findClosestQuestion(userQ):
    data = []
    with open('FAQs_q.txt') as f:
        lines = f.readlines()
        for line in lines:
            data.append(line.strip('\n'))
    cosineSimValsList = []
    for q in data:
        X = userQ
        Y = q
        # tokenization
        X_list = word_tokenize(X) 
        Y_list = word_tokenize(Y)
        # sw contains the list of stopwords
        sw = stopwords.words('english') 
        l1 =[];l2 =[]
        # remove stop words from the string
        X_set = {w for w in X_list if not w in sw} 
        Y_set = {w for w in Y_list if not w in sw}
        # form a set containing keywords of both strings 
        rvector = X_set.union(Y_set) 
        for w in rvector:
            if w in X_set: l1.append(1) # create a vector
            else: l1.append(0)
            if w in Y_set: l2.append(1)
            else: l2.append(0)
        c = 0
        # cosine formula 
        for i in range(len(rvector)):
                c+= l1[i]*l2[i]
        cosine = c / float((sum(l1)*sum(l2))**0.5)
        cosineSimValsList.append(cosine)
    maxSim = max(cosineSimValsList)
    if maxSim < 0.55:
        return(userQ)
    else:
        index = cosineSimValsList.index(maxSim)
        return(data[index])


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
        r"How many people are affected by Heart and Circulatory Diseases in the UK?",
        ["There are 7.6 million people living with heart and circulatory diseases in the UK.",]
    ],
    [
        r"How many people die from heart and circulatory diseases in the UK?",
        ["Heart and circulatory diseases cause a quarter of all deaths in the UK; that’s more than 160,000 deaths each year – or one death every three minutes."]
    ],
    [
        r"How many heart attacks are there in England each year?",
        ["There are over80,000 hospital admissions in England each year for heart attacks: that’s around 230 each day or 1 every six minutes."]
    ],

    [
        r"How many people die from strokes in Scotland each year?",
        ["Strokes cause over 3,700 deaths in Scotland each year."]
    ],

    [
        r"How many people have heart failure in Wales?",
        ["Around 3 6,000 people in Wales have been diagnosed with heart failure by their GP."]
    ],

    [
        r"How many people have high blood pressure in Northern Ireland?",
        ["An estimated 400,000 people in Northern Ireland have high blood pressure (hypertension)."]
    ],

    [
        r"How many men in the UK die from coronary heart disease?",
        ["In 2019, 39,845 men died from coronary heart disease in the UK."]
    ],

    [
        r"How many women aged 65\+ die from stroke in the UK?",
        ["In 2019, 18,157 women in the UK aged 65 and over died from stroke."]
    ],

    [
        r"How many people die from heart and circulatory diseases in Camden?",
        ["From 2017 to 2019, the average number of annual deaths in Camden from all heart and circulatory diseases was 296."]
    ],

    [
        r"How many people die from smoking in the UK?",
        ["In the UK it’s estimated that at least 80,000 deaths each year can be attributed to smoking. It’s estimated that at least 15,000 deaths in the UK each year from heart and circulatory diseases can be attributed to smoking."]
    ],

    [
        r"What percentage of men in England are classified as obese?",
        ["In England, around 27% of men are classified as obese."]
    ],
    [
        r"What percentage of women aged 65 and over in Wales are classified as obese?",
        ["In Wales, 25% of women aged 65-74 and 18% of women aged 75+ are classified as obese."]
    ],
    [
        r"What percentage of women in Northern Ireland are physically inactive?",
        ["In Northern Ireland, 49% of women do not meet the recommended levels of weekly physical activity."]
    ],
    [
        r"What local authority is worst affected by heart and circulatory diseases in the UK?",
        ["West Dunbartonshire in Scotland has the highest rate of age standardised deaths from Heart and Circulatory Diseases in the UK."]
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

def startChat():
    print("Welcome to HeartBot FAQ! \n")
    chat = Chat(pairs, reflections)
    chat.converse()

if __name__ == "__main__":
    startChat()