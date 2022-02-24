from process_questions import ProcessQ
from classifier_tab import Classifier_Tab
from classifier_col import Classifier_Col
from collections import defaultdict
import pandas as pd

# Read a csv file into a pandas dataframe
def from_csv_to_dataframe(filename):
  data = pd.read_csv(filename)   
  return pd.DataFrame(data)

# Create and return dataframe for a given csv file
def create_dataframe(tablename):
  filename = "data/{}.csv".format(tablename)
  return from_csv_to_dataframe(filename)

# Reformat col_name_val_pairs (returned by classifier_col) into,
# a dictionary. This dictionary is used by filter_dataframe()
def restructure(col_name_val_pairs):
  pairs = defaultdict(list)
  for name_val in col_name_val_pairs:
    if name_val[1] == '':
      continue
    pairs[name_val[0]].append(name_val[1])
  return pairs

# Create query to extract/filter required data from the 
# dataframe then extract data from dataframe using this 
# query; uses the dictionary created in the restructure()
def filter_dataframe(df, pairs_dict):
  output = []
  for key in pairs_dict.keys():
    temp=[]
    for value in pairs_dict[key]:
      if str(value).isnumeric():
        temp.append("{} == {}".format(key,value))
      else:
        # Str vals must be surrounded by double quotes in query
        temp.append("{} == \"{}\"".format(key,value))
    output.append('('+'|'.join(temp)+')')
  final_query = '&'.join(output)
  # Query the dataframe and return the relevent data
  result = df.query(final_query)
  return result

# Given a users questions, finds and returns the relevent data
def run():
  while True:
    # Get users question to query the database
    q = input("Please enter the question: ")
    processor = ProcessQ(q)
    # Split question into tokens
    tokens = processor.getProcessedQ()
    # Find the table_name from list of tokens
    table_name = Classifier_Tab(tokens).run()
    if table_name is None:
      # If valid table_name not found, then data does not exist
      print("I don't understand\n")
    else:
      # If table_name found then data exists, try to return required data
      # Find column_names and column_vals from the list of tokens
      col_name_val_pairs  = Classifier_Col(tokens).run(table_name)
      # Create, query, retrieve and output the required data
      df = create_dataframe(table_name)
      filter_info = restructure(col_name_val_pairs)
      result = filter_dataframe(df,filter_info)
      # Check if the result (i.e. filtered dataframe) is empty
      if result.empty:
        print("No data found for your question\n")
      else:
        print(result,"\n")

if __name__=="__main__":
  run()

'''
Testing - Example Questions:
  what is the asdr in england in 1977
  what is the asdr in countries england and scotland in 1977
  what are the risk factors in wales in 2018                          - DONT WORK
  what are the risk factors in wales in 2019 for females              - DONT WORK
  what are the risk factors in england in 2019 for males              - DONT WORK
  what are the admits in wales in 2010
  what are the number of prescriptions in 2019 in scotland
  how many medicines were given in 2019 in scotland
  how many drugs were given in 2015 in england
  what is the value of ohca in east of england in 2015 where number discharged alive
  What is the estimated burden - deaths in 2009 in the uk
  What is the estimated burden - DALYS in 2009 in the uk
  in what nation was there cvd

Sources:
  https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
  https://www.datacamp.com/community/tutorials/fuzzy-string-python
  https://www.guru99.com/wordnet-nltk.html
  https://www.geeksforgeeks.org/nlp-synsets-for-a-word-in-wordnet/
  https://www.geeksforgeeks.org/convert-json-to-dictionary-in-python/
  https://www.geeksforgeeks.org/python-read-csv-columns-into-list/
  https://www.geeksforgeeks.org/get-column-names-from-csv-using-python/
  https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
'''