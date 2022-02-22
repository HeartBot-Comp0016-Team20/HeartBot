from process_questions import ProcessQ
from classifier_tab import Classifier_Tab
from classifier_col import Classifier_Col

if __name__=="__main__":
  # TODO Delete csv files at end
  # Note: Add a check so if there is no table_name or column_name then return invalid question, the code now assumes that the questions are in valid format
  q = input("Please enter the question: ")
  tokens = ProcessQ(q).getProcessedQ()
  print("Tokens: ", tokens)
  table_name = Classifier_Tab(tokens).run()
  print("Table Name: ", table_name)
  col_name_val_pairs  = Classifier_Col(tokens).run(table_name)
  print("Col Name And Val Pairs: ", col_name_val_pairs)

  # First try returning one value i.e. risk factors with specific conditions
  # Else return the rows from database where the condition matches


# Sources:
#   https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
#   https://www.datacamp.com/community/tutorials/fuzzy-string-python
#   https://www.guru99.com/wordnet-nltk.html
#   https://www.geeksforgeeks.org/nlp-synsets-for-a-word-in-wordnet/
#   https://www.geeksforgeeks.org/convert-json-to-dictionary-in-python/
#   https://www.geeksforgeeks.org/python-read-csv-columns-into-list/
#   https://www.geeksforgeeks.org/get-column-names-from-csv-using-python/
#   https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/