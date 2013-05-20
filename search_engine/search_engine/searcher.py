import sqlite3 as sqlite

from nltk import PorterStemmer


class Searcher:
    stemmer = PorterStemmer()
    def __init__(self,dbname):
        self.con=sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def get_match_rows(self,q):
        # Strings to build the query
        fieldlist = 'w0.urlid'
        tablelist=''  
        clauselist=''
        wordids=[]

    # Split the words by spaces
        words= [Searcher.stemmer.stem(w.lower()) for w in  q.split(' ') if w!=' ' and w!='']
        tablenumber=0

        for word in words:
            # Get the word ID
            wordrow=self.con.execute(
                "select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow!=None:
                wordid=wordrow[0]
                wordids.append(wordid)
                if tablenumber>0:
                    tablelist+=','
                    clauselist+=' and '
                    clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
                fieldlist+=',w%d.location' % tablenumber
                tablelist+='wordlocation w%d' % tablenumber      
                clauselist+='w%d.wordid=%d' % (tablenumber,wordid)
                tablenumber+=1
        if (len(tablelist) == 0) or len(clauselist) == 0:
            return [],[]
        fullquery='select %s from %s where %s'%(fieldlist,tablelist,clauselist)
        cur=self.con.execute(fullquery)
        rows=[row for row in cur]
        return rows,wordids

    def get_url_name(self, urlid):
        query = 'select url from urllist where rowid = %d' %urlid
        return self.con.execute(query).fetchone()[0]

    def get_scored_list(self, rows, wordids):
        total_scores = dict([(row[0], 0) for row in rows])

        weights=[(1.5, self.frequency_scores(rows)), 
                 (1.5, self.location_scores(rows)),
                 (1.5, self.distance_scores(rows)),
            #(1.5, self.inbound_link_scores(rows)),
                 (2.5, self.page_rank_scores(rows)),
                 (3.5, self.link_text_scores(rows, wordids)),
                 ]

        for (weight, scores) in weights:
            for url in scores:
                total_scores[url] += weight*scores[url]

        return total_scores
    
    def query(self, q):
        rows, wordids = self.get_match_rows(q)
        scores = self.get_scored_list(rows, wordids)

        ranked_scores = sorted([(score, item ) 
                                for (item, score) in scores.items()], reverse=1)

        rs = []
        for (score, urlid) in ranked_scores:
            url_name = self.get_url_name(urlid)
            #print '%s\t%f' %(url_name, score)
            rs.append((url_name, score))
        return rs
        
    def normalize_scores(self, scores, smallIsBetter=0):
        vsmall=0.00001 # Avoid division by zero errors
        if smallIsBetter:
            if (len(scores.values()) == 0):
                minscore = vsmall
            else:
                minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
            if (len(scores.values()) == 0):
                maxscore = vsmall
            else:
                maxscore=max(scores.values())
                if maxscore==0: maxscore=vsmall
        return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])
    
    def frequency_scores(self, rows):
        scores = {}
        for row in rows:
            scores.setdefault(row[0], 0)
            scores[row[0]] += 1
        return self.normalize_scores(scores)

    def location_scores(self, rows):
        scores = {}
        for row in rows:
            scores.setdefault(row[0], 100000)
            loc = sum(row[1:])
            if loc < scores[row[0]]:
                scores[row[0]]=loc
        return self.normalize_scores(scores, 1)
        

    def distance_scores(self, rows):
        if not (rows): return {}
        # If there's only one word, everyone wins!
        if len(rows[0])<=2: return dict([(row[0],1.0) for row in rows])

         # Initialize the dictionary with large values
        mindistance=dict([(row[0],1000000) for row in rows])
         
        for row in rows:
            dist=sum([abs(row[i]-row[i-1]) for i in range(2,len(row))])
        if dist<mindistance[row[0]]: mindistance[row[0]]=dist
        return self.normalize_scores(mindistance, smallIsBetter=1)


    def inbound_link_scores(self, rows):
         if not rows: return {}
         unique_urls = set([row[0] for row in rows])
         inbound_count = dict([(u, self.con.execute(\
             'select count(*) from link where toid=%d'% u\
             ).fetchone()[0]) for u in unique_urls             
         ])
         return self.normalize_scores(inbound_count)

    def calculate_page_rank(self, damping_factor = 0.85, iteration_max = 30):
        df = damping_factor
        self.con.execute('drop table if exists page_rank')
        self.con.execute('create table page_rank(urlid primary key, score)')

        self.con.execute('insert into page_rank select rowid, 1.0 from urllist')
        self.con.commit()

        for i in range(iteration_max):
            
            for (urlid, ) in self.con.execute('select rowid from urllist'):
                pr = 1-df
                linkers =  self.con.execute(''' select distinct fromid 
                    from link where toid = %d''' %urlid)
                for (linker, ) in linkers:
                    linking_page = self.con.execute(\
                        'select score from page_rank where urlid = %d' %linker \
                        ).fetchone()[0]
                    linking_count = self.con.execute(\
                        'select count(*) from link where fromid = %d' %linker \
                        ).fetchone()[0]
                    
                    pr += df*(linking_page/linking_count)
                self.con.execute(''' update page_rank set 
                        score = %f where urlid = %d''' %(pr, urlid))

            self.con.commit()

    def link_text_scores(self, rows, wordids):
        if not rows or not wordids: return {}
        link_scores = dict([(row[0], 0) for row in rows])
        for wordid in wordids:
            curr = self.con.execute('''  select link.fromid, link.toid from linkwords, link
              where wordid=%d and linkwords.linkid = link.rowid ''' % wordid)

            for (fromid, toid) in curr:
                if toid in link_scores:
                    pr = self.con.execute('select score from \
                    page_rank where urlid= %d' %fromid).fetchone()[0]
                    link_scores[toid] += pr
        max_score = max(link_scores.values())
        if (max_score == 0): max_score =1 
        normalized_scores = dict([(u, float(l)/max_score) 
                                 for (u,l) in link_scores.iteritems() ])      
        return normalized_scores  
            
    def page_rank_scores(self,rows):
        if not rows: return {}
        
        page_ranks=dict([(row[0],self.con.execute('select score from \
           page_rank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
        max_rank=max(page_ranks.values())
        normalized_scores=dict([(u,float(l)/max_rank) for (u,l) in page_ranks.items()])
        return normalized_scores
