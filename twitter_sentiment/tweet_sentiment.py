import sys
import json
import string


sent_dict = {}
    
def get_scores(sent_file):
    with open(sent_file) as fi:
        for line in fi.readlines():
            l = line.split('\t')
            if (l != None and len(l)>1):
                term = l[0]
                score = l[1]
                sent_dict[term] = float(score)

def get_tweet_score(tweet):
    score = 0.0
    wds = {}

    for i  in range(10):
        score = 0.0
        terms = tweet.split(' ')
    
        pos_count = 0
        neg_count = 0

        for term in terms:
            term = term.rstrip(string.punctuation)
            if sent_dict.has_key(term):
                stm = sent_dict[term]
                score += stm
                if (stm > 0): 
                    pos_count += 1
                else:
                    neg_count += 1      
            else:
                wds.setdefault(term, 0.0)   
                score += wds[term]
        for term in wds:
            
            wds[term] = score/n
                
    return score 
                
def hw(sent_file, tweet_file):    
    get_scores(sent_file)
    with open(tweet_file) as ft: 
        l = 0
        for line in ft.readlines():
            l += 1
            tw_line = json.loads(line)
            tw_line.setdefault("text", "")
            if (tw_line.has_key("text")):           
                score = get_tweet_score(tw_line["text"])
            print(score)
    
    lines(sent_file)
    lines(tweet_file)

def lines(fi):
    with open(fi) as fp:
        print str(len(fp.readlines()))

        
def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw(sys.argv[1], sys.argv[2])
   

if __name__ == '__main__':
    main()
