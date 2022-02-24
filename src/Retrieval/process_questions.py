# Check Licenses
import nltk as N
from nltk.corpus import stopwords
import re

class ProcessQ():
  def __init__(self, userQ):
    self.userQ = userQ

  def cleanInput(self):
    self.userQ = self.userQ.upper()
    self.userQ = re.sub("[^A-Z0-9-/\s]", "", self.userQ)

  def remove_stopWords_tokenize(self):
    exceptions = {"how","of"}
    # Unions the "-" and "/" to remove any tokens where the first part is just "-" or "/"
    stopWords = set(stopwords.words('english')).union({"-","/"})
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
  