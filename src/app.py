from nltk.chat.util import reflections
from Retrieval import retriever
from FAQS import converse
from FAQS import aux_functions
from flask import Flask, render_template, request


# Takes the user query and runs the FAQ algorithm on it, if an answer is found, it is output, otherwise the retrieval algorithm is run
# friendly error messages are output in case no result is found
def run_chatbot(user_input):
    pairs = aux_functions.create_pairs()
    chat = converse.Chat(pairs, reflections)
    output = chat.web_converse(user_input)
    # Result for user q is found in FAQs so print
    if output[0] == 1:
        return str(output[1])
    # Result is NOT found in FAQ so try querying the database
    else:
        res = retriever.run(output[1])
        if isinstance(res,str) and res == "I don't understand\n":
            return "I don't understand\n"
        elif isinstance(res,str) and res == "No data found for your question\n":
            return "No data found for your question\n"
        else:
            return res.to_html(index=False)

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