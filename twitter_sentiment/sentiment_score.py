  

def get_scores(sent_file):
    sent_dict = {}
    with open(sent_file) as fi:
        for line in fi.readlines():
            l = line.split('\t')
            if (l != None and len(l)>1):
                term = l[0]
                score = l[1]
                sent_dict[term] = float(score)
    return sent_dict

def retrive_scores(sent_file, tweet_file):


def main():
    hw(sys.argv[1], sys.argv[2])
   

if __name__ == '__main__':
    main()
