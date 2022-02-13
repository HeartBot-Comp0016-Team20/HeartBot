# Check Licenses
from turtle import pos
import nltk as N
from nltk.corpus import stopwords
import string
import re
from collections import defaultdict
import pandas as pd
from fuzzywuzzy import process
from nltk.corpus import wordnet
N.download('omw-1.4')

class ProcessQ():
  def __init__(self, userQ):
    self.userQ = userQ

  def cleanInput(self):
    self.userQ = self.userQ.upper()
    self.userQ = self.userQ.translate(string.punctuation)
    self.userQ = re.sub("[^A-Z0-9\s]", "", self.userQ)

  def remove_stopWords_tokenize(self):
    exceptions = {"how"}
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

class Classifier():
  def __init__(self, tokens):
    self.tokens = tokens
    # These are the attributes for the SQL query
    self.tableName = None
    self.columnNames = []
    self.other = []

    # Create a dictionary with the actual tableName as in database + synonyms
    # as the key. The values for the keys are lists with other possible
    # words that could be used. For example admissions : ["admissions", "admisions" ,"admits", ...]
    # Note: in each value list the first word will always be the exact database word
    # TODO Create a list of alternative words people could type
    # TODO Add a way to automatically add this list into the values list
    actualTableNames = self.get_sheet_names()
    self.tablesNames  = defaultdict(list)
    for tableName in actualTableNames:
      tableName = tableName.lower()
      self.tablesNames[tableName].append(tableName)

  # Get the tableNames
  def get_sheet_names(self):
    xls = pd.ExcelFile("data.xlsx")
    return xls.sheet_names

  def directCheckForTableNames(self, str2Match, highestMatch=0, highestMatchList=None):
    # Direct/spelling mistake check to see find the closest match
    possibleTableNames = self.tablesNames.keys()
    highest = process.extractOne(str2Match, possibleTableNames)
    possibleTableNames = self.tablesNames[highest[0]]
    # Find best match from possible things the user could have typed
    for possibleTableName in possibleTableNames:
      highest = process.extractOne(str2Match, possibleTableName)
      if highest[1] == 100:
        highestMatchList = possibleTableName
        break
      elif highest[1] > highestMatch:
        highestMatch = highest[1]
        highestMatchList = possibleTableName
    if highestMatch < 75:
      return 0
    else:
      return highestMatchList

  def synonymsCheck(self, token):
    synonyms = []
    for syn in wordnet.synsets("active"):
      for l in syn.lemmas():
        synonyms.append(l.name())
    print(set(synonyms))

  def hypernymsCheck(self, token):
    syn = wordnet.synsets('hello')[0]
    print ("Synset name :  ", syn.name())
    print ("\nSynset abstract term :  ", syn.hypernyms())
    print ("\nSynset specific term :  ", syn.hypernyms()[0].hyponyms()) 
    syn.root_hypernyms()
    print ("\nSynset root hypernerm :  ", syn.root_hypernyms())

  def nGramsCheck():
    pass


if __name__=="__main__":

  t = Classifier([]).directCheckForTableNames("admits")
  print(t)

  q = input("Please enter the question: ")
  question1 = ProcessQ(q).getProcessedQ()
  print(question1)

# Sources:
#   https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
#   https://www.datacamp.com/community/tutorials/fuzzy-string-python
#   https://www.guru99.com/wordnet-nltk.html
#   https://www.geeksforgeeks.org/nlp-synsets-for-a-word-in-wordnet/