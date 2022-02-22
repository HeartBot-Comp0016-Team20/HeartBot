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
import pandas as pd
import json
import os
import pandas as pd

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
    with open('data/table_names.json') as json_file:
      data = json.load(json_file)
    i = 0
    keys = list(data.keys())
    values = list(data.values())
    while i < len(keys):
      table_names[keys[i]] = values[i]
      i = i + 1
    return table_names

  # Direct/spelling mistake check to find the closest match
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

  # Synonym check to find the closest match
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

  # def hypernymsCheck(self, token):
  #   syn = wordnet.synsets('hello')[0]
  #   print ("Synset name :  ", syn.name())
  #   print ("\nSynset abstract term :  ", syn.hypernyms())
  #   print ("\nSynset specific term :  ", syn.hypernyms()[0].hyponyms()) 
  #   syn.root_hypernyms()
  #   print ("\nSynset root hypernerm :  ", syn.root_hypernyms())

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
    table_name = self.find_table_name()
    column_names_for_table = self.get_tables_columns(table_name)
    for token in self.tokens:
      if token[0].isnumeric():
        pass
        # token is a year
      else:
        pass
        # Check if its other column names

    # Search the sentence tokens for the colums names:
    #   directCheck
    #   n-gramsCheck
    #   synonymCheck
    # After getting the column name then use HypernymCheck to get general column name
    # For example find 'UK', this is converted into 'nation'
    # Also could be directly found, "nation"
    return column_names_for_table

  def get_tables_columns(self, table_name):
    # Note: the case of the filename does not seem to matter
    data = pd.read_csv("data/{}.csv".format(table_name))
    return list(data.columns.values)


      
if __name__=="__main__":

  ### TESTING ###

  # 1) FUNCTION TO CREATE THE DATA
  # Given a table name, find a list of tuples, i.e. [(column names for the table name, set of items in that column)]
  # e.g. for asdr all ages -> ('nation', {'England', 'Wales', 'Northern Ireland', 'United Kingdom', 'Scotland'}) and etc
  # And also add this into a json file
  table_name = "ASDR all ages"
  data = pd.read_csv("data/{}.csv".format(table_name))
  column_names = list(data.columns)
  column_names_and_associated_values = dict()
  for column_name in column_names:
    # OPTIONAL CODE
    # # But this list will also include some other things users may type, we get this from the alternative_column_names.json
    # with open("data/alternative_column_names.json", 'r') as f:
    #   data = json.load(f)
    # extra = data[column_name]
    # # Extend below list with this list
    column_names_and_associated_values[column_name] = list(set(data[column_name].tolist()))
  json_object = json.dumps(column_names_and_associated_values)
  with open("data/{}.json".format(table_name), "w") as f:
    f.write(json_object)

  # 2) Read the json file for the given table into a list of tuples where tuple is in the form: [(column name, [possible values of items in the column])]
  col_names = []
  with open("data/{}.json".format(table_name)) as json_file:
      data = json.load(json_file)
      i = 0
      keys = list(data.keys())
      values = list(data.values())
      while i < len(keys):
        col_names.append((keys[i],values[i]))
        i = i + 1

  # 3) Direct Check for column names - finding the best match for the str2Match with the list of col possible names from list in 2)
  str2Match = "cvd"
  per_match = 0
  best_match_col_name = None
  best_match_item = None
  for possible_col_name in col_names:
    closest_match = process.extractOne(str2Match, possible_col_name[1])
    if closest_match[1] > per_match:
      per_match = closest_match[1]
      best_match_col_name = possible_col_name[0]
      best_match_item = closest_match[0]
  if per_match < 75:
    print(0)
  else:
    print(best_match_col_name, best_match_item)

  # 4) n-grams Check for column names - finding the best match for the str2Match with the list of col possible names from list in 2)
    # Take the tokens, and find the n-grams, then do a direct check

  # 5) Synonyms Check - finding the best match for the str2Match with the list of col alternative possible names from alternative_column_names.json

  ### TESTING ###



  # Note: Add a check so if there is no table_name or column_name then return invalid question,
  # the code now assumes that the questions are in valid format
  q = input("Please enter the question: ")
  tokens = ProcessQ(q).getProcessedQ()
  print(tokens)
  table_name = Classifier(tokens).find_table_name()
  print(table_name)
  column_names = Classifier(tokens).find_column_names()
  print(column_names)









# Sources:
#   https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
#   https://www.datacamp.com/community/tutorials/fuzzy-string-python
#   https://www.guru99.com/wordnet-nltk.html
#   https://www.geeksforgeeks.org/nlp-synsets-for-a-word-in-wordnet/
#   https://www.geeksforgeeks.org/convert-json-to-dictionary-in-python/
#   https://www.geeksforgeeks.org/python-read-csv-columns-into-list/
#   https://www.geeksforgeeks.org/get-column-names-from-csv-using-python/
#   https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/