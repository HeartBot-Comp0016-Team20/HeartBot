import nltk as N
from nltk.corpus import stopwords
import string
import re

def cleanInput(user_input):
  user_input = user_input.upper()
  user_input.translate(string.punctuation)
  user_input = re.sub("[^A-Z0-9\s]", "", user_input)
  return user_input

def remove_stopWords_tokenize(q):
  exceptions = {"how"}
  stopWords = set(stopwords.words('english'))
  stop_words = stopWords.difference(exceptions)
  word_tokens = N.word_tokenize(q)
  filtered = [w for w in word_tokens if not w.lower() in stop_words]
  return filtered

def pos_tagging(tokens):
  pass

def group_data(tagged_tokens):
  pass

# Add classes

if __name__=="__main__":
  q = input("Please enter the question: ")
  cleanedQ = cleanInput(q)
  cleanedQ = remove_stopWords_tokenize(cleanedQ)
  print(cleanedQ)

# Sources:
#   https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
#