import nltk
nltk.download('punkt')
import re

def cleanInput(user_input):
  user_input = user_input.upper()
  user_input = re.sub("[^A-Z0-9\s]", "", user_input)
  return user_input

question = input("Please enter the question: ")
cleanedQuestion = cleanInput(question)
tokenisedQuestion = nltk.word_tokenize(cleanedQuestion)
print(tokenisedQuestion)
# Loop through tokens and see if it matches the existing sections
# Group by 2/3 - using nltk
# Loop through tokens and see if it matches the existing sections
# If all the sections matches then search query