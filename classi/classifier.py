from collections import defaultdict
from stop_words import STOP_WORDS

class Classifier:
    """ """

    def __init__(self):
        self.features = defaultdict(int)
        self.labels = defaultdict(int)
        self.feature_count = defaultdict(lambda: defaultdict(int))

    def _get_features(self, doc):
        import re, math
        splitter=re.compile('\\W*')
        words=[s.lower() for s in splitter.split(doc)
               if len(s)>2 and len(s)<20 and s not in STOP_WORDS]
        return dict([(w,1) for w in words])        
        
    def train(self, document, label):
        features = self._get_features(document)
        for feature in features:
            self.feature_count[feature][label] += 1
            self.features[feature] += 1
        self.labels[label] += 1

    ################  PROBABILITY STUFF  #####################
    def _feature_count(self, feature, label):
        if feature in self.feature_count and label in self.feature_count[feature]:            
            return self.feature_count[feature][label]
        else:
            return 0
    
    def _labels(self):
        return self.labels.keys()   
    
    def feature_probability(self, feature, label):
        """ feature(word) probability given label P(F|L)"""
        feature_count = self.feature_count[feature][label]
        label_count = self.labels[label]
        if label_count != 0:
            return feature_count*1.0/label_count
        return 0.0     

    def adjusted_feature_probability(self, feature, label, \
                            weight = 1.0, assumed_proba = 0.5):
        """ feature(word) probability given label - adjusted to reduce bias """
        unadjusted_proba = self.feature_probability(feature, label)
        feature_total_count = self.features[feature]#sum([self._feature_count(feature, lab) for lab in self._labels()])

        adjusted_proba = (assumed_proba*weight + feature_total_count*unadjusted_proba)*1.0/(feature_total_count+weight)
        return adjusted_proba

    def document_probability(self, document, label):
        """ P(DOC|LABEL) computed using the feature probas under the independance assumption """
        features = self._get_features(document)
        p = 1
        for feature in features:
           
            p *= self.adjusted_feature_probability(feature, label)
            #print p
        return p

    def _label_probability(self, label):
        """ label proba P(L)"""
        label_count = self.labels.get(label, 0)
        label_total_count = sum(self.labels.values())
        return float(label_count)/label_total_count

    def label_probability(self, label,  document):
        """ label probability given document... P(L|D) = P(D|L)*P(L)/P(D) """
        doc_label_proba = self.document_probability(document, label) # proba of this document given label
        label_proba = self._label_probability(label) #. P(label)

        return doc_label_proba*label_proba # note that P(doc) is the same for every item
        

    #################################################################################################################
   

    def predict(self, document, size_limit = 5):
        """ we suppose it's already trained... """       
        probas = {}
            
        for label in self.labels.keys():
            probas[label] = self.label_probability(label, document)
        return sorted(probas.items(), key = lambda (x,y): y, reverse=True)[:size_limit]
   

class NaiveBayesClassifier(Classifier):
    def __init__(self):
        Classifier.__init__(self)



class FisherClassifier(Classifier):
    """  more details on http://www.gigamonkeys.com/book/practical-a-spam-filter.html """
    def __init__(self):
        Classifier.__init__(self)

    def label_feature_probability(self, label, feature):
        """ label given feature, under assumption all the the P(Li) have the same proba """
        feature_proba = self.feature_probability(feature, label)
        total_probas = sum([self.feature_probability(feature, lab) for lab in self._labels()])

        if total_probas == 0: return 0.0
        return float(feature_proba)/total_probas
        
    def adjusted_label_feature_probability(self, label, feature, \
                            weight = 1.0, assumed_proba = 0.5):
        """ feature(word) probability given label - adjusted to reduce bias """
        unadjusted_proba = self.label_feature_probability(label, feature)
        feature_total_count = self.features[feature]

        adjusted_proba = (assumed_proba*weight + feature_total_count*unadjusted_proba)*1.0/(feature_total_count+weight)
        return adjusted_proba
        
        
    def label_probability(self, label, document):
        import math
        """ P(LABEL|DOC) using the Fisher combination """
        features = self._get_features(document)
        p = 1
        for feature in features:           
            p *= self.adjusted_label_feature_probability(label, feature)
        score = -2*math.log(p+math.pow(10, -150))
        return self.inv_chi2P(score, len(features)*2)

    def inv_chi2P(self,chi,df):
        import math
        """Return prob(chisq >= chi, with df degrees of freedom)."""
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df//2):
            term *= m / i
            sum += term
        return min(sum, 1.0)
           

    
