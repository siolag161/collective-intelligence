import unittest

from classifier import *

def sampletrain(cl):
    cl.train('Nobody owns the water.','good')
    cl.train('the quick quick rabbit jumps fences','good')
    cl.train('buy pharmaceuticals now','bad')
    cl.train('make quick money at the online casino','bad')
    cl.train('the quick brown fox jumps','good')

class TestClassification(unittest.TestCase):

    def TestProbabilities(self):
        cl = Classifier()
        sampletrain(cl)

        self.assertTrue(abs(cl.feature_probability('quick', 'good')- 0.66667)<0.001)
        self.assertTrue(abs(cl.adjusted_feature_probability('money', 'good')- 1./4) == 0.0)

        self.assertTrue(abs(cl.label_probability('good', 'quick rabbit')- 0.156249999999) <  0.0001)

    def TestPredict(self):
        cl = NaiveBayesClassifier()
        sampletrain(cl)

        probs = cl.predict('quick rabbit')
        print probs, type(probs)
        #self.assertTrue(1==0)


    def TestFisher(self):
        cl = FisherClassifier()
        sampletrain(cl)
        prob = cl.label_feature_probability('good', 'quick')
        self.assertTrue(abs(prob- 0.571428571) <  0.0001)
        
        prob = cl.label_feature_probability('bad', 'money')      
        self.assertTrue(abs(prob- 1) <  0.0001)

        prob = cl.adjusted_label_feature_probability('bad', 'money')     
        self.assertTrue(abs(prob- 0.75) <  0.0001)

      
        prob = cl.label_probability('good', 'quick rabbit')     
        self.assertTrue(abs(prob- 0.780139865) <  0.0001)
 
        self.assertEqual(cl.predict('quick rabbit'),0)
