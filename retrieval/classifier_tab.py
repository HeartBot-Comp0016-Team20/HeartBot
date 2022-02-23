from collections import defaultdict
from fuzzywuzzy import process
from nltk.corpus import wordnet
import json

class Classifier_Tab():
  def __init__(self, tokens):
    self.tokens = tokens
    # Create a dictionary with actual table names as in database + other possible
    # words that could be used. For example admissions : ["admissions", "admisions" ,"admits", ...]
    self.table_names = self.create_dict(defaultdict(list))

  # Method to create table_names dictionary in constructor using json file
  # Json file hold the table_names as keys and values are alternative names for tables
  def create_dict(self, table_names):
    with open('data/table_names.json') as json_file:
      data = json.load(json_file)
    i = 0
    keys = list(data.keys())
    values = list(data.values())
    while i < len(keys):
      table_names[keys[i]] = values[i]
      i = i + 1
    return table_names

  # Direct/spelling check to find the closest match
  def direct_check(self, str2Match):
    # Finds the best match for the str2Match with the list of tablenames in the dictionary
    actual_names = self.table_names.keys()
    closest_match = process.extractOne(str2Match, actual_names)

    if closest_match[1] < 75:
      return -1

    # The token is one of the actual table names, we need to find which one
    possible_names = self.table_names[closest_match[0]]
    # Find best match from possible things the user could have typed
    per_match, best_match = self.get_match(str2Match, [possible_names])
    if per_match < 75:
      return 0
    else:
      return best_match[0]

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

  # Creates a list of tuples in the form: [(table_name, [synonyms for tablename])]
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

  # Try different checks to find the best match of table name from the list of tokens
  def get_table_name(self, str2Match):
    res = self.direct_check(str2Match)
    # proceed if direct check failed
    if res == 0:
      actual_names = self.table_names.keys()
      res = self.syn_check(str2Match, actual_names)
    elif res == -1:
      return 0
    return res

  # Uses the methods in the class to get the table name from the list of tokens
  def run(self):
    # If more than one table name in the list of tokens - take the first table name
    table_name = None
    for token in self.tokens:
      token = token[0]
      res = self.get_table_name(token)
      if res != 0:
        table_name = res
        break
    return table_name