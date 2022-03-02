import unittest
from FAQS import best_match
from Retrieval import classifier_tab, classifier_col

class TestBot(unittest.TestCase):

    # Following Tests are for best_match.py:

    def test_tokenise_method(self):
        X = "this is a test"
        Y = "this is a question"
        expected_X_list = ["this","is","a","test"]
        expected_Y_list = ["this","is","a","question"]
        X_list, Y_list = best_match.BestMatch().tokenize(X,Y)
        self.assertEqual(expected_X_list,X_list)
        self.assertEqual(expected_Y_list,Y_list)

    # Following Tests are for classifier_tab.py:


    # Following Tests are for classifier_col.py:


if __name__ == "__main__":
    unittest.main()
