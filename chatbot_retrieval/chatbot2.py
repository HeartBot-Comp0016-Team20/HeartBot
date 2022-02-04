import nltk as N
import string
import re
from nltk.corpus import stopwords

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

if __name__=="__main__":
  q = input("Please enter the question: ")
  cleanedQ = cleanInput(q)
  cleanedQ = remove_stopWords_tokenize(cleanedQ)
  print(cleanedQ)