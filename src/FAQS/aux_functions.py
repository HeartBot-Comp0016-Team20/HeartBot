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
        r"hi|hey|hello",
        ["Hello", "Hey there",]
    ], 
    [
        r"what is your name ?",
        ["I am HeartBot. you can call me crazy!",]
    ],
    [
        r"how are you",
        ["I'm doing good. How about You ?",]
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
