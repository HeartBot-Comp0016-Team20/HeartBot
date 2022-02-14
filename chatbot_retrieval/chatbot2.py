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
from nltk import ngrams
# N.download('omw-1.4')
import json

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

    # Create a dictionary with actual table names as in database + other possible
    # words that could be used. For example admissions : ["admissions", "admisions" ,"admits", ...]
    self.table_names = self.create_table_names_json(defaultdict(list))

  # Create dictionary for tables_names using the json file details
  def create_table_names_json(self, table_names):
    with open('table_names.json') as json_file:
      data = json.load(json_file)
    i = 0
    keys = list(data.keys())
    values = list(data.values())
    while i < len(keys):
      table_names[keys[i]] = values[i]
      i = i + 1
    return table_names

  # Direct/spelling mistake check to see find the closest match
  def direct_table_name(self, str2Match):
    # Finding the best match for the str2Match with the list of tablenames in the dictionary
    actual_names = self.table_names.keys()
    closest_match = process.extractOne(str2Match, actual_names)

    # The token is one of the actual table names, we need to find which one
    possible_names = self.table_names[closest_match[0]]
    # Find best match from possible things the user could have typed
    per_match, best_match = self.sim_check(str2Match, [possible_names])
    if per_match < 75:
      return 0
    else:
      return best_match[0]

  def synonyms_check(self, token):
    actual_names = self.table_names.keys()
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
      # If no synonyms for a certain table name
      if len(tuple[1]) == 0:
        pass
      else:
        new_per_match, new_best_match = self.sim_check(token, [tuple[1]])
        if new_per_match > per_match:
          per_match = new_per_match
          best_match = tuple
    if per_match < 70:
      return 0
    else:
      return best_match[0]

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

  # def nGramsCheck():
  #   pass

  # Try different checks to find the best match of table name from the list of tokens
  def get_table_name(self, str2Match):
    res = self.direct_table_name(str2Match)
    # proceed if direct check failed
    if res == 0:
      res = self.synonyms_check(str2Match)
    return res

  # Finds the table name from the list of tokens
  def find_table_name(self):
    # If more than one table name in the list of tokens
    # take the first table name
    table_name = None
    for token in self.tokens:
      token = token[0]
      res = self.get_table_name(token)
      if res != 0:
        table_name = res
        break
    return table_name

  def find_column_names(self):
    # Find table name
    # Look in excel sheet and get column names in that table name sheet
    # Search the sentence tokens for the colums names:
    #   directCheck
    #   n-gramsCheck
    #   synonymCheck
    # After getting the column name then use HypernymCheck to get general column name
    # For example find 'UK', this is converted into 'nation'
    # Also could be directly found, "nation"
    pass

  # def hypernymsCheck(self, token):
  #   syn = wordnet.synsets('hello')[0]
  #   print ("Synset name :  ", syn.name())
  #   print ("\nSynset abstract term :  ", syn.hypernyms())
  #   print ("\nSynset specific term :  ", syn.hypernyms()[0].hyponyms()) 
  #   syn.root_hypernyms()
  #   print ("\nSynset root hypernerm :  ", syn.root_hypernyms())

      
if __name__=="__main__":
  q = input("Please enter the question: ")
  tokens = ProcessQ(q).getProcessedQ()
  print(tokens)
  table_name = Classifier(tokens).find_table_name()
  print(table_name)











# Sources:
#   https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
#   https://www.datacamp.com/community/tutorials/fuzzy-string-python
#   https://www.guru99.com/wordnet-nltk.html
#   https://www.geeksforgeeks.org/nlp-synsets-for-a-word-in-wordnet/