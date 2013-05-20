import sys, json

def get_frequency(tweet_file):
    freq_terms = {}
    occurence = 0
    with open(tweet_file) as ft: 
        for line in ft.readlines():
            tw_line = json.loads(line)
            tw_line.setdefault("text", "")
            terms = tw_line["text"].split()
            for term in terms:
               occurence += 1
               freq_terms.setdefault(term, 0)
               freq_terms[term] += 1
    for term in freq_terms:
        freq_terms[term] = freq_terms[term]*1.0/occurence
        print "%s %.3f"%(term.replace(' ', '%20').encode('utf-8'), freq_terms[term])
    return freq_terms
                  
def main():
    freq = get_frequency(sys.argv[1])

if __name__ == '__main__':
    main()
