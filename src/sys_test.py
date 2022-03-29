# COMP0016-Team20-Ivan Varbanov, Neil Badal, Maheem Imran

import unittest
from app import run_chatbot
import pandas as pd

class TestSystem(unittest.TestCase):

    def test_faq(self):
        input = "How many people have high blood pressure in Northern Ireland?"
        expected_output = "An estimated 400,000 people in Northern Ireland have high blood pressure (hypertension)."
        output = run_chatbot(input)
        self.assertEqual(expected_output,output)

    def test_faq_variation(self):
        input = "How many women 65 above in Wales are obese?"
        expected_output = "In Wales, 25% of women aged 65-74 and 18% of women aged 75+ are classified as obese."
        output = run_chatbot(input)
        self.assertEqual(expected_output,output)

    def test_data_q_admissions(self):
        input = "what are the admits in wales in 2010"
        data = pd.read_csv("Retrieval/data/admissions.csv")  
        df = pd.DataFrame(data)
        expected_output = df.query("(`nation`==\"Wales\")&(`fin_year`==\"2010/11\")")
        output = run_chatbot(input)
        self.assertEqual(expected_output.to_html(index=False),output)

    def test_data_q_asdr(self):
        input = "what is the asdr in england in 1977"
        output = run_chatbot(input)
        data = pd.read_csv("Retrieval/data/asdr all ages.csv")  
        df = pd.DataFrame(data)
        expected_output = df.query("(`nation`==\"England\")&(`year`==1977)")
        self.assertEqual(expected_output.to_html(index=False),output)

    def test_data_q_burden(self):
        input = "What is the estimated burden - DALYS in 2009 in the uk"
        output = run_chatbot(input)
        data = pd.read_csv("Retrieval/data/burden.csv")  
        df = pd.DataFrame(data)
        expected_output = df.query("(`Nation`==\"UK\")&(`Year`==2009)")
        self.assertEqual(expected_output.to_html(index=False),output)

    def test_data_q_deathsbycauseagesex(self):
        input = "how many deaths were there of people aged 75-84 from circulatory diseases"
        output = run_chatbot(input)
        data = pd.read_csv("Retrieval/data/deaths by cause age sex uk.csv")  
        df = pd.DataFrame(data)
        expected_output = df.query("((`cause`==\"All heart and circulatory diseases\")|(`cause`==\"Diseases of arteries, arterioles and capillaries\"))&(`age_group`==\"75-84\")")
        self.assertEqual(expected_output.to_html(index=False),output)

    def test_data_q_ohca(self):
        input = "what is the value of ohca in east of england in 2015 where number discharged alive"
        output = run_chatbot(input)
        data = pd.read_csv("Retrieval/data/ohca.csv")  
        df = pd.DataFrame(data)
        expected_output = df.query("((`ambulance_trust`==\"East of England Ambulance Service NHS Trust\")|(`ambulance_trust`==\"England\")|(`ambulance_trust`==\"Isle of Wight NHS Trust\")|(`ambulance_trust`==\"East Midlands Ambulance Service NHS Trust\"))&(`fin_year`==\"2015-16\")&((`measure`==\"number_discharged_alive\")|(`measure`==\"proportion_discharged_alive\"))")
        self.assertEqual(expected_output.to_html(index=False),output)

    def test_data_q_prescriptions(self):
        input = "what are the number of prescriptions in 2019 in scotland"
        output = run_chatbot(input)
        data = pd.read_csv("Retrieval/data/prescriptions.csv")  
        df = pd.DataFrame(data)
        expected_output = df.query("(`nation`==\"Scotland\")&(`year_adjust`==2019)")
        self.assertEqual(expected_output.to_html(index=False),output)

    def test_data_q_prescriptions_synonym(self):
        input = "how many medicines were given in 2019 in scotland"
        output = run_chatbot(input)
        data = pd.read_csv("Retrieval/data/prescriptions.csv")  
        df = pd.DataFrame(data)
        expected_output = df.query("(`nation`==\"Scotland\")&(`year_adjust`==2019)")
        self.assertEqual(expected_output.to_html(index=False),output)

    def test_data_q_prevalence(self):
        input = "what is the prevelence for england in 2014/15"
        output = run_chatbot(input)
        data = pd.read_csv("Retrieval/data/prevalence.csv")  
        df = pd.DataFrame(data)
        expected_output = df.query("(`nation`==\"England\")&(`fin_year`==\"2014/15\")")
        self.assertEqual(expected_output.to_html(index=False),output)

    def test_data_q_procedures(self):
        input = "how many procedures in 1982 for CABG"
        output = run_chatbot(input)
        data = pd.read_csv("Retrieval/data/procedures.csv")  
        df = pd.DataFrame(data)
        expected_output = df.query("(`year`==1982)&(`proc_name`==\"CABG\")")
        self.assertEqual(expected_output.to_html(index=False),output)

    def test_data_q_riskfactors(self):
        input = "what are the risk factors in wales in 2019/20"
        output = run_chatbot(input)
        data = pd.read_csv("Retrieval/data/risk factors.csv")  
        df = pd.DataFrame(data)
        expected_output = df.query("(`Year`==\"2019/20\")&(`Nation`==\"Wales\")")
        self.assertEqual(expected_output.to_html(index=False),output)

    def test_unknown_q(self):
        input = "what are the risk factors in wales in 2018"
        output = run_chatbot(input)
        expected_output = "No data found for your question\n"
        self.assertEqual(expected_output,output)

    def test_greeting(self):
        input = "what is your name"
        output = run_chatbot(input)
        expected_output = "I am HeartBot. you can call me crazy!"
        self.assertEqual(expected_output,output)

    def test_randominput(self):
        input = "%%%#"
        output = run_chatbot(input)
        expected_output = "I don't understand. Please include a table name in your query\n"
        self.assertEqual(expected_output,output)
        

if __name__ == "__main__":
    unittest.main()
