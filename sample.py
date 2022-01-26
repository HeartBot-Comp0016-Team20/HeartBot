from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from sample2 import startChat

data=[]
with open('FAQs.txt') as f:
	lines = f.readlines()
	for line in lines:
		data.append(line.strip('\n'))
bot=ChatBot(
	'Heartbot',
	storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
	database_uri = 'sqlite:///database.sqlite3',
	logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.jaccard_similarity",
            "response_selection_method": "chatterbot.response_selection.get_first_response"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': "I didn't understand that question; do you need help with Math, Excel, Music or Graphic?"
        }
    ],
	
)

trainer = ListTrainer(bot)
trainer.train(data)

# Test Questions:
#1) How many people have heart failure in Wales?
#2) How many people are affected by Heart and Circulatory Diseases in the UK?

print("Welcome to HeartBot FAQ! \n")
question = input("Please enter your question: ")
while question not in ["bye","exit"]:
	response = bot.get_response(question)
	print("Bot Response:",response,"\n")
	question = input("Please enter your question: ")
print("Thank you for using HeartBot FAQ \n")


