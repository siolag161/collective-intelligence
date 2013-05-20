from math import sqrt
import numpy as np

def preference_distance(prefs, p1, p2):

    commun_prefs = set(prefs[p1].keys()).intersection(set(prefs[p2].keys()))
    if not commun_prefs:
        return 0.0

    sos = sum(pow(prefs[p1][item]-prefs[p2][item], 2) for item in commun_prefs)
    return 1/(1+sos)

def preference_correlation(prefs, p1, p2):
    
    commun_prefs = set(prefs[p1].keys()).intersection(set(prefs[p2].keys()))
    if not commun_prefs:
        return 0.0

    n = len(commun_prefs)
    
    x_bar = sum(prefs[p1][item] for item in commun_prefs)*1.0/n
    y_bar = sum(prefs[p2][item] for item in commun_prefs)*1.0/n    

    XY = sum((prefs[p1][i]-x_bar)*(prefs[p2][i]-y_bar) for i in commun_prefs)    
    
    X = sum((prefs[p1][item]-x_bar)**2 for item in commun_prefs)
    Y = sum((prefs[p2][item]-y_bar)**2 for item in commun_prefs)
    if (X*Y == 0): return 0.0
    return (XY)/(sqrt(X*Y))

def preference_jaccard(prefs, p1, p2):
    
    union_prefs = set(prefs[p1].keys()).intersection(set(prefs[p2].keys()))
    if not union_prefs: return 0.0
    
    commun_prefs = set(prefs[p1].keys()).intersection(set(prefs[p2].keys()))

    return len(common_prefs)*1.0/len(union_prefs)
    
