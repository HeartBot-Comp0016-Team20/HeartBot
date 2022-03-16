# Take the list of FAQs provided by the BHF and create question-answer pairs
def append_data (pairs, filename='FAQS/FAQs.txt'):
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

# Establish an initial list of pairs and responses and append the ones from the compendium
def create_pairs (): 
    pairs = [
    [
        r"hi|hey|hello|my name is (.*)",
        ["Hello", "Hey there", "hello, how are you today?"]
    ], 
    [
        r"what is your name|who are you|your name",
        ["I am HeartBot. you can call me crazy!",]
    ],
    [
        r"how are you|how are you feeling",
        ["I'm doing good. How about you?",]
    ],
    [
        r"I am fine|I am okay|I am good",
        ["Great to hear that, How can I help you?",]
    ],
    [
        r"i'm (.*) doing good",
        ["How can I help you?:)",]
    ],
    [
        r"(.*) created",
        ["UCL CS created me using Python's NLTK library for BHF","top secret ;)",]
    ],
    [
        r"NA",
        ["i dont understand the question"]
    ],
    [
        r"sorry",
        ["It's alright", "It's okay","Nevermind"]
    ],
    [
        r"quit|bye|goodbye",
        ["Bye take care. See you soon :) ","It was nice talking to you. See you soon :)","Thank you for using HeartBot FAQ"]
    ],
    ]
    return append_data(pairs)
