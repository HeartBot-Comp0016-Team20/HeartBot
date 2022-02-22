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

  def read_col_name_json_files(self, table_name):
    # Read the json file for the given table into a list of tuples where tuple is in the form: [(column name, [possible values of items in the column])]
    col_names = []
    just_column_names = []
    with open("data/{}.json".format(table_name)) as json_file:
        data = json.load(json_file)
        i = 0
        keys = list(data.keys())
        just_column_names = keys
        values = list(data.values())
        while i < len(keys):
          col_names.append((keys[i],values[i]))
          i = i + 1
    return col_names, just_column_names
  
  def direct_check_for_just_col_names(self, str2Match, just_column_names):
    # Direct Check for column names
    closest_match = process.extractOne(str2Match, just_column_names)
    if closest_match[1] < 75:
      return 0
    else:
      return closest_match[0]

  def direct_check_for_col_names_and_values(self, str2Match, col_names):
    # Direct Check for column names and values - finding the best match for the str2Match with the list of col possible names from list in 2)
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
      return 0, 0
    else:
      return best_match_col_name, best_match_item

  def n_grams_check_for_col_names(self):
    # 5) n-grams Check for column names - finding the best match for the str2Match with the list of col possible names from list in 2)
    # Take the tokens, and find the n-grams, then do a direct check
    pass

  def synonyms_check_for_col_names(self):
    # 6) Synonyms Check - finding the best match for the str2Match with the list of col alternative possible names from alternative_column_names.json
    pass

  def find_column_names(self, table_name):
    cols,just_cols = self.read_col_name_json_files(table_name)

    # Find best matching col_name
    best_match_col_names = []
    best_match_col_vals = []
    for token in self.tokens:
      token = token[0]
      res = self.direct_check_for_just_col_names(token, just_cols)
      if res != 0:
        if res not in best_match_col_names:
          best_match_col_names.append(res)
          best_match_col_vals.append("")
        continue
      # Find best matching value
      else:
        res2, res3 = self.direct_check_for_col_names_and_values(token, cols)
        if res2 != 0 and res3 != 0:
          best_match_col_names.append(res2)
          best_match_col_vals.append(res3)
          continue
        else:
          # Call synonym and n-grams
          pass
    return list(zip(best_match_col_names, best_match_col_vals))


      
if __name__=="__main__":
  # TODO Delete csv files at end
  # Note: Add a check so if there is no table_name or column_name then return invalid question, the code now assumes that the questions are in valid format
  q = input("Please enter the question: ")
  tokens = ProcessQ(q).getProcessedQ()
  print("Tokens: ", tokens)
  table_name = Classifier(tokens).find_table_name()
  print("Table Name: ", table_name)
  col_name_val_pairs  = Classifier(tokens).find_column_names(table_name)
  print("Col Name And Val Pairs: ", col_name_val_pairs)

  # First try returning one value i.e. risk factors with specific conditions
  # Else return the rows from database where the condition matches









# Sources:
#   https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
#   https://www.datacamp.com/community/tutorials/fuzzy-string-python
#   https://www.guru99.com/wordnet-nltk.html
#   https://www.geeksforgeeks.org/nlp-synsets-for-a-word-in-wordnet/
#   https://www.geeksforgeeks.org/convert-json-to-dictionary-in-python/
#   https://www.geeksforgeeks.org/python-read-csv-columns-into-list/
#   https://www.geeksforgeeks.org/get-column-names-from-csv-using-python/
#   https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/