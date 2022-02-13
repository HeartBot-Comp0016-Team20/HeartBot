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

  # Direct/spelling mistake check to see find the closest match
  def direct_table_name(self, str2Match):
    # Finding the best match for the str2Match with the list of tablenames in the dictionary
    actual_names = self.tablesNames.keys()
    closest_match = process.extractOne(str2Match, actual_names)

    # If the closest match percentage is too low then try another check else continue
    if closest_match[1] < 75:
      return 0

    # The token is one of the actual table names, we need to find which one
    possible_names = self.tablesNames[closest_match[0]]
    # Find best match from possible things the user could have typed
    per_match, best_match = self.sim_check(str2Match, [possible_names])
    if per_match < 75:
      return 0
    else:
      return best_match

  def synonyms_check(self, token):
    actual_names = self.tablesNames.keys()
    # A list of lists, where is list a list of synoyms for each tablename
    synonym_tuples = []
    for name in actual_names:
      syn_tup = (name,[])
      for syn in wordnet.synsets(name):
        for l in syn.lemmas():
          syn_tup[1].append(l.name())
      synonym_tuples.append(syn_tup)

    per_match = 0
    best_match = None
    for tuple in synonym_tuples:
      # If no synonyms for a certain tablename
      if len(tuple[1]) == 0:
        pass
      else:
        per_match, best_match = self.sim_check(token, tuple[1])
        if per_match < 70:
          return 0
        else:
          return best_match

  # Given a str2Match and a list of things to match from, the functions finds and returns the best match
  def sim_check(self, str2Match, possible_names):
    per_match = 0
    best_match = None
    for possible_name in possible_names:
      closest_match = process.extractOne(str2Match, possible_name)
      if closest_match[1] == 100:
        per_match = closest_match[1]
        best_match = possible_name
        break
      elif closest_match[1] > per_match:
        per_match = closest_match[1]
        best_match = possible_name
    return per_match, best_match



  # def hypernymsCheck(self, token):
  #   syn = wordnet.synsets('hello')[0]
  #   print ("Synset name :  ", syn.name())
  #   print ("\nSynset abstract term :  ", syn.hypernyms())
  #   print ("\nSynset specific term :  ", syn.hypernyms()[0].hyponyms()) 
  #   syn.root_hypernyms()
  #   print ("\nSynset root hypernerm :  ", syn.root_hypernyms())

  def nGramsCheck():
    pass

  def get_table_name(self, str2Match):
    res = self.direct_table_name(str2Match)
    # proceed if direct check failed
    if res == 0:
      res = self.synonyms_check(str2Match)
    return res

      



if __name__=="__main__":
  
  t = Classifier([]).get_table_name("entry")
  print(t)

  q = input("Please enter the question: ")
  question1 = ProcessQ(q).getProcessedQ()
  print(question1)

# Sources:
#   https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
#   https://www.datacamp.com/community/tutorials/fuzzy-string-python
#   https://www.guru99.com/wordnet-nltk.html
#   https://www.geeksforgeeks.org/nlp-synsets-for-a-word-in-wordnet/