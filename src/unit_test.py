# COMP0016-Team20-Ivan Varbanov, Neil Badal, Maheem Imran

import unittest
from FAQS import best_match
from Retrieval import classifier_tab, classifier_col, process_questions

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

    def test_find_closest(self):
        Q = "How many people are diabetics?"
        res = best_match.BestMatch().find_closest_q(Q)
        self.assertEqual("How many people have diabetes in the UK?",res)

    # Following Tests are for classifier_tab.py:
    def test_find_closest_tab(self):
        Q = "preverence"
        res = classifier_tab.Classifier_Tab('').direct_check(Q)
        self.assertEqual(res,"prevalence")

    def test_find_closest_tab_negative(self):
        Q = "padgvcbcce"
        res = classifier_tab.Classifier_Tab('').direct_check(Q)
        self.assertEqual(res,0)
    
    def test_get_table_name(self):
        Q = "deaths"
        res = classifier_tab.Classifier_Tab('').get_table_name(Q)
        self.assertEqual(res,"deaths by cause age sex uk")

    def test_get_table_name_negative(self):
        Q = "heart attack"
        res = classifier_tab.Classifier_Tab('').get_table_name(Q)
        self.assertEqual(res,0)

    # Following Tests are for classifier_col.py:
    def test_n_grams(self):
        res = classifier_col.Classifier_Col([('They', 'PRP'), ('refuse', 'VBP'), ('to', 'TO')]).create_n_grams(2)
        self.assertEqual(res,[('They refuse', ''), ('refuse to', '')])

    def test_run(self):
        processed = process_questions.ProcessQ('what is the value of ohca in scotland ').getProcessedQ()
        res = classifier_col.Classifier_Col(processed).run('prevalence')
        self.assertEqual(res,[('nation', 'Scotland')])

if __name__ == "__main__":
    unittest.main()
