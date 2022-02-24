from Retrieval import process_questions
from Retrieval import classifier_tab
from Retrieval import classifier_col
from collections import defaultdict
import pandas as pd

# Read a csv file into a pandas dataframe
def from_csv_to_dataframe(filename):
  data = pd.read_csv(filename)   
  return pd.DataFrame(data)

# Create and return dataframe for a given csv file
def create_dataframe(tablename):
  filename = "Retrieval/data/{}.csv".format(tablename)
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
        temp.append("`{}` == {}".format(key,value))
      else:
        # Str vals must be surrounded by double quotes in query
        temp.append("`{}` == \"{}\"".format(key,value))
    output.append('('+'|'.join(temp)+')')
  final_query = '&'.join(output)
  # Query the dataframe and return the relevent data
  result = df.query(final_query)
  return result

# Given a users questions, finds and returns the relevent data
def run(q):
  processor = process_questions.ProcessQ(q)
  # Split question into tokens
  tokens = processor.getProcessedQ()
  # Find the table_name from list of tokens
  table_name = classifier_tab.Classifier_Tab(tokens).run()
  if table_name is None:
    # If valid table_name not found, then data does not exist
    return "I don't understand\n"
  else:
    # If table_name found then data exists, try to return required data
    # Find column_names and column_vals from the list of tokens
    col_name_val_pairs  = classifier_col.Classifier_Col(tokens).run(table_name)
    # Create, query, retrieve and output the required data
    df = create_dataframe(table_name)
    filter_info = restructure(col_name_val_pairs)
    result = filter_dataframe(df,filter_info)
    # Check if the result (i.e. filtered dataframe) is empty
    if result.empty:
      return "No data found for your question\n"
    else:
      return result

if __name__=="__main__":
  print(run())