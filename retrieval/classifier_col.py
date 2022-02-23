from collections import defaultdict
from fuzzywuzzy import process
from nltk.corpus import wordnet
# nltk.download('omw-1.4')
from nltk import ngrams
import json

class Classifier_Col():
  def __init__(self, tokens):
    self.tokens = tokens
    self.col_names = self.create_dict(defaultdict(list))

  # Create col_names dictionary inistialesed in __init__ method using json file;
  # json file contains the actual col_names as keys and list of alternative names for col_names as values
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

  # Given a str2Match and a list of things to match from, the functions finds and returns the best match
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

  # Synonym check to find the closest match
  def syn_check(self, token, actual_names):
    # Get the actual col_names and synonyms for each col_name
    synonym_tuples = self.syn_tup(actual_names)
    # Find the best_match synonymn for the col_name
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

  # col_name json files contain key,val pairs. Keys are the col_names for a table_name. Vals are alternative vals col_name could take.
  def read_json(self, table_name):
    # Read the json file for a given table into a list of tuples where tuple is in the form: [(column name, [possible values of items in the column])]
    col_names_vals = []
    just_col_names = []
    with open("data/{}.json".format(table_name)) as json_file:
        data = json.load(json_file)
        i = 0
        keys = list(data.keys())
        just_col_names = keys
        values = list(data.values())
        while i < len(keys):
          col_names_vals.append((keys[i],values[i]))
          i = i + 1
    return col_names_vals, just_col_names
  
  # Direct Check 1 - Find best_match for str2Match in the actual col_names and spelling mistakes in them
  def direct_check1(self, str2Match, just_column_names):
    match = process.extractOne(str2Match, just_column_names)
    if match[1] < 75:
      return 0
    else:
      return match[0]

  # Direct Check 2 - Find best_match for str2Match from list of vals that col_names could take
  #                - Returns a list of tuples, where tuples are in the form: (col_name, col_val)
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

  # n-grams check to find the closest match
  # def n_grams_check(self):
  #   # finding the best match for the str2Match with the list of col possible names from list
  #   # Take the tokens, and find the n-grams, then do a direct check

  # Returns all col_names and col_vals found from list of tokens
  def run(self, table_name):
    # Get col_names and col_names_vals for a given tablename
    col_names_vals, col_names = self.read_json(table_name)
    # Set (to avoid duplicates) of tuples i.e. pairs of col_names and related col_vals found from tokens
    # Note: Some tuples may not include the col_val value, since this is just a col_name
    col_name_val_pairs = set()
    # Try finding best match for each token - Try checks in order, if one works add tuple into set and continue onto next token
    for token in self.tokens:
      token = token[0]
      # Check 1 - Direct Check 1 for col_names
      res = self.direct_check1(token, col_names)
      if res != 0 and res is not None:
        col_name_val_pairs.add((res,""))
        continue
      # Check 2 - Direct Check 2 for col_vals
      res, res2 = self.direct_check2(token, col_names_vals)
      if res != 0 and res2 != 0:
        col_name_val_pairs.add((res,res2))
        continue
      # Check 3 - Synonym Check for col_names
      res = self.syn_check(token, col_names)
      if res != 0:
        col_name_val_pairs.add((res,""))
        continue
      # TODO Add extra checks:
      # # Check 4 - Synonym Check for col_vals
      # res5, res6 = self.syn_check(token, col_names_vals)
      # if res5 != 0 and res6 != 0:
      #   col_name_val_pairs.add((res5,res6))
      #   continue
      # # Check 5 - n-grams Check for col_names
      # # Check 6 - n-grams Check for col_vals
    return list(col_name_val_pairs)

