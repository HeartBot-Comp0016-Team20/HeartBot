#COMP0016-Team20-Ivan Varbanov, Neil Badal, Maheem Imran

from collections import defaultdict
from fuzzywuzzy import process
from nltk.corpus import wordnet
import json

class Classifier_Tab():

  def __init__(self, tokens):
    self.tokens = tokens
    # Creates a dictionary with actual table names as in database + other possible
    # words/variations that could be used. For example admissions : ["admissions", "admisions" ,"admits", ...]
    self.table_names = self.create_dict(defaultdict(list))

  # Method to create table_names dictionary in constructor using json file
  # Json file holds the actual table_names as keys and the values are alternative names for tables
  # For example "admissions" : ["admissions", "admits"]
  def create_dict(self, table_names):
    with open('Retrieval/data/table_names.json') as json_file:
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

    # The token is similar to one of the actual table names, we need to find which one
    possible_names = self.table_names[closest_match[0]]
    # Find best match from the possible things the user could have typed
    best_match = process.extractOne(str2Match, possible_names)
    if best_match[1] < 75:
      return 0
    else:
      return closest_match[0]

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

    # Find the best_match synoymn for given tablename
    per_match = 0
    best_match = None
    for tuple in synonym_tuples:
      # If no synonyms for a certain table name
      if len(tuple[1]) == 0:
        continue
      else:
        syn = tuple[1]
        match = process.extractOne(token, syn)
        if match[1] > per_match:
          per_match = match[1]
          best_match = tuple[0]
    if per_match < 80:
      return 0
    else:
      return best_match

  # Runs the different checks to find the best match of table name from the list of tokens
  def get_table_name(self, str2Match):
    res = self.direct_check(str2Match)
    # proceed if direct check failed
    if res == 0:
      actual_names = self.table_names.keys()
      res = self.syn_check(str2Match, actual_names)
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
