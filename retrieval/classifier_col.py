from collections import defaultdict
from nis import match
from fuzzywuzzy import process
from nltk.corpus import wordnet
from nltk import ngrams
import json

class Classifier_Col():
  def __init__(self, tokens):
    self.tokens = tokens
    self.col_names = self.create_dict(defaultdict(list))

  # Method to create col_names dictionary in constructor using json file
  # Json file hold the col_names as keys and values are alternative names for cols
  def create_dict(self, col_names):
    with open('data/col_names.json') as json_file:
      data = json.load(json_file)
    i = 0
    keys = list(data.keys())
    values = list(data.values())
    while i < len(keys):
      col_names[keys[i]] = values[i]
      i = i + 1
    return col_names

  # Creates a list of tuples in the form: [(col_name, [synonyms for col_name])]
  def syn_tup(self, actual_names):
    synonym_tuples = []
    for name in actual_names:
      tup = (name,[])
      for syn in wordnet.synsets(name):
        for l in syn.lemmas():
          tup[1].append(l.name())
      synonym_tuples.append(tup)
    return synonym_tuples

  # Given a str2Match and a list of things to match from, the functions finds and returns the best match\
  # Helper Method - Used in syn_check
  def get_match(self, str2Match, possible_names):
    per_match = 0
    best_match = None
    for possible_name in possible_names:
      match = process.extractOne(str2Match, possible_name)
      if match[1] == 100:
        per_match = match[1]
        best_match = possible_name
        break
      elif match[1] > per_match:
        per_match = match[1]
        best_match = possible_name
    return per_match, best_match

  # Synonym check to find the closest match
  def syn_check(self, token, actual_names):
    # Get the synonyms for each table name
    synonym_tuples = self.syn_tup(actual_names)

    # Find the best_match synoymn for the tablename
    per_match = 0
    best_match = None
    for tuple in synonym_tuples:
      # If no synonyms for a certain table name
      if len(tuple[1]) == 0:
        pass
      else:
        new_per_match, new_best_match = self.get_match(token, [tuple[1]])
        if new_per_match > per_match:
          per_match = new_per_match
          best_match = tuple
    if per_match < 70:
      return 0
    else:
      return best_match[0]

  # Column name json files hold as keys the column names and as values the values that the column names can take
  def read_json(self, table_name):
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
  
  # Direct Check 1 - Checks against str2Match against the actual column names and any spelling mistakes
  def direct_check1(self, str2Match, just_column_names):
    match = process.extractOne(str2Match, just_column_names)
    if match[1] < 75:
      actual_names = self.col_names.keys()
      res = self.syn_check(str2Match, actual_names)
      if res == 0:
        return 0
      else:
        return res
    else:
      return match[0]

  # Direct Check 2 - Checks for values that column names could take - finding the best match for the str2Match from the values that the col could take
  def direct_check2(self, str2Match, col_names):
    per_match = 0
    best_match_col = None
    best_match_item = None
    for possible_col_name in col_names:
      match = process.extractOne(str2Match, possible_col_name[1])
      if match[1] > per_match:
        per_match = match[1]
        best_match_col = possible_col_name[0]
        best_match_item = match[0]
    if per_match < 75:
      return 0, 0
    else:
      return best_match_col, best_match_item

  def n_grams_check(self):
    # n-grams Check for column names - finding the best match for the str2Match with the list of col possible names from list in 2)
    # Take the tokens, and find the n-grams, then do a direct check
    pass

  def run(self, table_name):
    cols, just_cols = self.read_json(table_name)

    # Find best matching col_name
    best_match_col_names = []
    best_match_col_vals = []
    for token in self.tokens:
      token = token[0]
      res = self.direct_check1(token, just_cols)
      if res != 0 and res is not None:
        if res not in best_match_col_names:
          best_match_col_names.append(res)
          best_match_col_vals.append("")
        continue
      # Find best matching value
      else:
        res2, res3 = self.direct_check2(token, cols)
        if res2 != 0 and res3 != 0:
          best_match_col_names.append(res2)
          best_match_col_vals.append(res3)
          continue
        else:
          # Call synonym and n-grams
          pass
    return list(zip(best_match_col_names, best_match_col_vals))