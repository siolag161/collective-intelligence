import sqlite3 as sqlite
import os, re

# Porter Stemming
from nltk import PorterStemmer

#punctuation
import string

ignorewords={'the':1,'of':1,'to':1,'and':1,'a':1,'in':1,'is':1,'it':1}
    

class DbTool:
  # Initialize the crawler with the name of database
    def __init__(self, dbname, recreate=False):		
        if recreate:
            try:
                os.remove(dbname)
            except OSError:
                pass

        if not os.path.isfile(dbname):
            self.con=sqlite.connect(dbname)
            self.create_index_tables()
            
        self.con=sqlite.connect(dbname)
        
    def __del__(self):
        self.con.close()

    def commit(self):
        self.con.commit()

  # Auxilliary function for getting an entry id and adding 
  # it if it's not present
    def get_entry_id(self,table,field,value,createnew=True):
        cur=self.con.execute(
            "select rowid from %s where %s='%s'" % (table,field,value))
        res=cur.fetchone()
        if res==None:
            cur=self.con.execute(
                "insert into %s (%s) values ('%s')" % (table,field,value))
            return cur.lastrowid
        else:
            return res[0] 


    def is_indexed(self,url):
        u=self.con.execute \
          ("select rowid from urllist where url='%s'" % url).fetchone( )
        if u!=None:
              # Check if it has actually been crawled
            v=self.con.execute(
                    'select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v!=None: return True
        return False
    
    def add_to_index(self,url,text):
        if self.is_indexed(url): return
        #print 'Indexing '+url
  
        # Get the individual words
        words = self.separate_words(text)
    
        # Get the URL id
        urlid = self.get_entry_id('urllist','url',url)
    
        # Link each word to this url
        for i in range(len(words)):
            word=words[i]
            if word in ignorewords: continue
            wordid=self.get_entry_id('wordlist','word',word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)" % (urlid,wordid,i))
  
  # Seperate the words by any non-whitespace character
    ps = PorterStemmer()
    splitter=re.compile('\\W*')
    @staticmethod
    def separate_words(text):        
        words = [DbTool.ps.stem(s.strip(string.punctuation).lower()) for s in DbTool.splitter.split(text) 
                if  s!='']
            #print 'alibababa----------------------',len(words)
        return words
    
    def add_link_ref(self,urlFrom,urlTo,linkText):
        words=self.separate_words(linkText)
        fromid=self.get_entry_id('urllist','url',urlFrom)
        toid=self.get_entry_id('urllist','url',urlTo)
        if fromid==toid: return
        cur=self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
        linkid=cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid=self.get_entry_id('wordlist','word',word)
            self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid,wordid))

  
    def create_index_tables(self): 
        self.con.execute('create table if not exists urllist(url)')
        self.con.execute('create table if not exists wordlist(word)')
        self.con.execute('create table if not exists wordlocation(urlid,wordid,location)')
        self.con.execute('create table if not exists link(fromid integer,toid integer)')
        self.con.execute('create table if not exists linkwords(wordid,linkid)')
        self.con.execute('create index if not exists wordidx on wordlist(word)')
        self.con.execute('create index if not exists urlidx on urllist(url)')
        self.con.execute('create index if not exists wordurlidx on wordlocation(wordid)')
        self.con.execute('create index if not exists urltoidx on link(toid)')
        self.con.execute('create index if not exists urlfromidx on link(fromid)')
        self.commit()
