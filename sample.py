from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

data=[]
with open('FAQs.txt') as f:
	lines = f.readlines()
	for line in lines:
		data.append(line.strip('\n'))
bot=ChatBot(
	'Heartbot',
	storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
	database_uri = 'sqlite:///database.sqlite3',
	logic_adapters = [
		'chatterbot.logic.BestMatch',
		'chatterbot.logic.TimeLogicAdapter'],
	
)

trainer = ListTrainer(bot)

trainer.train(data)
response = bot.get_response('How many people have heart failure in Wales?')
print("Bot Response:",response)


