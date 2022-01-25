#https://www.analyticsvidhya.com/blog/2021/07/build-a-simple-chatbot-using-python-and-nltk/
import nltk
from nltk.chat.util import Chat, reflections

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
        r"",
        [""]
    ],

    [
        r"",
        [""]
    ],

    [
        r"",
        [""]
    ],

    [
        r"",
        [""]
    ],

    [
        r"",
        [""]
    ],

    [
        r"",
        [""]
    ],

    [
        r"",
        [""]
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