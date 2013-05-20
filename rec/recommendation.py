from metrics import *

def retrieve_recommendations(prefs, me, \
                             similarity_func=preference_distance):
    """ get a ranking of movie preference score, based on the 
    weighted sum of prefs """
    scores = {}
    sim_weights = {}

    for other in prefs:
        
        if other == me:
            continue
        sim = similarity_func(prefs, me, other)
        if sim <= 0:
            continue

        for item in prefs[other]:
           
            if not prefs[me].has_key(item) or prefs[me][item] == 0:
                scores.setdefault(item, 0)
                scores[item] += sim*prefs[other][item]

                sim_weights.setdefault(item, 0)
                sim_weights[item] += sim

    rankings = [(item, score*1.0/sim_weights[item]) for item, score in scores.iteritems()]

            #sorted(rankings.items(), key = itemgetter(1) , reverse = True)

    return sorted(rankings, key = lambda (k,v): v, reverse = True)
    #return rankings


def transform_preferences(prefs):
    """ transform from user-centric to item-centric """
    rs = {}
    for person in prefs:
        for item in prefs[person]:
            rs.setdefault(item, {})
            rs[item][person] = prefs[person][item]
    return rs

def top_similarity_matches(prefs, person, k = 10,
                         similarity_func=preference_distance):

    scores = [(other, similarity_func(prefs, person, other)) for other in prefs if other != person]
    return sorted(scores, key = lambda (k,v): v, reverse=True)[0:k]
#return scores[0:k]
    
def compute_nearest_items(prefs, k = 10, similarity_func=preference_distance):
    items = transform_preferences(prefs)
    results = {}
    c = 0
    for item in items:
        c += 1
        if c%100==0:
            print '%d / %d% '%(d, len(items))
        top_matches = top_similarity_matches(items, item, k, similarity_func)
        results[item] = top_matches

    return results



def recommended_items(prefs, sim_neighbors, person):
    ratings = prefs[person]
    sim_weights = {}
    scores = {}

    for item, score in ratings.iteritems():
        for neighbor, sim in sim_neighbors[item]:
            if neighbor in ratings: continue

            sim_weights.setdefault(neighbor, 0)
            sim_weights[neighbor] += sim

            scores.setdefault(neighbor, 0)
            scores[neighbor] += sim*score

    rankings = [(item, score/sim_weights[item]) for item, score in scores.iteritems() if sim_weights[item] != 0]

    return sorted(rankings, key=lambda (k,v): v, reverse =  True)
    
        
