""" 

train the classifier using the ENRON corpus which could be gotten for free online. it consists of 3 datasets
It will used the 2 of those 3 do train and then we test on the other.

it should give something like

C:\Users\pdt\ps\personal\classi>python enron.py ./data
****************** TESTING ON classifier.NaiveBayesClassifier *****************
training on C:\Users\pdt\ps\personal\classi\data\corpus2
training on C:\Users\pdt\ps\personal\classi\data\corpus3
testing on C:\Users\pdt\ps\personal\classi\data\corpus
result: accuraty = 94.567%

training on C:\Users\pdt\ps\personal\classi\data\corpus
training on C:\Users\pdt\ps\personal\classi\data\corpus3
testing on C:\Users\pdt\ps\personal\classi\data\corpus2
result: accuraty = 93.585%

training on C:\Users\pdt\ps\personal\classi\data\corpus
training on C:\Users\pdt\ps\personal\classi\data\corpus2
testing on C:\Users\pdt\ps\personal\classi\data\corpus3
result: accuraty = 88.633%

In general, I observed that ON THIS CORPUS, without using sophisticated email extraction methods,
Fisher method seems to obtain better results

*************************************
"""

import os, sys
from os.path import isfile, join
from os import listdir

from classifier import *

def get_corpus_path(path = "./data"):
    data_path = os.path.abspath(path)
    dirs = [os.path.join(data_path, di) for di in listdir(path) if os.path.isdir(os.path.join(data_path, di))]
   
    return dirs

def extract_features(s, min_len=2, max_len=20):
   
    words = set()
    for w in s.lower().split():
        wlen = len(w)
        if wlen > min_len and wlen < max_len:
            words.add(w)
    return list(words)

def train(classifier, corpus_paths):
    for path in corpus_paths:
        print 'training on %s ' %(path)
        labels = [di for di in listdir(path) if os.path.isdir(os.path.join(path, di))]#listdir(path)
        for label in labels:            
            label_path = join(path, label)
            
            filenames = [join(label_path, f) for f in listdir(label_path) if isfile(join(label_path, f))]
            for fname in filenames:                
                with open(fname) as fi:                    
                    text = fi.read()
                    #print text
                    classifier.train(text, label)

def test(classifier, corpus_path):
    path = corpus_path
    labels = [di for di in listdir(path) if os.path.isdir(os.path.join(path, di))]
        #labels = listdir(path)

    correct_count = 0
    total_count = 0
    
    for label in labels:            
        label_path = join(path, label)            
        filenames = [join(label_path, f) for f in listdir(label_path) if isfile(join(label_path, f))]
        for fname in filenames:                
            with open(fname) as fi:  
                text = fi.read()
                total_count += 1
                
                results = classifier.predict(text)
                predicted_label = results[0][0]
                
                if predicted_label == label:
                    correct_count += 1

    return float(correct_count)/total_count

def process(classifiers, data_paths):   
    for classifier in classifiers: 
        name = classifier.__class__
        print '****************** TESTING ON %s *****************' %(name)
        for path in data_paths:
            test_corpus = path
            train_corpus = [p for p in corpus_paths if p != path]
            
            
            train(classifier, train_corpus)
            print 'testing on %s'%(test_corpus)            
            accuracy = test(classifier, test_corpus)
            print 'result: accuraty = %.3f%%\n' %(accuracy*100)
        print '*************************************\n\n'

if __name__ == '__main__':
    corpus_paths = get_corpus_path(sys.argv[1]) # path to the 3 corpus directories
    classifiers = [FisherClassifier(),NaiveBayesClassifier(), ]
    process(classifiers, corpus_paths)
