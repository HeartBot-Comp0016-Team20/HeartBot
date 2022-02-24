from nltk.chat.util import reflections
from FAQS import converse
from FAQS import aux_functions
    

if __name__ == "__main__":
    print("Welcome to HeartBot FAQ! \n")
    pairs = aux_functions.create_pairs()
    chat = converse.Chat(pairs, reflections)
    chat.converse()