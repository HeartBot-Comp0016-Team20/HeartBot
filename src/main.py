from nltk.chat.util import reflections
from Retrieval import retriever
from FAQS import converse
from FAQS import aux_functions

def run_chatbot():
    print("Welcome to HeartBot FAQ! \n")
    pairs = aux_functions.create_pairs()
    chat = converse.Chat(pairs, reflections)
    output = chat.web_converse()
    # Result for user q is found in FAQs so print
    if output[0] == 1:
        return output[1]
    # Result is NOT found in FAQ so try querying the database
    else:
        return retriever.run(output[1])

if __name__ == "__main__":
    print(run_chatbot())