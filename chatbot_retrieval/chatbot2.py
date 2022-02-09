from turtle import pos
import nltk as N
from nltk.corpus import stopwords
import string
import re
from collections import defaultdict
import pandas as pd
from fuzzywuzzy import process

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

if __name__=="__main__":
  
  # Get the tableNames
  def get_sheet_names():
    xls = pd.ExcelFile("data.xlsx")
    return xls.sheet_names

  # Create a dictionary with the actual tableName as in database + synonyms
  # as the key. The values for the keys are lists with other possible
  # words that could be used. For example admissions : ["admissions", "admits", ...]
  # Note: in each value list the first word will always be the exact database word
  # TODO Create a list of alternative words people could type
  # TODO Add a way to automatically add this list into the values list
  actualTableNames = get_sheet_names()
  tablesNames  = defaultdict(list)
  for tableName in actualTableNames:
    tableName = tableName.lower()
    tablesNames[tableName].append(tableName)
  # print(tablesNames)

  # Direct/(synonym)/spelling mistake check to see find the closest match
  str2Match = "admits"
  possibleTableNames = tablesNames.values()
  highestMatch = 0
  highestMatchList = None
  for possibleTableName in possibleTableNames:
    # Find best match from possible things the user could have typed
    highest = process.extractOne(str2Match, possibleTableName)
    if highest[1] > highestMatch:
      highestMatch = highest[1]
      highestMatchList = possibleTableName
  if highestMatch < 75:
    print("Try Other Checks in Classifer")
  else:
    # Convert thing the user typed into what SQL database uses
    print("Found Match:", highestMatchList[0])

  # TODO N-gram Check
  # TODO Hypernym/Synonym Check

  # TODO This section of the code will be added into a class
  # It can be run on the different part of the SQL query





  q = input("Please enter the question: ")
  question1 = ProcessQ(q).getProcessedQ()
  print(question1)

# Sources:
#   https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
#   https://www.datacamp.com/community/tutorials/fuzzy-string-python