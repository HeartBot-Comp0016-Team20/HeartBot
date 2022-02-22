import json
import pandas as pd

with open('data/table_names.json') as json_file:
    data = json.load(json_file)
table_names = list(data.keys())

# 1) FUNCTION TO CREATE THE DATA
# Given a table name, find a list of tuples, i.e. [(column names for the table name, set of items in that column)]
# e.g. for asdr all ages -> ('nation', {'England', 'Wales', 'Northern Ireland', 'United Kingdom', 'Scotland'}) and etc
# And also add this into a json file
for table_name in table_names:
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