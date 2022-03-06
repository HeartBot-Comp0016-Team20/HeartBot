from collections import defaultdict
from fuzzywuzzy import process
from nltk.corpus import wordnet
import nltk
nltk.download('omw-1.4')
from nltk import ngrams
import json

class Classifier_Col():
  def __init__(self, tokens):
    self.tokens = tokens
    self.col_names = self.create_dict(defaultdict(list))

  # Create col_names dictionary initialised in __init__ method using json file; json file 
  # contains the actual col_names as keys and list of alternative names for col_names as values
  def create_dict(self, col_names):
    with open('Retrieval/data/col_names.json') as json_file:
      data = json.load(json_file)
    i = 0
    keys = list(data.keys())
    values = list(data.values())
    while i < len(keys):
      col_names[keys[i]] = values[i]
      i = i + 1
    return col_names

  # Create a set of tokens same as self.tokens but
  # without the pos-tags; used to create n-grams
  def pre_process_n_grams(self, tokens):
    aux = []
    for token in tokens:
      aux.append(token[0])
    return aux

  # Create a list of n-grams from list of tokens
  def create_n_grams(self, n):
    dgrams = []
    tokens = self.pre_process_n_grams(self.tokens)
    n_grams = list(ngrams(tokens, n))
    for grams in n_grams:
        grams = ' '.join(grams)
        dgrams.append((grams,''))
    return dgrams

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
    # Find the best_match synonymn for given col_name
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

  # col_name json files contain key,val pairs. Keys are the col_names for a table_name. Vals are alternative vals col_name could take.
  def read_json(self, table_name):
    # Read the json file for a given table into a list of tuples where tuple is in the form: [(column name, [possible values of items in the column])]
    col_names_vals = []
    just_col_names = []
    with open("Retrieval/data/{}.json".format(table_name)) as json_file:
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

  # Run the different checks in given order on a given list of tokens and tablename
  def run_checks(self, tokens, table_name):
      # Get col_names (column names in table) and col_names_vals (col names and values col_names could take) for a given tablename
      col_names_vals, col_names = self.read_json(table_name)
      # Set (to avoid duplicates) of tuples i.e. set of pairs of col_names and related col_vals found from list of tokens
      # Note: Some tuples may not include the col_val part of tuple, since this is just a col_name without col_val
      # Try finding best match for each token - Try checks in order, if one works add tuple into set and continue onto next token
      col_name_val_pairs = set()
      for token in tokens:
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
      return col_name_val_pairs
   
  # Returns all col_names and col_vals found from list of tokens
  def run(self, table_name):
    # Set to store all the col_name and col_val pairs found
    match_set = set()

    # Initialize the ngrams and tokens lists
    two_grams  = self.create_n_grams(2)
    three_grams = self.create_n_grams(3)
    tokens  = self.tokens
 
    # Check ngrams and regular tokens, add any matches found into set
    match_set = match_set.union(self.run_checks(tokens, table_name))
    match_set = match_set.union(self.run_checks(two_grams, table_name))
    match_set = match_set.union(self.run_checks(three_grams, table_name))
  
    return list(match_set)

