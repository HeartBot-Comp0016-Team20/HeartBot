from nltk.chat.util import reflections
from FAQS import converse
from FAQS import aux_functions
    

if __name__ == "__main__":
    print("Welcome to HeartBot FAQ! \n")
    pairs = aux_functions.create_pairs()
    chat = converse.Chat(pairs, reflections)
    chat.converse()


# Sources:
#   https://www.analyticsvidhya.com/blog/2021/07/build-a-simple-chatbot-using-python-and-nltk/
#   https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/
#   https://www.nltk.org/_modules/nltk/chat/util.html#Chat