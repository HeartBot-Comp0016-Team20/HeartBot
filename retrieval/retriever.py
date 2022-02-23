from process_questions import ProcessQ
from classifier_tab import Classifier_Tab
from classifier_col import Classifier_Col

if __name__=="__main__":

  # Example Questions:
  # what is the asdr in england in 1977
  # what is the asdr in countries england and scotland in 1977
  # what is the risk factors in wales in 2018
  # what are the admits in wales in 2010
  # what are the number of prescriptions in 2019 in scotland
  # how many medicines were given in 2019 in scotland                      NOT WORKING - Says None
  # how many drugs were given in 2015 in england                           NOT WORKING - Says None
  # what is the value of ohca in east of england in 2015 where number discharged alive     ************
  # What is the estimated burden - deaths in 2009 in the uk                                ************
  # What is the estimated burden - DALYS in 2009 in the uk
  # in what nation was there cvd                                      WORKING - Says None

  # Get users question to query the database
  q = input("Please enter the question: ")

  # Get tokens from the question
  tokens = ProcessQ(q).getProcessedQ()
  print("Tokens: ", tokens)

  # Find the table name from list of tokens
  table_name = Classifier_Tab(tokens).run()
  print("Table Name: ", table_name)

  # Find column names from the list of tokens
  if table_name is None:
    print("I dont understand")
  else:
    col_name_val_pairs  = Classifier_Col(tokens).run2(table_name)
    print("Col Name And Val Pairs: ", col_name_val_pairs)

'''
TODO & Notes:
  1) Delete csv files at end
  2) Filter the col_name_val_pairs, so for example if there is (nation,"england") in list then remove (nation,"")
  3) Read the csv/json file into a pandas dataframe, then filter the dataframe using the pairs:
  4) https://www.kite.com/python/answers/how-to-filter-a-pandas-dataframe-by-multiple-columns-in-python
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