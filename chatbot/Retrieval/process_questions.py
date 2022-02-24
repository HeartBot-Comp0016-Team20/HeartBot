# Check Licenses
import nltk as N
from nltk.corpus import stopwords
import string
import re

class ProcessQ():
  def __init__(self, userQ):
    self.userQ = userQ

  def cleanInput(self):
    self.userQ = self.userQ.upper()
    self.userQ = self.userQ.translate(string.punctuation)
    self.userQ = re.sub("[^A-Z0-9\s]", "", self.userQ)

  def remove_stopWords_tokenize(self):
    exceptions = {"how","of"}
    stopWords = set(stopwords.words('english'))
    stop_words = stopWords.difference(exceptions)
    word_tokens = N.word_tokenize(self.userQ)
    filtered = [w for w in word_tokens if not w.lower() in stop_words]
    self.userQ = filtered

  def pos_tagging(self):
    self.userQ = N.pos_tag(self.userQ)

  def getProcessedQ(self):
    self.cleanInput()
    self.remove_stopWords_tokenize()
    self.pos_tagging()
    return self.userQ
  