#COMP0016-Team20-Ivan Varbanov, Neil Badal, Maheem Imran

import json
import pandas as pd

with open('data/table_names.json') as json_file:
    data = json.load(json_file)
table_names = list(data.keys())

# Run this file once if the data is changed, in order to create json files with the new data

# 1) FUNCTION TO CREATE THE DATA
# Given a table name, finds a list of tuples, i.e. [(column names for the table name, set of items in that column)]
# e.g. for asdr all ages -> ('nation', {'England', 'Wales', 'Northern Ireland', 'United Kingdom', 'Scotland'}) etc
# And also adds this into a json file
for table_name in table_names:
    data = pd.read_csv("data/{}.csv".format(table_name))
    column_names = list(data.columns)
    column_names_and_associated_values = dict()
    for column_name in column_names:
        # * OPTIONAL CODE
        column_names_and_associated_values[column_name] = list(set(data[column_name].tolist()))
    json_object = json.dumps(column_names_and_associated_values)
    with open("data/{}.json".format(table_name), "w") as f:
        f.write(json_object)

# * But this list can also include some other things users may type, we get this from the alternative_column_names.json where we can add these variations/synonyms
        # with open("data/alternative_column_names.json", 'r') as f:
        #   data = json.load(f)
        # extra = data[column_name]
        # # Extend below list with this list
