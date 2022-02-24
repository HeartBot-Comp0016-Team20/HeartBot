from nltk.chat.util import reflections
from Retrieval import retriever
from FAQS import converse
from FAQS import aux_functions
from flask import Flask, render_template, request

def run_chatbot(user_input):
    pairs = aux_functions.create_pairs()
    chat = converse.Chat(pairs, reflections)
    output = chat.web_converse(user_input)
    # Result for user q is found in FAQs so print
    if output[0] == 1:
        return str(output[1])
    # Result is NOT found in FAQ so try querying the database
    else:
        return str(retriever.run(output[1]))


app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return run_chatbot(userText)

if __name__ == "__main__":
    app.run()