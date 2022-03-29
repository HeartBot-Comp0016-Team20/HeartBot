#COMP0016-Team20-Ivan Varbanov, Neil Badal, Maheem Imran

import nltk as N
from nltk.corpus import stopwords
import re

class ProcessQ():
  def __init__(self, userQ):
    self.userQ = userQ

# Removes any punctuation from the user input
  def cleanInput(self):
    self.userQ = self.userQ.upper()
    self.userQ = re.sub("[^A-Z0-9-/\s]", "", self.userQ)

# Removes any stop words of the english language with some exceptions
  def remove_stopWords_tokenize(self):
    exceptions = {"how","of"}
    # Unions the "-" and "/" to remove any tokens where the first part is just "-" or "/"
    stopWords = set(stopwords.words('english')).union({"-","/"})
    stop_words = stopWords.difference(exceptions)
    word_tokens = N.word_tokenize(self.userQ)
    filtered = [w for w in word_tokens if not w.lower() in stop_words]
    self.userQ = filtered

# Returns the pos (parts of speech i.e noun, verb etc) for each token
  def pos_tagging(self):
    self.userQ = N.pos_tag(self.userQ)

# Removes punctuation, stop words, and returns tokens with pos tags
  def getProcessedQ(self):
    self.cleanInput()
    self.remove_stopWords_tokenize()
    self.pos_tagging()
    return self.userQ
  
