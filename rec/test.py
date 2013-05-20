import unittest
from metrics import *
from recommendation import *

critics={

'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
 
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
 
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
 
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
 
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

class TestRecommendation(unittest.TestCase):

    def test_metric(self):
        sm = preference_distance(critics, 'Lisa Rose','Gene Seymour')
        self.assertTrue(abs(sm-0.14814)<0.00001)

        corr = preference_correlation(critics, 'Lisa Rose','Gene Seymour')
        #print corr
        
        self.assertTrue(abs(corr-0.396059017)<0.0001)

    def test_recommendation(self):       
        sm = retrieve_recommendations(critics,'Toby', preference_distance)
        #print sm
        self.assertEqual(len(sm), 3)
        titles = [k for (k,v) in sm]
        self.assertEqual(titles, ['The Night Listener', 'Lady in the Water', 'Just My Luck'])

        #matches = top_similarity_matches(critics, 'Toby', 5, preference_correlation)
        #print matches
        #self.assertTrue(1==0)

    def test_top_matches(self):
        movies = transform_preferences(critics)
        #print top_similarity_matches(movies, 'Superman Returns', 10, preference_correlation)
        
        top_matches = compute_nearest_items(critics, 10, preference_distance)
        #print top_matches
        #print top_matches['Lady in the Water']
        rec = recommended_items(critics, top_matches, 'Toby')
        print rec
        self.assertTrue(1==0)

    
    def load_movieslens_dataset(path='./ml-100k'):
        movies = {}
            
        import os
        if os.path.isfile(path+'/u.item'):
            with open(path+'/u.item') as fi:
                for line in fi.readlines():
                    (id, title) = line.split('|')[0:2]
                    movies[id] = title

        prefs = {}
        if os.path.isfile(path+'/u.data'):
            with open(path+'/u.data') as fi:
                for line in fi.readlines():
                    (user, movieid, rating, ts) = line.split('\t')
                     prefs.setdefault(user, {})
                     prefs[user][movies[movieid]] = float(rating)

        return prefs
