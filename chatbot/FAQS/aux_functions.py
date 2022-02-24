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
    