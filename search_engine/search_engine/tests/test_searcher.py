
from search_engine.searcher import Searcher
import unittest

class TestSearcher(unittest.TestCase):


    def test_normalize_scores(self):
        s = Searcher('abc.db')
        
        self.assertEqual(s.normalize_scores({}, 1), {})
        self.assertEqual(s.normalize_scores({}, 0), {})

    
    def test_distance_scores(self):
        s = Searcher('abc.db')
        
        self.assertEqual(s.distance_scores({}), {})
        
   
    def test_query(self):
        s = Searcher('search_engine_nyk.sql')
        
        #self.assertEqual(s.query('AOAPAPA'), [])
        #print(s.query('love')[:1])
        #print(s.query('Mad Men'))
        #self.assertEqual(s.query('Mad Men'), [])
        pass

    def test_inbound_scores(self):
        s = Searcher('nyw.sql')

        s.calculate_page_rank()
        self.assertNotEqual(s.inbound_link_scores({}), {})
        


        #print(s.query('Mad Men'))
        #
        #        self.assertNotEqual(s.inbound_link_scores({}), {})

    
