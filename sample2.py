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
        r"quit",
        ["Bye take care. See you soon :) ","It was nice talking to you. See you soon :)","Thank you for using HeartBot FAQ"]
    ],
]

def startChat():
    print("Welcome to HeartBot FAQ! \n")
    chat = Chat(pairs, reflections)
    chat.converse()

if __name__ == "__main__":
    print(reflections)
    startChat()