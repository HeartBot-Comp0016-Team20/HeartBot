# How many men in the UK die from coronary heart disease?
# Sex - Men, Nation - UK, Disease - chd, Type of Question - How Many - Count

import nltk
nltk.download('punkt')
import re

sex = ['men', 'woman']
nation = ['uk', 'england' 'wales']
disease = ['chd',"coronary heart disease"]
typesOfQuestions = ['how many', 'what is']
tables = []

# clean the question - make lower and remove stop words
# tokenise the question
# try and identify the words in the question

def cleanInput(inp):
  inp = inp.lower()
  inp = re.sub("[^a-z0-9\s]", "", inp)
  return inp

question = input("Please enter the question: ")
cleanedQuestion = cleanInput(question)
tokenisedQuestion = nltk.word_tokenize(cleanedQuestion)
print(tokenisedQuestion)
# Loop through tokens and see if it matches the existing sections
# Group by 2/3 - using nltk
# Loop through tokens and see if it matches the existing sections
# If all the sections matches then search query